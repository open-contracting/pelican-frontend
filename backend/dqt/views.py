
import time
import random
import intervals as I
import simplejson as json
from psycopg2 import sql

from datetime import datetime
from django.db.models import Count, Max, Min, Sum
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core import serializers
from django.db import connections
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from .tools.gdocs import Gdocs
from .tools.gdocs import process_template
from .tools.tags.template_tags.base import BaseTemplateTag

from .models import Dataset, DatasetLevelCheck, ResourceLevelCheck, Report, TimeVarianceLevelCheck, DataItem
from .tools.rabbit import publish


@csrf_exempt
def create_dataset_filter(request):
    if request.method == 'GET':
        return HttpResponseBadRequest(reason='Only post method is accepted.')

    publish(request.body, '_dataset_filter_extractor_init')

    return HttpResponse('done')


@csrf_exempt
def dataset_filter_items(request):
    if request.method == 'GET':
        return HttpResponseBadRequest(reason='Only post method is accepted.')

    body_unicode = request.body.decode('utf-8')
    input_message = json.loads(body_unicode)

    # checking input_message correctness
    if (
        "dataset_id_original" not in input_message or not isinstance(input_message['dataset_id_original'], int)
        or "filter_message" not in input_message or not isinstance(input_message['filter_message'], dict)
    ):
        return HttpResponseBadRequest(reason='Input message is malformed, will be dropped.')

    dataset_id_original = input_message["dataset_id_original"]
    filter_message = input_message["filter_message"]

    # building query in a safely manner
    try:
        query = sql.SQL("SELECT count(*) FROM data_item WHERE dataset_id = ") + sql.Literal(dataset_id_original)
        if 'release_date_from' in filter_message:
            expr = sql.SQL("data->>'date' >= ") + sql.Literal(filter_message['release_date_from'])
            query += sql.SQL(' and ') + expr
        if 'release_date_to' in filter_message:
            expr = sql.SQL("data->>'date' <= ") + sql.Literal(filter_message['release_date_to'])
            query += sql.SQL(" and ") + expr
        if 'buyer' in filter_message:
            expr = sql.SQL(", ").join([
                sql.Literal(buyer)
                for buyer in filter_message['buyer']
            ])
            expr = sql.SQL("data->'buyer'->>'name' in ") + sql.SQL("(") + expr + sql.SQL(")")
            query += sql.SQL(" and ") + expr
        if 'buyer_regex' in filter_message:
            expr = sql.SQL("data->'buyer'->>'name' LIKE ") + sql.Literal(filter_message['buyer_regex'])
            query += sql.SQL(" and ") + expr
        if 'procuring_entity' in filter_message:
            expr = sql.SQL(", ").join([
                sql.Literal(procuring_entity)
                for procuring_entity in filter_message['procuring_entity']
            ])
            expr = sql.SQL("data->'tender'->'procuringEntity'->>'name' in ") + sql.SQL("(") + expr + sql.SQL(")")
            query += sql.SQL(" and ") + expr
        if 'procuring_entity_regex' in filter_message:
            expr = sql.SQL("data->'tender'->'procuringEntity'->>'name' LIKE ") \
                + sql.Literal(filter_message['procuring_entity_regex'])
            query += sql.SQL(" and ") + expr
        query += sql.SQL(';')

        with connections["data"].cursor() as cursor:
            cursor.execute(query)
            items = cursor.fetchall()[0][0]
    except:
        return HttpResponseBadRequest(reason='The dataset could not be filtered in this way.')

    return JsonResponse({'items': items})


def dataset_stats(request, dataset_id):
    result = {}
    dataset_meta = Dataset.objects.get(id=dataset_id)
    result["name"] = dataset_meta.name
    result["meta"] = dataset_meta.meta

    return JsonResponse(result)


def dataset_level_stats(request, dataset_id):
    result = {}
    checks = DatasetLevelCheck.objects.filter(
        dataset=dataset_id)
    for check in checks:
        result[check.check_name] = {
            "result": check.result,
            "value": check.value,
            "meta": check.meta,
        }
    return JsonResponse(result)


# json_path requires shape: field1.field2.field3 ...
def dataset_distinct_values(request, dataset_id, json_path, sub_string=''):
    json_path = 'data__' + '__'.join(json_path.split('.'))
    kwargs = {
        'dataset_id': dataset_id,
        json_path + '__icontains': sub_string
    }
    data_items_query = DataItem.objects.filter(
        **kwargs).values(json_path).annotate(count=Count(json_path)).order_by('-count')
    query_set = data_items_query.values_list(json_path, 'count').distinct()[:200]
    return JsonResponse([{'value': el[0], 'count': el[1]} for el in query_set], safe=False)


