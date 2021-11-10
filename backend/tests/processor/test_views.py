from unittest.mock import patch

from django.db import connections
from django.test import TransactionTestCase
from dqt.models import DataItem, Dataset, FieldLevelCheck, ProgressMonitorDataset


class ViewsTests(TransactionTestCase):
    databases = {"default", "data"}
    unmanaged = {DataItem, Dataset, FieldLevelCheck, ProgressMonitorDataset}

    def setUp(self):
        with connections["data"].schema_editor() as schema_editor:
            for model in self.unmanaged:
                schema_editor.create_model(model)

    def tearDown(self):
        with connections["data"].schema_editor() as schema_editor:
            for model in self.unmanaged:
                schema_editor.delete_model(model)

    def create(self, model, **kwargs):
        obj = model(**kwargs)
        obj.full_clean()
        obj.save()
        return obj

    def test_require_POST(self):
        for path in ("api/create_dataset_filter", "datasets/", "datasets/123/"):
            with self.subTest(path=path):
                response = self.client.get(f"/{path}")

                self.assertEqual(response.status_code, 405)

    @patch("processor.views.publish")
    def test_create(self, publish):
        response = self.client.post(
            "/datasets/", {"name": "anything", "collection_id": 123, "xxx": "xxx"}, "application/json"
        )

        self.assertEqual(response.status_code, 202)
        publish.assert_called_once_with('{"name": "anything", "collection_id": 123}', "ocds_kingfisher_extractor_init")

    @patch("processor.views.publish")
    def test_create_dataset_filter(self, publish):
        response = self.client.post(
            "/api/create_dataset_filter", {"dataset_id_original": 123, "filter_message": {}}, "application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
        publish.assert_called_once_with(
            b'{"dataset_id_original": 123, "filter_message": {}}', "dataset_filter_extractor_init"
        )

    @patch("processor.views.publish")
    def test_destroy(self, publish):
        response = self.client.delete("/datasets/123/")

        self.assertEqual(response.status_code, 202)
        publish.assert_called_once_with('{"dataset_id": 123}', "wiper_init")

    def test_find_by_name(self):
        dataset = self.create(Dataset, name="anything")

        response = self.client.get("/datasets/find_by_name/?name=anything")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"id": dataset.pk})

    def test_metadata_no_meta(self):
        dataset = self.create(Dataset, name="anything")

        response = self.client.get(f"/datasets/{dataset.pk}/metadata/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_metadata(self):
        dataset = self.create(Dataset, name="anything", meta={"collection_metadata": {"ocid_prefix": "ocds-213czf"}})

        response = self.client.get(f"/datasets/{dataset.pk}/metadata/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"ocid_prefix": "ocds-213czf"})

    def test_coverage(self):
        dataset = self.create(Dataset, name="anything")
        data_item = self.create(DataItem, dataset=dataset, data={"parties": {"id": 1}})
        self.create(FieldLevelCheck, dataset=dataset, data_item=data_item, result={"checks": {"parties.id": [{}]}})

        response = self.client.get(f"/datasets/{dataset.pk}/coverage/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "amendments": 0,
                "awards": 0,
                "awards_items": 0,
                "awards_suppliers": 0,
                "contracts": 0,
                "contracts_items": 0,
                "contracts_transactions": 0,
                "documents": 0,
                "milestones": 0,
                "parties": 1,
                "plannings": 0,
                "tenderers": 0,
                "tenders": 0,
                "tenders_items": 0,
            },
        )

    def test_status_no_dataset(self):
        response = self.client.get("/datasets/123/status/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_status_no_progress(self):
        dataset = self.create(Dataset, name="anything")

        response = self.client.get(f"/datasets/{dataset.pk}/status/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_status_no_values(self):
        dataset = self.create(Dataset, name="anything")
        self.create(ProgressMonitorDataset, dataset=dataset)

        response = self.client.get(f"/datasets/{dataset.pk}/status/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"phase": None, "state": None})

    def test_status(self):
        dataset = self.create(Dataset, name="anything")
        self.create(ProgressMonitorDataset, dataset=dataset, phase="CHECKED", state="OK")

        response = self.client.get(f"/datasets/{dataset.pk}/status/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"phase": "CHECKED", "state": "OK"})
