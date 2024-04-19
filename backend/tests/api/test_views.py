import json
from unittest.mock import patch

from api.models import (
    DataItem,
    Dataset,
    DatasetFilter,
    DatasetLevelCheck,
    FieldLevelCheck,
    FieldLevelCheckExamples,
    ProgressMonitorDataset,
    Report,
    ResourceLevelCheckExamples,
    TimeVarianceLevelCheck,
)
from tests import PelicanTestCase


class ViewsTests(PelicanTestCase):
    def test_openapi(self):
        response = self.client.get("/api/schema/")

        self.assertEqual(response.status_code, 200)

    def test_swagger_ui(self):
        response = self.client.get("/api/schema/swagger-ui/")

        self.assertEqual(response.status_code, 200)

    def test_data_items_list_not_implemented(self):
        with self.assertNumQueries(0, using="data"):
            response = self.client.get("/api/data_items/")

            self.assertEqual(response.status_code, 404)

    def test_data_items_retrieve(self):
        dataset = self.create(Dataset, name="parent")
        data_item = self.create(DataItem, dataset=dataset, data={"parties": {"id": 1}})

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/data_items/{data_item.pk}/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"data": {"parties": {"id": 1}}, "id": 1})

    def test_datasets_list(self):
        dataset = self.create(Dataset, name="parent")
        filtered = self.create(Dataset, name="child")
        self.create(ProgressMonitorDataset, dataset=dataset, phase="CHECKED", state="OK")
        self.create(DatasetFilter, parent=dataset, dataset=filtered, filter_message={"buyer": "Acme Inc."})

        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/")

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

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{filtered.pk}/")

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

    @patch("api.views.publish")
    def test_datasets_create_invalid(self, publish):
        with self.assertNumQueries(0, using="data"):
            response = self.client.post(
                "/api/datasets/", {"name": "anything", "collection_id": "xxx"}, "application/json"
            )

            self.assertEqual(response.status_code, 400)
        publish.assert_not_called()

    @patch("api.views.publish")
    def test_datasets_create_no_values(self, publish):
        with self.assertNumQueries(0, using="data"):
            response = self.client.post("/api/datasets/", {}, "application/json")

            self.assertEqual(response.status_code, 400)
        publish.assert_not_called()

    @patch("api.views.publish")
    def test_datasets_create(self, publish):
        with self.assertNumQueries(0, using="data"):
            response = self.client.post(
                "/api/datasets/", {"name": "anything", "collection_id": "123", "xxx": "xxx"}, "application/json"
            )

            self.assertEqual(response.status_code, 202)
            publish.assert_called_once_with(
                {"name": "anything", "collection_id": 123, "ancestor_id": None, "max_items": None},
                "ocds_kingfisher_extractor_init",
            )

    @patch("api.views.publish")
    def test_datasets_filter_invalid(self, publish):
        with self.assertNumQueries(0, using="data"):
            response = self.client.post("/api/datasets/123/filter/", {"buyer": "xxx"}, "application/json")

            self.assertEqual(response.status_code, 400)
            publish.assert_not_called()

    @patch("api.views.publish")
    def test_datasets_filter_no_values(self, publish):
        with self.assertNumQueries(0, using="data"):
            response = self.client.post("/api/datasets/123/filter/", {}, "application/json")

            self.assertEqual(response.status_code, 202)
            publish.assert_called_once_with(
                {"dataset_id_original": 123, "filter_message": {}}, "dataset_filter_extractor_init"
            )

    @patch("api.views.publish")
    def test_datasets_filter(self, publish):
        with self.assertNumQueries(0, using="data"):
            response = self.client.post(
                "/api/datasets/123/filter/", {"buyer": ["MOF"], "xxx": "xxx"}, "application/json"
            )

            self.assertEqual(response.status_code, 202)
            publish.assert_called_once_with(
                {"dataset_id_original": 123, "filter_message": {"buyer": ["MOF"]}}, "dataset_filter_extractor_init"
            )

    @patch("api.views.publish")
    def test_datasets_destroy(self, publish):
        with self.assertNumQueries(0, using="data"):
            response = self.client.delete("/api/datasets/123/")

            self.assertEqual(response.status_code, 202)
            publish.assert_called_once_with({"dataset_id": 123}, "wiper_init")

    def test_datasets_find_by_name_no_name(self):
        self.create(Dataset, name="anything")

        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/find_by_name/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {})

    def test_datasets_find_by_name_no_match(self):
        self.create(Dataset, name="anything")

        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/find_by_name/?name=other")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {})

    def test_datasets_find_by_name(self):
        dataset = self.create(Dataset, name="anything")

        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/find_by_name/?name=anything")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"id": dataset.pk})

    def test_datasets_field_level_report(self):
        dataset = self.create(Dataset, name="anything")
        self.create(Report, dataset=dataset, type="field_level_check", data={"ocid": {}})

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/field_level_report/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"ocid": {}})

    def test_datasets_compiled_release_level_report(self):
        dataset = self.create(Dataset, name="anything")
        self.create(Report, dataset=dataset, type="resource_level_check", data={"coherent.dates": {}})

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/compiled_release_level_report/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"coherent.dates": {}})

    def test_datasets_dataset_level_report(self):
        dataset = self.create(Dataset, name="anything")
        self.create(
            DatasetLevelCheck,
            dataset=dataset,
            check_name="distribution.tender_value",
            result=True,
            value=100,
            meta={"total_passed": 1},
        )
        self.create(
            DatasetLevelCheck,
            dataset=dataset,
            check_name="distribution.awards_value",
            result=False,
            value=0,
            meta={"total_failed": 1},
        )

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/dataset_level_report/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(
                response.content,
                {
                    "distribution.awards_value": {"meta": {"total_failed": 1}, "result": False, "value": 0},
                    "distribution.tender_value": {"meta": {"total_passed": 1}, "result": True, "value": 100},
                },
            )

    def test_datasets_time_based_report(self):
        dataset = self.create(Dataset, name="anything")
        self.create(
            TimeVarianceLevelCheck,
            dataset=dataset,
            check_name="phase_stable",
            coverage_value=100,
            coverage_result=True,
            check_value=99,
            check_result=True,
            meta={"version": 1.0},
        )
        self.create(
            TimeVarianceLevelCheck,
            dataset=dataset,
            check_name="tender_title",
            coverage_value=1,
            coverage_result=False,
            check_value=0,
            check_result=False,
            meta={"version": 1.1},
        )

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/time_based_report/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(
                response.content,
                {
                    "phase_stable": {
                        "check_result": True,
                        "check_value": 99,
                        "coverage_result": True,
                        "coverage_value": 100,
                        "meta": {"version": 1.0},
                    },
                    "tender_title": {
                        "check_result": False,
                        "check_value": 0,
                        "coverage_result": False,
                        "coverage_value": 1,
                        "meta": {"version": 1.1},
                    },
                },
            )

    def test_datasets_status_no_progress(self):
        dataset = self.create(Dataset, name="anything")

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/status/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {})

    def test_datasets_status_no_values(self):
        dataset = self.create(Dataset, name="anything")
        self.create(ProgressMonitorDataset, dataset=dataset)

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/status/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"phase": None, "state": None})

    def test_datasets_status(self):
        dataset = self.create(Dataset, name="anything")
        self.create(ProgressMonitorDataset, dataset=dataset, phase="CHECKED", state="OK")

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/status/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"phase": "CHECKED", "state": "OK"})

    def test_datasets_metadata_no_values(self):
        dataset = self.create(Dataset, name="anything")

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/metadata/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {})

    def test_datasets_metadata(self):
        dataset = self.create(Dataset, name="anything", meta={"collection_metadata": {"ocid_prefix": "ocds-213czf"}})

        with self.assertNumQueries(1, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/metadata/")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"ocid_prefix": "ocds-213czf"})

    def test_datasets_coverage(self):
        dataset = self.create(Dataset, name="anything")
        data_item = self.create(DataItem, dataset=dataset, data={"parties": {"id": 1}})
        self.create(FieldLevelCheck, dataset=dataset, data_item=data_item, result={"checks": {"parties.id": [{}]}})

        with self.assertNumQueries(2, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/coverage/")

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

    def test_field_level_detail(self):
        dataset = self.create(Dataset, name="anything")
        self.create(
            Report,
            dataset=dataset,
            type="field_level_check",
            data={
                "ocid": {
                    "coverage": {
                        "checks": {"exists": {"passed_examples": [1], "failed_examples": [2]}, "non_empty": {}},
                    },
                    "quality": {
                        "checks": {"exists": {"passed_examples": [3], "failed_examples": [4]}, "non_empty": {}},
                    },
                }
            },
        )
        self.create(
            FieldLevelCheckExamples,
            dataset=dataset,
            path="ocid",
            data={
                "coverage": {
                    "passed_examples": [11],
                    "failed_examples": [12],
                    "checks": {"exists": {"passed_examples": [13], "failed_examples": [14]}},
                },
                "quality": {
                    "passed_examples": [15],
                    "failed_examples": [16],
                    "checks": {"exists": {"passed_examples": [17], "failed_examples": [18]}},
                },
            },
        )

        with self.assertNumQueries(2, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/field_level/ocid/")
            detail = json.loads(response.content)
            detail.pop("time")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(
                json.dumps(detail),
                {
                    "coverage": {
                        "passed_examples": [11],
                        "failed_examples": [12],
                        "checks": {"exists": {"passed_examples": [13], "failed_examples": [14]}, "non_empty": {}},
                    },
                    "quality": {
                        "passed_examples": [15],
                        "failed_examples": [16],
                        "checks": {"exists": {"passed_examples": [17], "failed_examples": [18]}, "non_empty": {}},
                    },
                },
            )

    def test_resource_level_detail(self):
        dataset = self.create(Dataset, name="anything")
        self.create(Report, dataset=dataset, type="resource_level_check", data={"coherent.dates": {"a": "b"}})
        self.create(ResourceLevelCheckExamples, dataset=dataset, check_name="coherent.dates", data={"c": "d"})

        with self.assertNumQueries(2, using="data"):
            response = self.client.get(f"/api/datasets/{dataset.pk}/compiled_release_level/coherent.dates/")
            detail = json.loads(response.content)
            detail.pop("time")

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(json.dumps(detail), {"a": "b", "c": "d"})

    def test_datasets_field_level_report_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/field_level_report/")

            self.assertEqual(response.status_code, 404)

    def test_datasets_compiled_release_level_report_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/compiled_release_level_report/")

            self.assertEqual(response.status_code, 404)

    def test_datasets_dataset_level_report_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/dataset_level_report/")

            self.assertEqual(response.status_code, 200)  # returning 404 requires an additional query

    def test_datasets_time_based_report_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/time_based_report/")

            self.assertEqual(response.status_code, 200)  # returning 404 requires an additional query

    def test_datasets_status_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/status/")

            self.assertEqual(response.status_code, 404)

    def test_datasets_metadata_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/metadata/")

            self.assertEqual(response.status_code, 404)

    def test_datasets_coverage_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/coverage/")

            self.assertEqual(response.status_code, 404)

    def test_field_level_detail_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/field_level/ocid/")

            self.assertEqual(response.status_code, 404)

    def test_resource_level_detail_no_dataset(self):
        with self.assertNumQueries(1, using="data"):
            response = self.client.get("/api/datasets/123/compiled_release_level/coherent.dates/")

            self.assertEqual(response.status_code, 404)
