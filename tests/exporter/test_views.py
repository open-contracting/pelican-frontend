from unittest.mock import patch

from api.models import Dataset
from exporter.exceptions import GoogleDriveError
from tests import PelicanTestCase

MALFORMED = {"status": "report_error", "data": {"reason": "Input message is malformed, will be dropped."}}


class GenerateReportTests(PelicanTestCase):
    def test_get(self):
        response = self.client.get("/api/generate-report")

        self.assertEqual(response.status_code, 405)

    def test_anonymous(self):
        self.sign_out()

        response = self.client.post("/api/generate-report", {}, "application/json")

        self.assertEqual(response.status_code, 403)

    def test_malformed(self):
        for input_message in (
            {},
            {"dataset_id": 1},  # missing document_id and folder_id keys
            {"document_id": "anything", "folder_id": "anything"},  # missing dataset_id key
            {"dataset_id": "anything", "document_id": "anything", "folder_id": "anything"},  # incorrect dataset_id
        ):
            with self.subTest(input_message=input_message):
                response = self.client.post("/api/generate-report", input_message, "application/json")

                # The response is 200, so that the frontend reports the reason instead of a server error.
                self.assertEqual(response.status_code, 200)
                self.assertJSONEqual(response.text, MALFORMED)

    def test_unauthorized_dataset(self):
        dataset = self.create(Dataset, name="chile_compra_bulk_2026-01-01")
        self.sign_in("publisher", spiders=["dominican_republic_api"])

        response = self.client.post(
            "/api/generate-report",
            {"dataset_id": dataset.pk, "document_id": "anything", "folder_id": "anything"},
            "application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_nonexistent_dataset(self):
        response = self.client.post(
            "/api/generate-report",
            {"dataset_id": 123, "document_id": "anything", "folder_id": "anything"},
            "application/json",
        )

        self.assertEqual(response.status_code, 404)

    @patch("exporter.views.Gdocs", side_effect=GoogleDriveError("Unable to open the template"))
    def test_own_dataset(self, gdocs):
        dataset = self.create(Dataset, name="chile_compra_bulk_2026-01-01")
        self.sign_in("publisher", spiders=["chile_compra_bulk"])

        response = self.client.post(
            "/api/generate-report",
            {"dataset_id": dataset.pk, "document_id": "anything", "folder_id": "anything"},
            "application/json",
        )

        # The export is attempted, rather than refused.
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.text,
            {"status": "report_error", "data": {"reason": "Google Drive Error: Unable to open the template"}},
        )
        gdocs.assert_called_once_with("anything")
