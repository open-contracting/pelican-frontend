import time

import simplejson as json
from django.conf import settings
from django.db import connections
from django.db.models import Count, F, OuterRef, Subquery
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from psycopg2.sql import SQL, Identifier
from rest_framework import mixins, serializers, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import (
    DataItem,
    Dataset,
    DatasetFilter,
    DatasetLevelCheck,
    FieldLevelCheck,
    FieldLevelCheckExamples,
    ProgressMonitorDataset,
    Report,
    ResourceLevelCheckExamples,
    TimeVarianceLevelCheck,
)
from api.rabbitmq import publish


@csrf_exempt
def app_settings(request):
    return JsonResponse(
        {
            "user": settings.GOOGLE_DRIVE_USER,
            "template": {
                "en": settings.GDOCS_TEMPLATES["DEFAULT_BASE_TEMPLATE"],
                "es": settings.GDOCS_TEMPLATES["DEFAULT_BASE_TEMPLATE_ES"],
            },
            "folder": settings.GOOGLE_DRIVE_FOLDER,
        },
    )


@csrf_exempt
def dataset_filter_items(request):
    if request.method == "GET":
        return HttpResponseBadRequest(reason="Only POST method is accepted.")

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
        parts.append("data->'buyer'->>'name' ILIKE %(buyer_regex)s")

    if "procuring_entity" in filter_message:
        variables["procuring_entity"] = tuple(
            procuring_entity for procuring_entity in filter_message["procuring_entity"]
        )
        parts.append("data->'tender'->'procuringEntity'->>'name' IN %(procuring_entity)s")

    if "procuring_entity_regex" in filter_message:
        variables["procuring_entity_regex"] = filter_message["procuring_entity_regex"]
        parts.append("data->'tender'->'procuringEntity'->>'name' ILIKE %(procuring_entity_regex)s")

    with connections["pelican_backend"].cursor() as cursor:
        cursor.execute(SQL(" AND ".join(parts)), variables)
        items = cursor.fetchall()[0][0]

    return JsonResponse({"items": items})


# field is in the format: tender.procuringEntity.name
def dataset_distinct_values(request, dataset_id, field, query=""):
    lookup = "data__" + "__".join(field.split("."))
    kwargs = {"dataset_id": dataset_id, f"{lookup}__icontains": query}
    data_items_query = (
        DataItem.objects.filter(**kwargs).values(lookup).annotate(count=Count(lookup)).order_by("-count")
    )
    query_set = data_items_query.values_list(lookup, "count").distinct()[:200]
    return JsonResponse([{"value": el[0], "count": el[1]} for el in query_set], safe=False)


class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = ["id", "data"]


class DatasetSerializer(serializers.ModelSerializer):
    phase = serializers.CharField()
    state = serializers.CharField()
    parent_id = serializers.IntegerField()
    parent_name = serializers.CharField()
    filter_message = serializers.JSONField()

    class Meta:
        model = Dataset
        fields = [
            "id",
            "name",
            "meta",
            "ancestor_id",
            "created",
            "modified",
            "phase",
            "state",
            "parent_id",
            "parent_name",
            "filter_message",
        ]


class StatusSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=ProgressMonitorDataset.State.choices)
    phase = serializers.ChoiceField(choices=ProgressMonitorDataset.Phase.choices)


class CreateDatasetSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="The name to assign to the dataset")
    collection_id = serializers.IntegerField(help_text="The compiled collection ID in Kingfisher Process")
    ancestor_id = serializers.IntegerField(
        required=False, help_text="The ID of the previous report in Pelican, for time-based checks"
    )
    max_items = serializers.IntegerField(
        required=False, help_text="The number of compiled releases to import from Kingfisher Process"
    )


class FilterDatasetSerializer(serializers.Serializer):
    release_date_from = serializers.CharField(required=False, help_text="The minimum release date (YYYY-MM-DD)")
    release_date_to = serializers.CharField(required=False, help_text="The maximum release date (YYYY-MM-DD)")
    buyer = serializers.ListField(required=False, child=serializers.CharField(), help_text="Names of buyers")
    buyer_regex = serializers.CharField(required=False, help_text="A SQL ILIKE pattern for the buyer's name")
    procuring_entity = serializers.ListField(
        required=False, child=serializers.CharField(), help_text="Names of procuring entities"
    )
    procuring_entity_regex = serializers.CharField(
        required=False, help_text="A SQL ILIKE pattern for the procuring entity's name"
    )


class DataItemViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Return OCDS data that passed or failed a check."""

    queryset = DataItem.objects.all()
    serializer_class = DataItemSerializer
    lookup_value_converter = "int"


class DatasetViewSet(viewsets.ViewSet):
    lookup_value_converter = "int"

    def get_queryset(self):
        return Dataset.objects.all()

    def get_annotated_queryset(self):
        dataset_filter = DatasetFilter.objects.filter(dataset=OuterRef("pk"))[:1]
        return Dataset.objects.annotate(
            phase=F("progress__phase"),
            state=F("progress__state"),
            parent_id=Subquery(dataset_filter.values("parent__id")),
            parent_name=Subquery(dataset_filter.values("parent__name")),
            filter_message=Subquery(dataset_filter.values("filter_message")),
        )

    def get_object_or_404(self, queryset):
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def get_object(self):
        return self.get_object_or_404(self.get_queryset())

    def get_annotated_object(self):
        return self.get_object_or_404(self.get_annotated_queryset())

    def get_report(self, model, fields):
        return Response(
            {
                check.check_name: {field: getattr(check, field) for field in fields}
                for check in model.objects.filter(dataset=self.kwargs["pk"])
            }
        )

    # https://github.com/encode/django-rest-framework/blob/2db0c0b/rest_framework/mixins.py#L35
    @extend_schema(responses=DatasetSerializer)
    def list(self, request, *args, **kwargs):
        """Return all datasets with their status and filter metadata."""
        queryset = self.get_annotated_queryset()
        serializer = DatasetSerializer(queryset, many=True)
        return Response(serializer.data)

    # https://github.com/encode/django-rest-framework/blob/2db0c0b/rest_framework/mixins.py#L51
    @extend_schema(responses=DatasetSerializer)
    def retrieve(self, request, *args, **kwargs):
        """Return the dataset with its status and filter metadata."""
        instance = self.get_annotated_object()
        serializer = DatasetSerializer(instance)
        return Response(serializer.data)

    @extend_schema(request=CreateDatasetSerializer, responses={202: None, 404: {"type": "string"}})
    def create(self, request):
        """Publish a message to RabbitMQ to create a dataset."""
        serializer = CreateDatasetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        collection_id = serializer.data["collection_id"]
        with connections["kingfisher_process"].cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM compiled_release WHERE collection_id = %(id)s)",
                {"id": collection_id},
            )
            if not cursor.fetchone()[0]:
                return Response(
                    f"collection_id {collection_id} matches no compiled_release rows",
                    status=status.HTTP_404_NOT_FOUND,
                )

        if (ancestor_id := serializer.data.get("ancestor_id")) and not Dataset.objects.filter(pk=ancestor_id).exists():
            return Response(
                f"ancestor_id {ancestor_id} matches no Pelican reports",
                status=status.HTTP_404_NOT_FOUND,
            )

        message = {
            "name": serializer.data["name"],
            "collection_id": collection_id,
            "ancestor_id": ancestor_id,
            "max_items": serializer.data.get("max_items"),
        }
        publish(message, "ocds_kingfisher_extractor_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    @extend_schema(request=FilterDatasetSerializer, responses={202: None})
    @action(detail=True, methods=["post"])
    def filter(self, request, pk=None):
        """Publish a message to RabbitMQ to create a filtered dataset."""
        serializer = FilterDatasetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = {"dataset_id_original": pk, "filter_message": serializer.data}
        publish(message, "dataset_filter_extractor_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    @extend_schema(responses={202: None})
    def destroy(self, request, pk=None):
        """Publish a message to RabbitMQ to wipe the dataset."""
        publish({"dataset_id": pk}, "wiper_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    @extend_schema(responses={200: {"type": "object", "properties": {"id": {"type": "integer"}}}})
    @action(detail=False)
    def find_by_name(self, request):
        """
        Return the ID of the dataset with the name given in the `name` query string parameter, as an object.

        ``{"id": 123}`` for example, or ``{}`` if no name matches.
        """
        try:
            dataset = self.get_queryset().get(name=request.query_params.get("name"))
            return Response({"id": dataset.pk})
        except Dataset.DoesNotExist:
            return Response({})

    @extend_schema(responses={200: {"type": "object"}})
    @action(detail=True)
    def field_level_report(self, request, pk=None):
        """Return a report of the dataset's field-level checks."""
        return Response(get_object_or_404(Report, dataset=pk, type="field_level_check").data)

    @extend_schema(responses={200: {"type": "object"}})
    @action(detail=True)
    def compiled_release_level_report(self, request, pk=None):
        """Return a report of the dataset's compiled release-level checks."""
        return Response(get_object_or_404(Report, dataset=pk, type="resource_level_check").data)

    @extend_schema(responses={200: {"type": "object"}})
    @action(detail=True)
    def dataset_level_report(self, request, pk=None):
        """Return a report of the dataset's dataset-level checks."""
        return self.get_report(
            DatasetLevelCheck,
            [
                "result",
                "value",
                "meta",
            ],
        )

    @extend_schema(responses={200: {"type": "object"}})
    @action(detail=True)
    def time_based_report(self, request, pk=None):
        """Return a report of the dataset's time-based checks."""
        return self.get_report(
            TimeVarianceLevelCheck,
            [
                "coverage_value",
                "coverage_result",
                "check_value",
                "check_result",
                "meta",
            ],
        )

    @extend_schema(responses=StatusSerializer)
    @action(detail=True)
    def status(self, request, pk=None):
        """Return the dataset's status, as an object like `{"phase": "CHECKED", "state": "OK"}`, or `{}` if not set."""
        try:
            progress = self.get_object_or_404(self.get_queryset().select_related("progress")).progress
            return Response({"phase": progress.phase, "state": progress.state})
        except ProgressMonitorDataset.DoesNotExist:
            return Response({})

    @extend_schema(responses={200: {"type": "object"}})
    @action(detail=True)
    def metadata(self, request, pk=None):
        """Return the dataset's collection metadata."""
        meta = self.get_object_or_404(self.get_queryset().values_list("meta__collection_metadata", flat=True))
        return Response(meta or {})

    @extend_schema(responses={200: {"type": "object"}})
    @action(detail=True)
    def coverage(self, request, pk=None):
        """Return the dataset's coverage statistics."""
        self.get_object()  # trigger 404 if no dataset

        # The lists of fields must match the names of field-level checks in pelican-backend.
        mapping = {
            "parties": ["parties.id"],
            "plannings": ["planning.budget"],
            "tenders": ["tender.id"],
            "tenderers": ["tender.tenderers.id"],
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
            "amendments": [
                "tender.amendments.id",
                "awards.amendments.id",
                "contracts.amendments.id",
            ],
        }

        with connections["pelican_backend"].cursor() as cursor:
            statement = """
                SELECT c.key AS check, SUM(jsonb_array_length(c.value)) AS count
                FROM {table} flc, jsonb_each(flc.result->'checks') c
                WHERE dataset_id = %(dataset_id)s AND c.key IN %(checks)s
                GROUP BY c.key
                ORDER BY c.key
                """

            cursor.execute(
                SQL(statement).format(table=Identifier(FieldLevelCheck._meta.db_table)),
                {"checks": tuple(j for i in mapping.values() for j in i), "dataset_id": pk},
            )

            results = cursor.fetchall()

            counts = {}
            for key, items in mapping.items():
                counts[key] = 0
                for i in items:
                    for result in results:
                        if result[0] == i:
                            counts[key] += int(result[1])

        return Response(counts)


