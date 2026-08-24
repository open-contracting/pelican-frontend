from unittest.mock import Mock, patch

from exporter.exceptions import GoogleDriveError, TagError
from exporter.management.commands.export import callback
from exporter.models import Export
from tests import PelicanTestCase

MODULE = "exporter.management.commands.export"


class ExportTests(PelicanTestCase):
    def setUp(self):
        super().setUp()
        # Each test runs in a transaction, which closing the connection would roll back.
        self.enterContext(patch(f"{MODULE}.close_old_connections"))
        self.ack = self.enterContext(patch(f"{MODULE}.ack"))
        self.gdocs = self.enterContext(patch(f"{MODULE}.Gdocs"))
        self.base_tag = self.enterContext(patch(f"{MODULE}.base_tag"))
        self.base_tag.return_value.validate_and_render.return_value = ("content", [])
        self.gdocs.return_value.upload.return_value = "file"
        self.export = self.create(
            Export, user=self.user, dataset_id=1, document_id="template", folder_id="folder", language="es"
        )

    def run_callback(self):
        callback(Mock(), Mock(), Mock(delivery_tag=1), Mock(), {"export_id": self.export.pk})
        self.export.refresh_from_db()

    def test_ok(self):
        self.base_tag.return_value.validate_and_render.return_value = ("content", ["{% id %}"])

        self.run_callback()

        self.assertEqual(self.export.status, Export.Status.OK)
        self.assertEqual(self.export.file_id, "file")
        self.assertEqual(self.export.failed_tags, ["{% id %}"])
        self.assertEqual(self.export.reason, "")
        self.gdocs.assert_called_once_with("template")
        self.base_tag.assert_called_once_with(self.gdocs.return_value, 1, "es")
        self.gdocs.return_value.close.assert_called_once_with()
        self.ack.assert_called_once()

    def test_default_language(self):
        self.export.language = "xx"
        self.export.save()

        self.run_callback()

        self.base_tag.assert_called_once_with(self.gdocs.return_value, 1, "en")

    def test_default_report_name(self):
        self.run_callback()

        folder_id, filename, content = self.gdocs.return_value.upload.call_args[0]
        self.assertEqual(folder_id, "folder")
        self.assertRegex(filename, r"^Report 1 \d{4}-\d{2}-\d{2} ")
        self.assertEqual(content, "content")

    def test_report_name(self):
        self.export.report_name = "Report"
        self.export.save()

        self.run_callback()

        self.gdocs.return_value.upload.assert_called_once_with("folder", "Report", "content")

    def test_report_error(self):
        self.gdocs.side_effect = GoogleDriveError("Unable to open the template")

        with self.assertLogs(MODULE, level="ERROR"):
            self.run_callback()

        self.assertEqual(self.export.status, Export.Status.REPORT_ERROR)
        self.assertEqual(self.export.reason, "Google Drive Error: Unable to open the template")
        self.assertEqual(self.export.file_id, "")
        self.ack.assert_called_once()

    def test_template_error(self):
        self.base_tag.return_value.validate_and_render.side_effect = TagError("Unknown tag", "{% xxx %}", "template")

        self.run_callback()

        self.assertEqual(self.export.status, Export.Status.TEMPLATE_ERROR)
        self.assertEqual(
            self.export.tag_errors, [{"reason": "Unknown tag", "full_tag": "{% xxx %}", "template_id": "template"}]
        )
        self.assertEqual(self.export.failed_tags, [])
        self.gdocs.return_value.close.assert_called_once_with()
        self.ack.assert_called_once()

    def test_unexpected_error(self):
        self.base_tag.return_value.validate_and_render.side_effect = ValueError("anything")

        with self.assertLogs(MODULE, level="ERROR"):
            self.run_callback()

        self.assertEqual(self.export.status, Export.Status.REPORT_ERROR)
        self.assertEqual(self.export.reason, "An unexpected error occurred.")
        self.ack.assert_called_once()
