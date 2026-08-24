import time

from django.conf import settings
from django.db import connections
from django.db.models import Count, F, OuterRef, Subquery
from django.http import HttpResponseBadRequest, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from psycopg.sql import SQL
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Profile
from api.models import (
    DataItem,
    Dataset,
    DatasetFilter,
    DatasetLevelCheck,
    FieldLevelCheckExamples,
    Report,
    ResourceLevelCheckExamples,
    TimeVarianceLevelCheck,
)
from api.rabbitmq import publish
from api.serializers import (
    CountDatasetFilterItemsSerializer,
    CreateDatasetSerializer,
    DataItemSerializer,
    DatasetLevelReportSerializer,
    DatasetSerializer,
    DistinctValueSerializer,
    FieldLevelCheckDetailSerializer,
    FieldLevelReportSerializer,
    FilterDatasetSerializer,
    ResourceLevelCheckDetailSerializer,
    ResourceLevelReportSerializer,
    SettingsSerializer,
    TimeVarianceLevelReportSerializer,
    UserSettingsSerializer,
)
from api.util import get_permitted_dataset, permitted_datasets


class DataItemViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Return OCDS data that passed or failed a check."""

    serializer_class = DataItemSerializer
    lookup_value_converter = "int"

    def get_queryset(self):
        return DataItem.objects.filter(dataset__in=permitted_datasets(self.request.user))


class DatasetViewSet(viewsets.ViewSet):
    lookup_value_converter = "int"

    def get_permissions(self):
        if self.action in {"create", "destroy"}:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        return permitted_datasets(self.request.user)

    def get_annotated_queryset(self):
        dataset_filter = DatasetFilter.objects.filter(dataset=OuterRef("pk"))[:1]
        return self.get_queryset().annotate(
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
                for check in model.objects.filter(dataset__in=self.get_queryset(), dataset=self.kwargs["pk"])
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
        get_permitted_dataset(request.user, pk)

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

    @extend_schema(responses=FieldLevelReportSerializer)
    @action(detail=True)
    def field_level_report(self, request, pk=None):
        """Return a report of the dataset's field-level checks, by field path."""
        return Response(
            get_object_or_404(Report, dataset__in=self.get_queryset(), dataset=pk, type="field_level_check").data
        )

    @extend_schema(responses=ResourceLevelReportSerializer)
    @action(detail=True)
    def compiled_release_level_report(self, request, pk=None):
        """Return a report of the dataset's compiled release-level checks, by check name."""
        return Response(
            get_object_or_404(Report, dataset__in=self.get_queryset(), dataset=pk, type="resource_level_check").data
        )

    @extend_schema(responses=DatasetLevelReportSerializer)
    @action(detail=True)
    def dataset_level_report(self, request, pk=None):
        """Return a report of the dataset's dataset-level checks, by check name."""
        return self.get_report(
            DatasetLevelCheck,
            [
                "result",
                "value",
                "meta",
            ],
        )

    @extend_schema(responses=TimeVarianceLevelReportSerializer)
    @action(detail=True)
    def time_based_report(self, request, pk=None):
        """Return a report of the dataset's time-based checks, by check name."""
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


class FieldLevelDetail(views.APIView):
    @extend_schema(responses=FieldLevelCheckDetailSerializer)
    def get(self, request, pk, name, format=None):
        """Return a report and examples of one field-level check."""
        start_time = time.time()

        detail = get_object_or_404(
            Report,
            dataset__in=permitted_datasets(request.user),
            dataset=pk,
            type="field_level_check",
            data__has_key=name,
        ).data[name]
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
    @extend_schema(responses=ResourceLevelCheckDetailSerializer)
    def get(self, request, pk, name, format=None):
        """Return a report and examples of one compiled release-level check."""
        start_time = time.time()

        detail = get_object_or_404(
            Report,
            dataset__in=permitted_datasets(request.user),
            dataset=pk,
            type="resource_level_check",
            data__has_key=name,
        ).data[name]
        data = get_object_or_404(ResourceLevelCheckExamples, dataset=pk, check_name=name).data

        detail.update(data)

        detail["time"] = time.time() - start_time

        return Response(detail)


def failures_response(filename, statement, variables):
    def rows():
        with connections["pelican_backend"].chunked_cursor() as cursor:
            cursor.execute(statement, variables)
            while batch := cursor.fetchmany(1000):
                for row in batch:
                    yield f"{row[0]}\n"

    return StreamingHttpResponse(
        rows(),
        content_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


class FieldLevelFailures(views.APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("type", description="The type of check", enum=["coverage", "quality"], default="quality"),
        ],
        responses={(200, "text/plain"): {"type": "string"}},
    )
    def get(self, request, pk, name, format=None):
        """Return, one OCID per line, the compiled releases failing the field-level check."""
        get_object_or_404(
            Report,
            dataset__in=permitted_datasets(request.user),
            dataset=pk,
            type="field_level_check",
            data__has_key=name,
        )

        type = request.query_params.get("type", "quality")
        if type not in {"coverage", "quality"}:
            return HttpResponseBadRequest(reason="type must be either 'coverage' or 'quality'.")

        return failures_response(
            f"dataset_{pk}_{name}_{type}_failures.txt",
            """
            SELECT result->'meta'->>'ocid'
            FROM field_level_check
            WHERE dataset_id = %(dataset_id)s
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements(result->'checks'->%(path)s) AS occurrence
                    WHERE (occurrence->%(type)s->>'overall_result')::boolean IS FALSE
                )
            ORDER BY 1
            """,
            {"dataset_id": pk, "path": name, "type": type},
        )