def field_level_stats(request, dataset_id):
    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data
            from report
            where dataset_id = %s and type = 'field_level_check';
            """, [dataset_id]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no field_level_check report for dataset_id: {}".format(dataset_id)
                }
            )

        return JsonResponse(rows[0][0])


def field_level_detail(request, dataset_id, path):
    start_time = time.time()

    result = None

    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data->%s
            from report
            where dataset_id = %s and
                  type = 'field_level_check' and
                  data ? %s;
            """, [path, dataset_id, path]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no results for dataset_id: {}, path: '{}' combination".format(dataset_id, path)
                }
            )

        result = rows[0][0]

        # getting examples
        cursor.execute(
            """
            select data
            from field_level_check_examples
            where dataset_id = %s and path = %s;
            """, [dataset_id, path]
        )
        data = cursor.fetchall()[0][0]

        result['coverage']['passed_examples'] = data['coverage']['passed_examples']
        result['coverage']['failed_examples'] = data['coverage']['failed_examples']
        result['quality']['passed_examples'] = data['quality']['passed_examples']
        result['quality']['failed_examples'] = data['quality']['failed_examples']

        for check_name, check in data['coverage']['checks'].items():
            result['coverage']['checks'][check_name]['passed_examples'] = check['passed_examples']
            result['coverage']['checks'][check_name]['failed_examples'] = check['failed_examples']

        for check_name, check in data['quality']['checks'].items():
            result['quality']['checks'][check_name]['passed_examples'] = check['passed_examples']
            result['quality']['checks'][check_name]['failed_examples'] = check['failed_examples']

    result["time"] = time.time() - start_time

    return JsonResponse(result)


def resource_level_stats(request, dataset_id):
    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data
            from report
            where dataset_id = %s and type = 'resource_level_check';
            """, [dataset_id]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no resource_level_check report for dataset_id: {}".format(dataset_id)
                }
            )

        return JsonResponse(rows[0][0])


def resource_level_detail(request, dataset_id, check_name):
    start_time = time.time()

    result = None

    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data->%s
            from report
            where dataset_id = %s and
                  type = 'resource_level_check' and
                  data ? %s;
            """, [check_name, dataset_id, check_name]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no results for dataset_id: {}, check_name: '{}' combination".format(
                        dataset_id,
                        check_name
                    )
                }
            )

        result = rows[0][0]

        # getting examples
        cursor.execute(
            """
            select data
            from resource_level_check_examples
            where dataset_id = %s and
                  check_name = %s;
            """, [dataset_id, check_name]
        )
        data = cursor.fetchall()[0][0]
        result = {**result, **data}

    result["time"] = time.time() - start_time

    return JsonResponse(result)


def time_variance_level_stats(request, dataset_id):
    result = {}
    checks = TimeVarianceLevelCheck.objects.all().filter(dataset=dataset_id)
    for check in checks:
        result[check.check_name] = {
            "coverage_value": check.coverage_value,
            "coverage_result": check.coverage_result,
            "check_value": check.check_value,
            "check_result": check.check_result,
            "meta": check.meta
        }
    return JsonResponse(result)

TEMPLATE_DOCUMENT_ID = '1paW4y4jxkWOi12qq1IVWlhKe9-WbosJATkp_BDRGTiA'

FOLDER_ID = "1yLTCRV3yoBM5Goc93SaO4irxnd0iapnK"

@csrf_exempt
def generate_report(request):
    if request.method == 'GET':
        return HttpResponseBadRequest(reason='Only post method is accepted.')

    body_unicode = request.body.decode('utf-8')
    input_message = json.loads(body_unicode)

    # checking input_message correctness
    if (
        "dataset_id" not in input_message or not isinstance(input_message["dataset_id"], int) or
        "document_id" not in input_message or "folder_id" not in input_message
    ):
        return HttpResponseBadRequest(reason='Input message is malformed, will be dropped.')

    # gdocs = Gdocs(input_message["document_id"])
    # main_template = gdocs.get_main_template()
    # main_template = process_template(main_template, {}, gdocs, input_message['dataset_id'])
    # file_id = gdocs.upload(FOLDER_ID, input_message["document_id"], "Paraguay {}".format(datetime.now()), main_template)
    # gdocs.destroy_tempdir()

    gdocs = Gdocs(input_message["document_id"])
    base = BaseTemplateTag(gdocs, input_message['dataset_id'])
    base.set_param('template', input_message['document_id'])
    main_template = base.validate_and_process()
    
    file_id = gdocs.upload(FOLDER_ID, input_message["document_id"], "Paraguay {}".format(datetime.now()), main_template)
    # gdocs.destroy_tempdir()

    return HttpResponse(file_id)