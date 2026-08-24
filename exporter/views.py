import datetime
import logging

from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema
from rest_framework import serializers, views
from rest_framework.response import Response

from api.util import get_permitted_dataset
from exporter.exceptions import GoogleDriveError, TagError
from exporter.gdocs import Gdocs
from exporter.messages import DEFAULT_LANGUAGE, MESSAGES
from exporter.template_tags.base import base as base_tag

logger = logging.getLogger(__name__)


class GenerateReportSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField(help_text="The dataset's ID")
    document_id = serializers.CharField(allow_blank=True, help_text="The ID of the Google Docs template")
    folder_id = serializers.CharField(
        allow_blank=True, help_text="The ID of the Google Drive folder in which to create the report"
    )
    language = serializers.CharField(
        required=False, allow_blank=True, help_text="The report's language, defaulting to English"
    )
    report_name = serializers.CharField(
        required=False, allow_blank=True, help_text="The report's filename, defaulting to a generated name"
    )


class ReportFileSerializer(serializers.Serializer):
    file_id = serializers.CharField(help_text="The ID of the Google Docs report")


class ReportReasonSerializer(serializers.Serializer):
    reason = serializers.CharField(help_text="The reason the report could not be created")


class TagErrorSerializer(serializers.Serializer):
    reason = serializers.CharField(help_text="The reason the tag could not be rendered")
    full_tag = serializers.CharField(allow_null=True, help_text="The tag as extracted from the template")
    template_id = serializers.CharField(allow_null=True, help_text="The ID of the Google Docs template")


class GeneratedReportSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["ok"])
    data = ReportFileSerializer()
    failed_tags = serializers.ListField(child=serializers.CharField(), help_text="The tags that could not be rendered")


class ReportErrorSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["report_error"])
    data = ReportReasonSerializer()


class TemplateErrorSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["template_error"])
    data = TagErrorSerializer(many=True)
    failed_tags = serializers.ListField(child=serializers.CharField(), help_text="The tags that could not be rendered")


class GenerateReport(views.APIView):
    @extend_schema(
        request=GenerateReportSerializer,
        responses={
            200: PolymorphicProxySerializer(
                component_name="GenerateReportResponse",
                serializers=[GeneratedReportSerializer, ReportErrorSerializer, TemplateErrorSerializer],
                resource_type_field_name=None,
            )
        },
    )
    def post(self, request, format=None):
        """
        Create a report in Google Docs, and return its file ID.

        The response is 200 whether or not the report was created. Its ``status`` is ``ok``, ``report_error`` if
        the report could not be created, or ``template_error`` if the template could not be rendered.
        """
        serializer = GenerateReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "report_error", "data": {"reason": "Input message is malformed, will be dropped."}}
            )

        input_message = serializer.validated_data

        get_permitted_dataset(request.user, input_message["dataset_id"])

        if "language" in input_message and input_message["language"] in MESSAGES:
            language = input_message["language"]
        else:
            language = DEFAULT_LANGUAGE

        document_id = input_message["document_id"].strip()
        folder_id = input_message["folder_id"].strip()

        gdocs = None

        failed_tags = []
        try:
            gdocs = Gdocs(document_id)
            base = base_tag(gdocs, input_message["dataset_id"], language)
            base.set_argument("template", document_id)
            base.finalize_arguments()
            content, failed_tags = base.validate_and_render({})

            if "report_name" in input_message:
                filename = input_message["report_name"]
            else:
                filename = f"Report {input_message['dataset_id']} {datetime.datetime.now(tz=datetime.UTC)}"

            file_id = gdocs.upload(folder_id, filename, content)

            response = Response({"status": "ok", "data": {"file_id": file_id}, "failed_tags": failed_tags})
        except GoogleDriveError as e:
            logger.exception("Unable to export the report for dataset %s", input_message["dataset_id"])
            response = Response({"status": "report_error", "data": {"reason": str(e)}})
        except TagError as e:
            response = Response(
                {
                    "status": "template_error",
                    "data": [e.as_dict()],  # Can accommodate multiple TagErrors in the future
                    "failed_tags": failed_tags,
                }
            )
        finally:
            if gdocs is not None:
                gdocs.close()

        return response
