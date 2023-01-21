from unittest.mock import patch

from api.models import DataItem, Dataset, DatasetFilter, FieldLevelCheck, ProgressMonitorDataset
from tests import TestCase


class ViewsTests(TestCase):
    def test_data_items_list_not_implemented(self):
        response = self.client.get("/data_items/")

        self.assertEqual(response.status_code, 404)

    def test_data_items_retrieve(self):
        dataset = self.create(Dataset, name="parent")
        data_item = self.create(DataItem, dataset=dataset, data={"parties": {"id": 1}})
        response = self.client.get(f"/data_items/{data_item.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"data": {"parties": {"id": 1}}, "id": 1})

    def test_datasets_list(self):
        dataset = self.create(Dataset, name="parent")
        filtered = self.create(Dataset, name="child")
        self.create(ProgressMonitorDataset, dataset=dataset, phase="CHECKED", state="OK")
        self.create(DatasetFilter, parent=dataset, dataset=filtered, filter_message={"buyer": "Acme Inc."})
        response = self.client.get("/datasets/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": dataset.pk,
                    "name": "parent",
                    "meta": {},
                    "ancestor_id": None,
                    "created": None,
                    "modified": None,
                    "phase": "CHECKED",
                    "state": "OK",
                    "parent_id": None,
                    "parent_name": None,
                    "filter_message": None,
                },
                {
                    "id": filtered.pk,
                    "name": "child",
                    "meta": {},
                    "ancestor_id": None,
                    "created": None,
                    "modified": None,
                    "phase": None,
                    "state": None,
                    "parent_id": dataset.pk,
                    "parent_name": "parent",
                    "filter_message": {"buyer": "Acme Inc."},
                },
            ],
        )

    def test_datasets_retrieve(self):
        dataset = self.create(Dataset, name="parent")
        filtered = self.create(Dataset, name="child")
        self.create(ProgressMonitorDataset, dataset=dataset, phase="CHECKED", state="OK")
        self.create(DatasetFilter, parent=dataset, dataset=filtered, filter_message={"buyer": "Acme Inc."})
        response = self.client.get(f"/datasets/{filtered.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "id": filtered.pk,
                "name": "child",
                "meta": {},
                "ancestor_id": None,
                "created": None,
                "modified": None,
                "phase": None,
                "state": None,
                "parent_id": dataset.pk,
                "parent_name": "parent",
                "filter_message": {"buyer": "Acme Inc."},
            },
        )

    @patch("controller.views.publish")
    def test_datasets_create_invalid(self, publish):
        response = self.client.post("/datasets/", {"name": "anything", "collection_id": "xxx"}, "application/json")

        self.assertEqual(response.status_code, 400)
        publish.assert_not_called()

    @patch("controller.views.publish")
    def test_datasets_create_no_values(self, publish):
        response = self.client.post("/datasets/", {}, "application/json")

        self.assertEqual(response.status_code, 400)
        publish.assert_not_called()

    @patch("controller.views.publish")
    def test_datasets_create(self, publish):
        response = self.client.post(
            "/datasets/", {"name": "anything", "collection_id": "123", "xxx": "xxx"}, "application/json"
        )

        self.assertEqual(response.status_code, 202)
        publish.assert_called_once_with({"name": "anything", "collection_id": 123}, "ocds_kingfisher_extractor_init")

    @patch("controller.views.publish")
    def test_datasets_filter_invalid(self, publish):
        response = self.client.post("/datasets/123/filter/", {"buyer": "xxx"}, "application/json")

        self.assertEqual(response.status_code, 400)
        publish.assert_not_called()

    @patch("controller.views.publish")
    def test_datasets_filter_no_values(self, publish):
        response = self.client.post("/datasets/123/filter/", {}, "application/json")

        self.assertEqual(response.status_code, 202)
        publish.assert_called_once_with(
            {"dataset_id_original": 123, "filter_message": {}}, "dataset_filter_extractor_init"
        )

    @patch("controller.views.publish")
    def test_datasets_filter(self, publish):
        response = self.client.post("/datasets/123/filter/", {"buyer": ["MOF"], "xxx": "xxx"}, "application/json")

        self.assertEqual(response.status_code, 202)
        publish.assert_called_once_with(
            {"dataset_id_original": 123, "filter_message": {"buyer": ["MOF"]}}, "dataset_filter_extractor_init"
        )

    @patch("controller.views.publish")
    def test_datasets_destroy(self, publish):
        response = self.client.delete("/datasets/123/")

        self.assertEqual(response.status_code, 202)
        publish.assert_called_once_with({"dataset_id": 123}, "wiper_init")

    def test_datasets_find_by_name_no_name(self):
        self.create(Dataset, name="anything")
        response = self.client.get("/datasets/find_by_name/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_datasets_find_by_name_no_match(self):
        self.create(Dataset, name="anything")
        response = self.client.get("/datasets/find_by_name/?name=other")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_datasets_find_by_name(self):
        dataset = self.create(Dataset, name="anything")
        response = self.client.get("/datasets/find_by_name/?name=anything")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"id": dataset.pk})

    def test_datasets_status_no_progress(self):
        dataset = self.create(Dataset, name="anything")
        response = self.client.get(f"/datasets/{dataset.pk}/status/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_datasets_status_no_values(self):
        dataset = self.create(Dataset, name="anything")
        self.create(ProgressMonitorDataset, dataset=dataset)
        response = self.client.get(f"/datasets/{dataset.pk}/status/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"phase": None, "state": None})

    def test_datasets_status(self):
        dataset = self.create(Dataset, name="anything")
        self.create(ProgressMonitorDataset, dataset=dataset, phase="CHECKED", state="OK")
        response = self.client.get(f"/datasets/{dataset.pk}/status/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"phase": "CHECKED", "state": "OK"})

    def test_datasets_metadata_no_values(self):
        dataset = self.create(Dataset, name="anything")
        response = self.client.get(f"/datasets/{dataset.pk}/metadata/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_datasets_metadata(self):
        dataset = self.create(Dataset, name="anything", meta={"collection_metadata": {"ocid_prefix": "ocds-213czf"}})
        response = self.client.get(f"/datasets/{dataset.pk}/metadata/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"ocid_prefix": "ocds-213czf"})

    def test_datasets_coverage(self):
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

    def test_datasets_status_no_dataset(self):
        response = self.client.get("/datasets/123/status/")
        self.assertEqual(response.status_code, 404)

    def test_datasets_metadata_no_dataset(self):
        response = self.client.get("/datasets/123/metadata/")
        self.assertEqual(response.status_code, 404)

    def test_datasets_coverage_no_dataset(self):
        response = self.client.get("/datasets/123/coverage/")
        self.assertEqual(response.status_code, 404)
