import time

import simplejson as json
from django.db import connections
from django.db.models import Count
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from psycopg2.sql import SQL

from .models import DataItem, Dataset, DatasetLevelCheck, TimeVarianceLevelCheck


@csrf_exempt
def dataset_filter_items(request):
    if request.method == "GET":
        return HttpResponseBadRequest(reason="Only post method is accepted.")

    body_unicode = request.body.decode("utf-8")
    input_message = json.loads(body_unicode)

    # checking input_message correctness
    if (
        "dataset_id_original" not in input_message
        or not isinstance(input_message["dataset_id_original"], int)
        or "filter_message" not in input_message
        or not isinstance(input_message["filter_message"], dict)
    ):
        return HttpResponseBadRequest(reason="Input message is malformed, will be dropped.")

    dataset_id_original = input_message["dataset_id_original"]
    filter_message = input_message["filter_message"]

    # building query in a safely manner
    try:
        variables = {"dataset_id_original": dataset_id_original}
        parts = ["SELECT count(*) FROM data_item WHERE dataset_id = %(dataset_id_original)s"]

        if "release_date_from" in filter_message:
            variables["release_date_from"] = filter_message["release_date_from"]
            parts.append("data->>'date' >= %(release_date_from)s")

        if "release_date_to" in filter_message:
            variables["release_date_to"] = filter_message["release_date_to"]
            parts.append("data->>'date' <= %(release_date_to)s")

        if "buyer" in filter_message:
            variables["buyer"] = tuple(buyer for buyer in filter_message["buyer"])
            parts.append("data->'buyer'->>'name' IN %(buyer)s")

        if "buyer_regex" in filter_message:
            variables["buyer_regex"] = filter_message["buyer_regex"]
            parts.append("data->'buyer'->>'name' LIKE %(buyer_regex)s")

        if "procuring_entity" in filter_message:
            variables["procuring_entity"] = tuple(
                procuring_entity for procuring_entity in filter_message["procuring_entity"]
            )
            parts.append("data->'tender'->'procuringEntity'->>'name' IN %(procuring_entity)s")

        if "procuring_entity_regex" in filter_message:
            variables["procuring_entity_regex"] = filter_message["procuring_entity_regex"]
            parts.append("data->'tender'->'procuringEntity'->>'name' LIKE %(procuring_entity_regex)s")

        with connections["data"].cursor() as cursor:
            cursor.execute(SQL(" AND ".join(parts)), variables)
            items = cursor.fetchall()[0][0]
    except Exception:
        return HttpResponseBadRequest(reason="The dataset could not be filtered in this way.")

    return JsonResponse({"items": items})


def dataset_stats(request, dataset_id):
    result = {}
    dataset_meta = Dataset.objects.get(id=dataset_id)
    result["name"] = dataset_meta.name
    result["meta"] = dataset_meta.meta

    return JsonResponse(result)


def dataset_level_stats(request, dataset_id):
    result = {}
    checks = DatasetLevelCheck.objects.filter(dataset=dataset_id)
    for check in checks:
        result[check.check_name] = {
            "result": check.result,
            "value": check.value,
            "meta": check.meta,
        }
    return JsonResponse(result)


# json_path requires shape: field1.field2.field3 ...
def dataset_distinct_values(request, dataset_id, json_path, sub_string=""):
    json_path = "data__" + "__".join(json_path.split("."))
    kwargs = {"dataset_id": dataset_id, json_path + "__icontains": sub_string}
    data_items_query = (
        DataItem.objects.filter(**kwargs).values(json_path).annotate(count=Count(json_path)).order_by("-count")
    )
    query_set = data_items_query.values_list(json_path, "count").distinct()[:200]
    return JsonResponse([{"value": el[0], "count": el[1]} for el in query_set], safe=False)


def field_level_stats(request, dataset_id):
    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data
            from report
            where dataset_id = %s and type = 'field_level_check';
            """,
            [dataset_id],
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse({"error": f"no field_level_check report for dataset_id: {dataset_id}"})

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
            """,
            [path, dataset_id, path],
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse({"error": f"no results for dataset_id: {dataset_id}, path: '{path}' combination"})

        result = rows[0][0]

        # getting examples
        cursor.execute(
            """
            select data
            from field_level_check_examples
            where dataset_id = %s and path = %s;
            """,
            [dataset_id, path],
        )
        data = cursor.fetchall()[0][0]

        result["coverage"]["passed_examples"] = data["coverage"]["passed_examples"]
        result["coverage"]["failed_examples"] = data["coverage"]["failed_examples"]
        result["quality"]["passed_examples"] = data["quality"]["passed_examples"]
        result["quality"]["failed_examples"] = data["quality"]["failed_examples"]

        for check_name, check in data["coverage"]["checks"].items():
            result["coverage"]["checks"][check_name]["passed_examples"] = check["passed_examples"]
            result["coverage"]["checks"][check_name]["failed_examples"] = check["failed_examples"]

        for check_name, check in data["quality"]["checks"].items():
            result["quality"]["checks"][check_name]["passed_examples"] = check["passed_examples"]
            result["quality"]["checks"][check_name]["failed_examples"] = check["failed_examples"]

    result["time"] = time.time() - start_time

    return JsonResponse(result)


def resource_level_stats(request, dataset_id):
    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data
            from report
            where dataset_id = %s and type = 'resource_level_check';
            """,
            [dataset_id],
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse({"error": f"no resource_level_check report for dataset_id: {dataset_id}"})

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
            """,
            [check_name, dataset_id, check_name],
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {"error": f"no results for dataset_id: {dataset_id}, check_name: '{check_name}' combination"}
            )

        result = rows[0][0]

        # getting examples
        cursor.execute(
            """
            select data
            from resource_level_check_examples
            where dataset_id = %s and
                  check_name = %s;
            """,
            [dataset_id, check_name],
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
            "meta": check.meta,
        }
    return JsonResponse(result)