class FieldLevelDetail(views.APIView):
    @extend_schema(responses={200: {"type": "object"}})
    def get(self, request, pk, name, format=None):
        """Return a report and examples of one field-level check."""
        start_time = time.time()

        detail = get_object_or_404(Report, dataset=pk, type="field_level_check", data__has_key=name).data[name]
        data = get_object_or_404(FieldLevelCheckExamples, dataset=pk, path=name).data

        for key in ("coverage", "quality"):
            detail[key]["passed_examples"] = data[key]["passed_examples"]
            detail[key]["failed_examples"] = data[key]["failed_examples"]
            for check_name, check in data[key]["checks"].items():
                detail[key]["checks"][check_name]["passed_examples"] = check["passed_examples"]
                detail[key]["checks"][check_name]["failed_examples"] = check["failed_examples"]

        detail["time"] = time.time() - start_time

        return Response(detail)


class ResourceLevelDetail(views.APIView):
    @extend_schema(responses={200: {"type": "object"}})
    def get(self, request, pk, name, format=None):
        """Return a report and examples of one compiled release-level check."""
        start_time = time.time()

        detail = get_object_or_404(Report, dataset=pk, type="resource_level_check", data__has_key=name).data[name]
        data = get_object_or_404(ResourceLevelCheckExamples, dataset=pk, check_name=name).data

        detail.update(data)

        detail["time"] = time.time() - start_time

        return Response(detail)
