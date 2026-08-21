from django.test import SimpleTestCase

MALFORMED = {"status": "report_error", "data": {"reason": "Input message is malformed, will be dropped."}}


class GenerateReportTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/api/generate-report")

        self.assertEqual(response.status_code, 405)

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
