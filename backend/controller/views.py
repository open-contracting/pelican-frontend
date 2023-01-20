from django.db import connections
from django.db.models import F, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from psycopg2.sql import SQL, Identifier
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from api.models import DataItem, Dataset, DatasetFilter, FieldLevelCheck, ProgressMonitorDataset
from controller.rabbitmq import publish


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


class CreateDatasetSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="The name to assign to the dataset")
    collection_id = serializers.IntegerField(help_text="The collection ID in Kingfisher Process")


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


# https://www.django-rest-framework.org/api-guide/schemas/
# https://www.django-rest-framework.org/coreapi/schemas/
class CustomSchema(AutoSchema):
    def get_responses(self, path, method):
        responses = super().get_responses(path, method)
        # POST requests return HTTP 202 with no content (not 201).
        if "201" in responses:
            responses["202"] = responses.pop("201")
            del responses["202"]["content"]
        # GET requests return a JSON object (not string).
        elif "200" in responses:
            responses["200"]["content"]["application/json"]["schema"] = {"type": "object"}
        return responses


class DataItemViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_value_regex = "[0-9]+"
    queryset = DataItem.objects.all()
    serializer_class = DataItemSerializer


class DatasetViewSet(viewsets.ViewSet):
    schema = CustomSchema()
    # ViewSet's don't allow typed paths like <int:pk> until next version (> 3.14.0).
    # https://github.com/encode/django-rest-framework/pull/6789
    # https://github.com/encode/django-rest-framework/issues/6148#issuecomment-725297421
    lookup_value_regex = "[0-9]+"

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

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])

    def get_annotated_object(self):
        return get_object_or_404(self.get_annotated_queryset(), pk=self.kwargs["pk"])

    def get_serializer(self, *args, **kwargs):
        if self.action in ("list", "retrieve"):
            return DatasetSerializer(*args, **kwargs)
        elif self.action == "create":
            return CreateDatasetSerializer(*args, **kwargs)
        elif self.action == "filter":
            return FilterDatasetSerializer(*args, **kwargs)

    # https://github.com/encode/django-rest-framework/blob/2db0c0b/rest_framework/mixins.py#L35
    def list(self, request, *args, **kwargs):
        queryset = self.get_annotated_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # https://github.com/encode/django-rest-framework/blob/2db0c0b/rest_framework/mixins.py#L51
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_annotated_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request):
        """
        Publishes a message to RabbitMQ to create a dataset.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = {"name": serializer.data["name"], "collection_id": serializer.data["collection_id"]}
        publish(message, "ocds_kingfisher_extractor_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def filter(self, request, pk=None):
        """
        Publishes a message to RabbitMQ to create a filtered dataset.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = {"dataset_id_original": int(pk), "filter_message": serializer.data}
        publish(message, "dataset_filter_extractor_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        """
        Publishes a message to RabbitMQ to wipe the dataset.
        """
        publish({"dataset_id": int(pk)}, "wiper_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=False)
    def find_by_name(self, request):
        """
        Returns the ID of the dataset with the name given in the `name` query string parameter, as an object like
        `{"id": 123}`, or `{}` if no name matches.
        """
        try:
            dataset = self.get_queryset().get(name=request.query_params.get("name"))
            return Response({"id": dataset.pk})
        except Dataset.DoesNotExist:
            return Response({})

    @action(detail=True)
    def status(self, request, pk=None):
        """
        Returns the dataset's status, as an object like `{"phase": "CHECKED", "state": "OK"}`, or `{}` if not set.
        """
        self.get_object()  # trigger 404 if no dataset
        try:
            monitor = ProgressMonitorDataset.objects.values("phase", "state").get(dataset__pk=pk)
            return Response(monitor)
        except ProgressMonitorDataset.DoesNotExist:
            return Response({})

    @action(detail=True)
    def metadata(self, request, pk=None):
        """
        Returns the dataset's collection metadata.
        """
        meta = get_object_or_404(self.get_queryset().values_list("meta__collection_metadata", flat=True), pk=pk)
        return Response(meta or {})

    @action(detail=True)
    def coverage(self, request, pk=None):
        """
        Returns the dataset's coverage statistics.
        """
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
                {"checks": tuple(j for i in mapping.values() for j in i), "dataset_id": pk},
            )

            results = cursor.fetchall()

            counts = {}
            for key, items in mapping.items():
                counts[key] = 0
                for i in items:
                    for r in results:
                        if r[0] == i:
                            counts[key] += int(r[1])

        return Response(counts)
