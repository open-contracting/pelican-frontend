
import time
import random
import intervals as I
import simplejson as json

from django.db.models import Count, Max, Min, Sum
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core import serializers
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

from .models import Dataset, DatasetLevelCheck, ResourceLevelCheck, Report, TimeVarianceLevelCheck, DataItem
from .tools.rabbit import publish


@csrf_exempt
def create_dataset_filter(request):
    if request.method == 'GET':
        return HttpResponseBadRequest(reason='Only post method is accepted.')

    publish(request.body, '_dataset_filter_extractor_init')

    return HttpResponse('done')


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
def dataset_distinct_values(request, dataset_id, json_path):
    json_path = 'data__' + '__'.join(json_path.split('.'))
    data_items_query = DataItem.objects.filter(dataset_id=dataset_id)
    values = list(data_items_query.values_list(json_path, flat=True).distinct())

    return JsonResponse([v for v in values if v is not None], safe=False)


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
