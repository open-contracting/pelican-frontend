import simplejson as json
from django.db import connections
from django.db.models import Count
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from psycopg2.sql import SQL

from api.models import DataItem


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

    # See similar code in dataset_filter.py in pelican-backend.
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


# json_path requires shape: field1.field2.field3 ...
def dataset_distinct_values(request, dataset_id, json_path, sub_string=""):
    json_path = "data__" + "__".join(json_path.split("."))
    kwargs = {"dataset_id": dataset_id, json_path + "__icontains": sub_string}
    data_items_query = (
        DataItem.objects.filter(**kwargs).values(json_path).annotate(count=Count(json_path)).order_by("-count")
    )
    query_set = data_items_query.values_list(json_path, "count").distinct()[:200]
    return JsonResponse([{"value": el[0], "count": el[1]} for el in query_set], safe=False)
