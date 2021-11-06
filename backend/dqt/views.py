import time
from datetime import datetime

import simplejson as json
from django.conf import settings
from django.db import connections
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from psycopg2 import sql

from .models import (
    DataItem,
    Dataset,
    DatasetLevelCheck,
    FieldLevelCheck,
    ProgressMonitorDataset,
    TimeVarianceLevelCheck,
)
from .tools.errors import GoogleDriveError, TagError
from .tools.gdocs import Gdocs
from .tools.rabbit import publish
from .tools.tags.template_tags.base import BaseTemplateTag


@csrf_exempt
def create_dataset_filter(request):
    if request.method == "GET":
        return HttpResponseBadRequest(reason="Only post method is accepted.")

    publish(request.body, "_dataset_filter_extractor_init")

    return HttpResponse("done")


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
        query = sql.SQL("SELECT count(*) FROM data_item WHERE dataset_id = ") + sql.Literal(dataset_id_original)
        if "release_date_from" in filter_message:
            expr = sql.SQL("data->>'date' >= ") + sql.Literal(filter_message["release_date_from"])
            query += sql.SQL(" and ") + expr
        if "release_date_to" in filter_message:
            expr = sql.SQL("data->>'date' <= ") + sql.Literal(filter_message["release_date_to"])
            query += sql.SQL(" and ") + expr
        if "buyer" in filter_message:
            expr = sql.SQL(", ").join([sql.Literal(buyer) for buyer in filter_message["buyer"]])
            expr = sql.SQL("data->'buyer'->>'name' in ") + sql.SQL("(") + expr + sql.SQL(")")
            query += sql.SQL(" and ") + expr
        if "buyer_regex" in filter_message:
            expr = sql.SQL("data->'buyer'->>'name' LIKE ") + sql.Literal(filter_message["buyer_regex"])
            query += sql.SQL(" and ") + expr
        if "procuring_entity" in filter_message:
            expr = sql.SQL(", ").join(
                [sql.Literal(procuring_entity) for procuring_entity in filter_message["procuring_entity"]]
            )
            expr = sql.SQL("data->'tender'->'procuringEntity'->>'name' in ") + sql.SQL("(") + expr + sql.SQL(")")
            query += sql.SQL(" and ") + expr
        if "procuring_entity_regex" in filter_message:
            expr = sql.SQL("data->'tender'->'procuringEntity'->>'name' LIKE ") + sql.Literal(
                filter_message["procuring_entity_regex"]
            )
            query += sql.SQL(" and ") + expr
        query += sql.SQL(";")

        with connections["data"].cursor() as cursor:
            cursor.execute(query)
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


@csrf_exempt
def generate_report(request):
    if request.method == "GET":
        return JsonResponse({"status": "report_error", "data": {"reason": "Only post method is accepted."}})

    body_unicode = request.body.decode("utf-8")
    input_message = json.loads(body_unicode)

    # checking input_message correctness
    if (
        "dataset_id" not in input_message
        or not isinstance(input_message["dataset_id"], int)
        or "document_id" not in input_message
        or "folder_id" not in input_message
    ):
        return JsonResponse(
            {"status": "report_error", "data": {"reason": "Input message is malformed, will be dropped."}}
        )

    if "language" in input_message and input_message["language"] in dict(settings.LANGUAGES):
        # switch to input language
        translation.activate(input_message["language"])
    else:
        translation.activate("en")

    response = None
    gdocs = None

    try:
        gdocs = Gdocs(input_message["document_id"])
        base = BaseTemplateTag(gdocs, input_message["dataset_id"])
        base.set_param("template", input_message["document_id"])
        base.finalize_params()
        failed_tags = []
        main_template, failed_tags = base.validate_and_process({})

        report_name = "Report %s %s" % (input_message["dataset_id"], datetime.now())
        if "report_name" in input_message and isinstance(input_message["report_name"], str):
            report_name = input_message["report_name"]

        file_id = gdocs.upload(input_message["folder_id"], report_name, main_template)

        response = JsonResponse({"status": "ok", "data": {"file_id": file_id}, "failed_tags": failed_tags})
    except GoogleDriveError as er:
        response = JsonResponse({"status": "report_error", "data": {"reason": str(er)}})
    except TagError as er:
        response = JsonResponse(
            {
                "status": "template_error",
                "data": [er.as_dict()],  # Can accommodate multiple TagErrors in the future
                "failed_tags": failed_tags,
            }
        )
    finally:
        if gdocs is not None:
            gdocs.destroy_tempdir()

    # restores default english translations
    translation.activate("en")
    return response


