import simplejson as json
from django.db import connections
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dqt.models import Dataset, FieldLevelCheck, ProgressMonitorDataset
from psycopg2.sql import SQL, Identifier

from .rabbitmq import publish


@csrf_exempt
def create_dataset_filter(request):
    if request.method == "GET":
        return HttpResponseBadRequest(reason="Only post method is accepted.")

    publish(request.body, "_dataset_filter_extractor_init")

    return HttpResponse("done")


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
            SQL(statement).format(table=Identifier(FieldLevelCheck._meta.db_table)),
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
