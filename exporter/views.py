from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from api.rabbitmq import publish
from api.util import get_permitted_dataset
from exporter.models import Export

ROUTING_KEY = "report_exporter_init"


class CreateExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Export
        fields = ["dataset_id", "document_id", "folder_id", "language", "report_name"]


class TagErrorSerializer(serializers.Serializer):
    reason = serializers.CharField(help_text="The reason the tag could not be rendered")
    full_tag = serializers.CharField(allow_null=True, help_text="The tag as extracted from the template")
    template_id = serializers.CharField(allow_null=True, help_text="The ID of the Google Docs template")


class ExportSerializer(serializers.ModelSerializer):
    tag_errors = TagErrorSerializer(many=True, read_only=True)
    failed_tags = serializers.ListField(
        child=serializers.CharField(), read_only=True, help_text="The tags that could not be rendered"
    )

    class Meta:
        model = Export
        fields = ["id", "status", "file_id", "reason", "tag_errors", "failed_tags"]
        read_only_fields = fields


class ExportViewSet(viewsets.GenericViewSet):
    serializer_class = ExportSerializer
    lookup_value_converter = "int"

    def get_queryset(self):
        """Return the user's own exports. Another user's export is 404, whoever requested it."""
        return Export.objects.filter(user=self.request.user)

    # https://github.com/encode/django-rest-framework/blob/2db0c0b/rest_framework/mixins.py#L51
    @extend_schema(responses=ExportSerializer)
    def retrieve(self, request, *args, **kwargs):
        """
        Return the export, whose ``status`` is ``waiting`` until the report is created.

        A created report has a ``file_id``, and might have ``failed_tags``. Otherwise, the ``status`` is
        ``report_error``, with a ``reason``, or ``template_error``, with ``tag_errors``.
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @extend_schema(request=CreateExportSerializer, responses={202: ExportSerializer})
    def create(self, request):
        """Publish a message to RabbitMQ to create a report in Google Docs, and return the export to poll."""
        serializer = CreateExportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        get_permitted_dataset(request.user, serializer.validated_data["dataset_id"])

        export = serializer.save(user=request.user)
        publish({"export_id": export.pk}, ROUTING_KEY)
        return Response(ExportSerializer(export).data, status=status.HTTP_202_ACCEPTED)
