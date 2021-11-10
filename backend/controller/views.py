import simplejson as json
from django.db import connections
from django.shortcuts import get_object_or_404
from dqt.models import Dataset, FieldLevelCheck, ProgressMonitorDataset
from psycopg2.sql import SQL, Identifier
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .rabbitmq import publish


class CreateDatasetSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="The name to assign to the dataset")
    collection_id = serializers.IntegerField(help_text="The collection ID in Kingfisher Process")


class FilterDatasetSerializer(serializers.Serializer):
    dataset_id_original = serializers.IntegerField(help_text="The ID of the dataset to filter")
    # Django REST Framework's auto-generated documentation does not render nested relationships.
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    filter_message = serializers.JSONField(help_text="The date, buyer and procuring entity filters")


class DeleteDatasetSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()


class DatasetViewSet(viewsets.GenericViewSet):
    queryset = Dataset.objects.all()
    serializer_class = CreateDatasetSerializer
    # ViewSet's don't allow typed paths like <int:pk>.
    # https://github.com/encode/django-rest-framework/pull/6789
    # https://github.com/encode/django-rest-framework/issues/6148#issuecomment-725297421
    lookup_value_regex = "[0-9]+"

    def create(self, request):
        """
        Publishes a message to RabbitMQ to create a dataset with the given `name` and `collection_id`.
        """
        serializer = self.get_serializer(
            data={
                "name": request.data.get("name"),
                "collection_id": request.data.get("collection_id"),
            }
        )
        serializer.is_valid(raise_exception=True)
        publish(json.dumps(serializer.data), "ocds_kingfisher_extractor_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["post"], serializer_class=FilterDatasetSerializer)
    def filter(self, request):
        """
        Publishes a message to RabbitMQ to create a filtered dataset with the given `dataset_id_original` and
        `filter_message`.
        """
        serializer = self.get_serializer(
            data={
                "dataset_id_original": request.data.get("dataset_id_original"),
                "filter_message": request.data.get("filter_message"),
            }
        )
        serializer.is_valid(raise_exception=True)
        publish(json.dumps(serializer.data), "dataset_filter_extractor_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        """
        Publishes a message to RabbitMQ to wipe the dataset.
        """
        # get_serializer_class() and @action(serializer_class=) can't be used together.
        # https://github.com/encode/django-rest-framework/discussions/8244
        serializer = DeleteDatasetSerializer(data={"dataset_id": pk})
        serializer.is_valid(raise_exception=True)
        publish(json.dumps(serializer.data), "wiper_init")
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=False)
    def find_by_name(self, request):
        """
        Returns the ID of the dataset with the `name` given in the query string, as an object like `{"id": 123}`,
        or `{}` if no name matches.
        """
        try:
            dataset = self.get_queryset().get(name=request.query_params.get("name"))
            return Response({"id": dataset.pk})
        except Dataset.DoesNotExist:
            return Response({})

    @action(detail=True)
    def status(self, request, pk=None):
        """
        Returns the dataset's status, or `{}` if no status is set.
        """
        self.get_object()  # trigger 404 if no dataset
        try:
            monitor = ProgressMonitorDataset.objects.values("state", "phase").get(dataset__pk=pk)
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

        mapping = {
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
            "amendments": [
                "tender.amendments.id",
                "awards.amendments.id",
                "contract.amendments.id",
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
