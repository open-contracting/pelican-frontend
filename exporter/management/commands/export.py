import datetime
import logging

from django.core.management.base import BaseCommand
from django.db import close_old_connections
from yapw.decorators import discard
from yapw.methods import ack

from api.rabbitmq import consume
from exporter.exceptions import GoogleDriveError, TagError
from exporter.gdocs import Gdocs
from exporter.messages import DEFAULT_LANGUAGE, MESSAGES
from exporter.models import Export
from exporter.template_tags.base import base as base_tag
from exporter.views import ROUTING_KEY

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create the reports that POST api/exports/ requests, one message at a time"

    def handle(self, *args, **options):
        consume(on_message_callback=callback, queue=ROUTING_KEY, decorator=discard)


def callback(client_state, channel, method, properties, input_message):
    """Render the report, upload it to Google Drive, and record the outcome on the export."""
    # The server can close a connection while this thread waits for a message, or renders a report.
    close_old_connections()

    export = Export.objects.get(pk=input_message["export_id"])
    language = export.language if export.language in MESSAGES else DEFAULT_LANGUAGE

    gdocs = None
    try:
        gdocs = Gdocs(export.document_id)
        base = base_tag(gdocs, export.dataset_id, language)
        base.set_argument("template", export.document_id)
        base.finalize_arguments()
        content, export.failed_tags = base.validate_and_render({})

        filename = export.report_name or f"Report {export.dataset_id} {datetime.datetime.now(tz=datetime.UTC)}"

        export.file_id = gdocs.upload(export.folder_id, filename, content)
        export.status = Export.Status.OK
    except GoogleDriveError as e:
        logger.exception("Unable to export the report for dataset %s", export.dataset_id)
        export.status = Export.Status.REPORT_ERROR
        export.reason = str(e)
    except TagError as e:
        export.status = Export.Status.TEMPLATE_ERROR
        export.tag_errors = [e.as_dict()]  # Can accommodate multiple TagErrors in the future
    except Exception:
        # The frontend polls until the status changes, so an unexpected error must be recorded, too.
        logger.exception("Unable to export the report for dataset %s", export.dataset_id)
        export.status = Export.Status.REPORT_ERROR
        export.reason = "An unexpected error occurred."
    finally:
        if gdocs is not None:
            gdocs.close()

    close_old_connections()
    export.save()

    ack(client_state, channel, method.delivery_tag)