class ResourceLevelFailures(views.APIView):
    @extend_schema(responses={(200, "text/plain"): {"type": "string"}})
    def get(self, request, pk, name, format=None):
        """Return, one OCID per line, the compiled releases failing the compiled release-level check."""
        get_object_or_404(
            Report,
            dataset__in=permitted_datasets(request.user),
            dataset=pk,
            type="resource_level_check",
            data__has_key=name,
        )

        return failures_response(
            f"dataset_{pk}_{name}_failures.txt",
            """
            SELECT result->'meta'->>'ocid'
            FROM resource_level_check
            WHERE dataset_id = %(dataset_id)s
                AND (result->'checks'->%(name)s->>'result')::boolean IS FALSE
            ORDER BY 1
            """,
            {"dataset_id": pk, "name": name},
        )


class CountDatasetFilterItems(views.APIView):
    @extend_schema(
        request=CountDatasetFilterItemsSerializer,
        responses={200: {"type": "object", "properties": {"items": {"type": "integer"}}}},
    )
    def post(self, request, format=None):
        """
        Return the number of data items that the filter matches, as an object.

        ``{"items": 123}`` for example.
        """
        serializer = CountDatasetFilterItemsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filter_message = serializer.validated_data["filter_message"]

        dataset = get_permitted_dataset(request.user, serializer.validated_data["dataset_id_original"])

        # See similar code in dataset_filter.py in pelican-backend.
        variables = {"dataset_id_original": dataset.pk}
        parts = ["SELECT count(*) FROM data_item WHERE dataset_id = %(dataset_id_original)s"]

        if "release_date_from" in filter_message:
            variables["release_date_from"] = filter_message["release_date_from"]
            parts.append("data->>'date' >= %(release_date_from)s")

        if "release_date_to" in filter_message:
            variables["release_date_to"] = filter_message["release_date_to"]
            parts.append("data->>'date' <= %(release_date_to)s")

        if "buyer" in filter_message:
            variables["buyer"] = filter_message["buyer"]
            parts.append("data->'buyer'->>'name' = ANY(%(buyer)s)")

        if "buyer_regex" in filter_message:
            variables["buyer_regex"] = filter_message["buyer_regex"]
            parts.append("data->'buyer'->>'name' ILIKE %(buyer_regex)s")

        if "procuring_entity" in filter_message:
            variables["procuring_entity"] = filter_message["procuring_entity"]
            parts.append("data->'tender'->'procuringEntity'->>'name' = ANY(%(procuring_entity)s)")

        if "procuring_entity_regex" in filter_message:
            variables["procuring_entity_regex"] = filter_message["procuring_entity_regex"]
            parts.append("data->'tender'->'procuringEntity'->>'name' ILIKE %(procuring_entity_regex)s")

        with connections["pelican_backend"].cursor() as cursor:
            cursor.execute(SQL(" AND ".join(parts)), variables)
            items = cursor.fetchall()[0][0]

        return Response({"items": items})


def distinct_values_response(user, dataset_id, field, query):
    get_permitted_dataset(user, dataset_id)

    lookup = "data__" + "__".join(field.split("."))
    kwargs = {"dataset_id": dataset_id, f"{lookup}__icontains": query}
    data_items_query = (
        DataItem.objects.filter(**kwargs).values(lookup).annotate(count=Count(lookup)).order_by("-count")
    )
    query_set = data_items_query.values_list(lookup, "count").distinct()[:200]
    return Response([{"value": value, "count": count} for value, count in query_set])


# The field is in dot notation, like tender.procuringEntity.name.
class DatasetDistinctValues(views.APIView):
    @extend_schema(operation_id="dataset_distinct_values", responses=DistinctValueSerializer(many=True))
    def get(self, request, dataset_id, field, format=None):
        """Return the field's 200 most common values, with their counts, in descending order."""
        return distinct_values_response(request.user, dataset_id, field, "")


class DatasetDistinctValuesSearch(views.APIView):
    @extend_schema(operation_id="dataset_distinct_values_search", responses=DistinctValueSerializer(many=True))
    def get(self, request, dataset_id, field, query, format=None):
        """Return the field's 200 most common values containing the query, with their counts, in descending order."""
        return distinct_values_response(request.user, dataset_id, field, query)


class AppSettings(views.APIView):
    @extend_schema(responses=SettingsSerializer)
    def get(self, request, format=None):
        """Return the reader's own settings, and the settings that the frontend needs in order to generate a report."""
        profile = Profile.objects.filter(user=request.user).first()
        return Response(
            {
                "username": request.user.username,
                "language": profile.language if profile else "",
                "user": settings.GOOGLE_DRIVE_USER,
                "template": {
                    "en": settings.GDOCS_TEMPLATES["DEFAULT_BASE_TEMPLATE"],
                    "es": settings.GDOCS_TEMPLATES["DEFAULT_BASE_TEMPLATE_ES"],
                },
                # Only staff can write to GOOGLE_DRIVE_FOLDER. Non-staff must share a folder with the service account.
                "folder": settings.GOOGLE_DRIVE_FOLDER if request.user.is_staff else "",
            }
        )

    @extend_schema(request=UserSettingsSerializer, responses=UserSettingsSerializer)
    def patch(self, request, format=None):
        """Update the reader's own settings, which follow them between browsers."""
        serializer = UserSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Profile.objects.update_or_create(user=request.user, defaults=serializer.validated_data)
        return Response(serializer.data)
