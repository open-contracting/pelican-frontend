from unittest.mock import Mock, patch

from exporter.exceptions import GoogleDriveError, TagError
from exporter.management.commands.export import callback
from exporter.models import Export
from tests import PelicanTestCase

MODULE = "exporter.management.commands.export"


class ExportTests(PelicanTestCase):
    def setUp(self):
        super().setUp()
        self.ack = self.enterContext(patch(f"{MODULE}.ack"))
        self.gdocs = self.enterContext(patch(f"{MODULE}.Gdocs"))
        self.base_tag = self.enterContext(patch(f"{MODULE}.base_tag"))
        self.base_tag.return_value.validate_and_render.return_value = ("content", [])
        self.gdocs.return_value.upload.return_value = "file"
        self.export = self.create(
            Export, user=self.user, dataset_id=1, template_id="template", folder_id="folder", language="es"
        )

    def run_callback(self):
        """Run the callback and reload the export. The message is acked, whatever the outcome."""
        callback(Mock(), Mock(), Mock(delivery_tag=1), Mock(), {"export_id": self.export.pk})
        self.export.refresh_from_db()
        self.ack.assert_called_once()

    def assert_export(self, status, *, document_id="", reason="", errors=(), failed_checks=()):
        """Assert the export's result. Each field is empty by default, so a test states only what it expects."""
        self.assertEqual(self.export.status, status)
        self.assertEqual(self.export.document_id, document_id)
        self.assertEqual(self.export.reason, reason)
        self.assertEqual(list(self.export.errors.values("reason", "tag", "template_id")), list(errors))
        self.assertEqual(self.export.failed_checks, list(failed_checks))

    def test_ok(self):
        self.base_tag.return_value.validate_and_render.return_value = ("content", ["distribution.tender_value"])

        self.run_callback()

        self.assert_export(Export.Status.OK, document_id="file", failed_checks=["distribution.tender_value"])
        self.gdocs.assert_called_once_with("template")
        self.base_tag.assert_called_once_with(self.gdocs.return_value, 1, "es")
        self.gdocs.return_value.close.assert_called_once_with()

    def test_default_language(self):
        self.export.language = "xx"
        self.export.save()

        self.run_callback()

        self.base_tag.assert_called_once_with(self.gdocs.return_value, 1, "en")

    def test_default_name(self):
        self.run_callback()

        folder_id, filename, content = self.gdocs.return_value.upload.call_args[0]

        self.assertEqual(folder_id, "folder")
        self.assertRegex(filename, r"^Report 1 \d{4}-\d{2}-\d{2} ")
        self.assertEqual(content, "content")

    def test_name(self):
        self.export.name = "Report"
        self.export.save()

        self.run_callback()

        self.gdocs.return_value.upload.assert_called_once_with("folder", "Report", "content")

    def test_template_error(self):
        self.base_tag.return_value.validate_and_render.side_effect = TagError("Unknown tag", "{% xxx %}", "template")

        self.run_callback()

        self.assert_export(
            Export.Status.TEMPLATE_ERROR,
            errors=[{"reason": "Unknown tag", "tag": "{% xxx %}", "template_id": "template"}],
        )
        self.gdocs.return_value.close.assert_called_once_with()

    def test_drive_error(self):
        self.gdocs.side_effect = GoogleDriveError("Unable to open the template")

        with self.assertLogs(MODULE, level="ERROR"):
            self.run_callback()

        self.assert_export(Export.Status.ERROR, reason="Google Drive Error: Unable to open the template")
        self.gdocs.return_value.close.assert_not_called()  # never opened

    def test_unexpected_error(self):
        self.base_tag.return_value.validate_and_render.side_effect = ValueError("anything")

        with self.assertLogs(MODULE, level="ERROR"):
            self.run_callback()

        self.assert_export(Export.Status.ERROR, reason="An unexpected error occurred.")
        self.gdocs.return_value.close.assert_called_once_with()
