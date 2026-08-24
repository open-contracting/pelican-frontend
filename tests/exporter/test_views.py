from unittest.mock import patch

from api.models import Dataset
from exporter.models import Export
from tests import PelicanTestCase

INPUT_MESSAGE = {"document_id": "anything", "folder_id": "anything"}


class ExportTests(PelicanTestCase):
    def create_export(self, user, **kwargs):
        return self.create(Export, user=user, dataset_id=1, document_id="anything", folder_id="anything", **kwargs)

    def test_list(self):
        response = self.client.get("/api/exports/")

        self.assertEqual(response.status_code, 405)

    def test_anonymous(self):
        self.sign_out()

        for method, url in (("post", "/api/exports/"), ("get", "/api/exports/1/")):
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, {}, "application/json")

                self.assertEqual(response.status_code, 403)

    @patch("exporter.views.publish")
    def test_create_malformed(self, publish):
        for input_message in (
            {},
            {"dataset_id": 1},  # missing document_id and folder_id keys
            INPUT_MESSAGE,  # missing dataset_id key
            {"dataset_id": "anything", **INPUT_MESSAGE},  # incorrect dataset_id
            {"dataset_id": 1, "document_id": "", "folder_id": ""},  # blank document_id and folder_id
        ):
            with self.subTest(input_message=input_message):
                response = self.client.post("/api/exports/", input_message, "application/json")

                self.assertEqual(response.status_code, 400)
                self.assertFalse(Export.objects.exists())
                publish.assert_not_called()

    @patch("exporter.views.publish")
    def test_create_unauthorized_dataset(self, publish):
        dataset = self.create(Dataset, name="chile_compra_bulk_2026-01-01")
        self.sign_in("publisher", spiders=["dominican_republic_api"])

        response = self.client.post("/api/exports/", {"dataset_id": dataset.pk, **INPUT_MESSAGE}, "application/json")

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Export.objects.exists())
        publish.assert_not_called()

    @patch("exporter.views.publish")
    def test_create_nonexistent_dataset(self, publish):
        response = self.client.post("/api/exports/", {"dataset_id": 123, **INPUT_MESSAGE}, "application/json")

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Export.objects.exists())
        publish.assert_not_called()

    @patch("exporter.views.publish")
    def test_create(self, publish):
        dataset = self.create(Dataset, name="chile_compra_bulk_2026-01-01")
        user = self.sign_in("publisher", spiders=["chile_compra_bulk"])

        response = self.client.post(
            "/api/exports/",
            {
                "dataset_id": dataset.pk,
                # A pasted ID can have whitespace around it.
                "document_id": " anything ",
                "folder_id": " anything ",
                "language": "es",
                "report_name": "Report",
            },
            "application/json",
        )

        export = Export.objects.get()
        self.assertEqual(response.status_code, 202)
        self.assertJSONEqual(
            response.text,
            {
                "id": export.pk,
                "status": "waiting",
                "file_id": "",
                "reason": "",
                "tag_errors": [],
                "failed_tags": [],
            },
        )
        publish.assert_called_once_with({"export_id": export.pk}, "report_exporter_init")
        self.assertEqual(export.user, user)
        self.assertEqual(export.dataset_id, dataset.pk)
        self.assertEqual(export.document_id, "anything")
        self.assertEqual(export.folder_id, "anything")
        self.assertEqual(export.language, "es")
        self.assertEqual(export.report_name, "Report")

    def test_retrieve_waiting(self):
        export = self.create_export(self.user)

        response = self.client.get(f"/api/exports/{export.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.text,
            {
                "id": export.pk,
                "status": "waiting",
                "file_id": "",
                "reason": "",
                "tag_errors": [],
                "failed_tags": [],
            },
        )

    def test_retrieve_ok(self):
        export = self.create_export(self.user, status=Export.Status.OK, file_id="anything", failed_tags=["{% id %}"])

        response = self.client.get(f"/api/exports/{export.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.text,
            {
                "id": export.pk,
                "status": "ok",
                "file_id": "anything",
                "reason": "",
                "tag_errors": [],
                "failed_tags": ["{% id %}"],
            },
        )

    def test_retrieve_report_error(self):
        export = self.create_export(self.user, status=Export.Status.REPORT_ERROR, reason="Unable to open the template")

        response = self.client.get(f"/api/exports/{export.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["reason"], "Unable to open the template")

    def test_retrieve_template_error(self):
        tag_error = {"reason": "Unknown tag", "full_tag": "{% xxx %}", "template_id": "anything"}
        export = self.create_export(self.user, status=Export.Status.TEMPLATE_ERROR, tag_errors=[tag_error])

        response = self.client.get(f"/api/exports/{export.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["tag_errors"], [tag_error])

    def test_retrieve_another_users_export(self):
        export = self.create_export(self.user)
        self.sign_in("staff2", is_staff=True)

        response = self.client.get(f"/api/exports/{export.pk}/")

        self.assertEqual(response.status_code, 404)

    def test_retrieve_nonexistent(self):
        response = self.client.get("/api/exports/123/")

        self.assertEqual(response.status_code, 404)