@csrf_exempt
def dataset_start(request):
    if request.method == "GET":
        return JsonResponse({"status": "error", "data": {"reason": "Only post method is accepted."}})

    routing_key = "_ocds_kingfisher_extractor_init"

    body = json.loads(request.body.decode("utf-8"))

    dataset_name = body.get("name")

    message = {
        "name": dataset_name,
        "collection_id": body.get("collection_id"),
        # "ancestor_id": ancestor_id,
        # "max_items": max_items,
    }

    publish(json.dumps(message), routing_key)

    return JsonResponse(
        {"status": "ok", "data": {"message": f"Dataset {dataset_name} on Pelican started"}}, safe=False
    )


@csrf_exempt
def dataset_wipe(request):
    if request.method == "GET":
        return JsonResponse({"status": "error", "data": {"reason": "Only post method is accepted."}})

    routing_key = "_wiper_init"

    body = json.loads(request.body.decode("utf-8"))

    message = {
        "dataset_id": body.get("dataset_id"),
    }

    publish(json.dumps(message), routing_key)

    return JsonResponse(
        {"status": "ok", "data": {"message": f"Dataset id {body.get('dataset_id')} on Pelican will be wiped"}},
        safe=False,
    )


@csrf_exempt
def dataset_progress(request, dataset_id):
    try:
        monitor = ProgressMonitorDataset.objects.values("state", "phase").get(dataset__id=dataset_id)
        return JsonResponse({"status": "ok", "data": monitor}, safe=False)
    except ProgressMonitorDataset.DoesNotExist:
        return JsonResponse({"status": "ok", "data": None}, safe=False)


@csrf_exempt
def dataset_id(request):
    if request.method == "GET":
        return JsonResponse({"status": "error", "data": {"reason": "Only post method is accepted."}})

    body = json.loads(request.body.decode("utf-8"))
    dataset_name = body.get("name")

    dataset = Dataset.objects.get(name=dataset_name)
    return JsonResponse({"status": "ok", "data": dataset.id if dataset else None}, safe=False)


@csrf_exempt
def dataset_availability(request, dataset_id):
    map = {
        "parties": ["parties.id"],
        "plannings": ["planning.budget"],
        "tenders": ["tender.id"],
        "tenderers": ["tenderers.id"],
        "tenders_items": ["tender.items.id"],
        "awards": ["awards.id"],
        "awards_items": ["awards.items.id"],
        "awards_suppliers": ["awards.suppliers.id"],
        "contracts": ["contracts.id"],
        "contracts_items": ["contracts.items.id"],
        "contracts_transactions": ["contracts.implementation.transactions.id"],
        "documents": [
            "planning.documents.id",
            "tender.documents.id",
            "awards.documents.id",
            "contracts.documents.id",
            "contracts.implementation.documents.id",
        ],
        "milestones": [
            "planning.milestones.id",
            "tender.milestones.id",
            "contracts.milestones.id",
            "contracts.implementation.milestones.id",
        ],
        "amendments": ["tender.amendments.id", "awards.amendments.id", "contract.amendments.id"],
    }

    with connections["data"].cursor() as cursor:
        statement = """
            SELECT c.key AS check, SUM(jsonb_array_length(c.value)) AS count
            FROM {table} flc, jsonb_each(flc.result->'checks') c
            WHERE dataset_id = %(dataset_id)s
                AND c.key IN %(checks)s
            GROUP BY c.key
            ORDER BY c.key
            """

        cursor.execute(
            sql.SQL(statement).format(table=sql.Identifier(FieldLevelCheck._meta.db_table)),
            {"checks": tuple(j for i in map.values() for j in i), "dataset_id": dataset_id},
        )

        results = cursor.fetchall()

        counts = {}
        for key, items in map.items():
            counts[key] = 0
            for i in items:
                for r in results:
                    if r[0] == i:
                        counts[key] += int(r[1])

    return JsonResponse({"status": "ok", "data": counts}, safe=False)


@csrf_exempt
def dataset_metadata(request, dataset_id):
    meta = Dataset.objects.values_list("meta__collection_metadata", flat=True).get(id=dataset_id)

    return JsonResponse({"status": "ok", "data": meta}, safe=False)
