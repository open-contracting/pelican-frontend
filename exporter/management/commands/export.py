import datetime
import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from yapw.methods import ack

from api.rabbitmq import consume, decorator
from exporter import exceptions
from exporter.gdocs import Gdocs
from exporter.messages import DEFAULT_LANGUAGE, MESSAGES
from exporter.models import Export, ExportError
from exporter.template_tags.base import base as base_tag
from exporter.views import ROUTING_KEY

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create the reports that POST api/exports/ requests"

    def handle(self, *args, **options):
        consume(on_message_callback=callback, queue=ROUTING_KEY, decorator=decorator)


def callback(client_state, channel, method, properties, input_message):
    """Render the template, upload the document to Google Drive, and record the result."""
    export = Export.objects.get(pk=input_message["export_id"])
    language = export.language if export.language in MESSAGES else DEFAULT_LANGUAGE

    errors = []
    gdocs = None
    try:
        gdocs = Gdocs(export.template_id)
        base = base_tag(gdocs, export.dataset_id, language)
        base.set_argument("template", export.template_id)
        base.finalize_arguments()
        content, export.failed_checks = base.validate_and_render({})

        filename = export.name or f"Report {export.dataset_id} {datetime.datetime.now(tz=datetime.UTC)}"

        export.document_id = gdocs.upload(export.folder_id, filename, content)
        export.status = Export.Status.OK
    except exceptions.TagError as e:
        export.status = Export.Status.TEMPLATE_ERROR
        # Can accommodate multiple TagErrors in the future. The tag and template are unknown for some errors.
        errors = [ExportError(export=export, reason=e.reason, tag=e.full_tag or "", template_id=e.template_id or "")]
    except exceptions.GoogleDriveError as e:
        logger.exception("Unable to export the report for dataset %s", export.dataset_id)
        export.status = Export.Status.ERROR
        export.reason = str(e)
    except Exception:  # handle, instead of deferring to the decorator, to make the frontend stop polling
        logger.exception("Unable to export the report for dataset %s", export.dataset_id)
        export.status = Export.Status.ERROR
        export.reason = "An unexpected error occurred."
    finally:
        if gdocs is not None:
            gdocs.close()

    with transaction.atomic():
        export.save()
        ExportError.objects.bulk_create(errors)

    ack(client_state, channel, method.delivery_tag)
