from unittest.mock import patch

from api.models import (
    DataItem,
    Dataset,
    DatasetFilter,
    FieldLevelCheckExamples,
    ProgressMonitorDataset,
    Report,
    ResourceLevelCheckExamples,
)
from tests import PelicanTestCase

REPORT_URLS = (
    "field_level_report/",
    "compiled_release_level_report/",
    "dataset_level_report/",
    "time_based_report/",
    "field_level/ocid/",
    "field_level/ocid/failures/",
    "compiled_release_level/coherent.dates/",
    "compiled_release_level/coherent.dates/failures/",
)
# The smallest report and examples that the detail views can merge.
FIELD_LEVEL = {"coverage": {"checks": {}}, "quality": {"checks": {}}}
FIELD_LEVEL_EXAMPLES = {
    group: {"passed_examples": [], "failed_examples": [], "checks": {}} for group in ("coverage", "quality")
}


class AuthorizationTests(PelicanTestCase):
    def setUp(self):
        super().setUp()

        self.own = self.create(Dataset, name="chile_compra_bulk_2026-01-01")

        # Pelican backend copies a report's name into a report filtered from it.
        self.filtered = self.create(Dataset, name="chile_compra_bulk_2026-01-01")
        self.create(DatasetFilter, parent=self.own, dataset=self.filtered, filter_message={"buyer": ["MOF"]})

        self.other = self.create(Dataset, name="dominican_republic_api_2026-01-01")

        self.internal = self.create(Dataset, name="chile_compra_bulk_2026-01-01_test")

        self.sign_in("publisher", spiders=["chile_compra_bulk"])

    def test_list(self):
        response = self.client.get("/api/datasets/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([dataset["id"] for dataset in response.json()], [self.own.pk, self.filtered.pk])

    def test_list_without_publisher(self):
        self.sign_in("newcomer")

        response = self.client.get("/api/datasets/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.text, [])

    def test_retrieve_own(self):
        self.create(ProgressMonitorDataset, dataset=self.own, phase="CHECKED", state="OK")

        response = self.client.get(f"/api/datasets/{self.own.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "chile_compra_bulk_2026-01-01")

    def test_retrieve_other(self):
        for dataset in (self.other, self.internal):
            with self.subTest(name=dataset.name):
                response = self.client.get(f"/api/datasets/{dataset.pk}/")

                self.assertEqual(response.status_code, 404)

    def create_reports(self, dataset):
        self.create(Report, dataset=dataset, type="field_level_check", data={"ocid": FIELD_LEVEL})
        self.create(Report, dataset=dataset, type="resource_level_check", data={"coherent.dates": {}})
        self.create(FieldLevelCheckExamples, dataset=dataset, path="ocid", data=FIELD_LEVEL_EXAMPLES)
        self.create(ResourceLevelCheckExamples, dataset=dataset, check_name="coherent.dates", data={})

    def test_reports_own(self):
        self.create_reports(self.own)

        for url in REPORT_URLS:
            with self.subTest(url=url):
                response = self.client.get(f"/api/datasets/{self.own.pk}/{url}")
                # The failures views query the database only when the response is iterated.
                if response.streaming:
                    b"".join(response.streaming_content)

                self.assertEqual(response.status_code, 200)

    def test_reports_other(self):
        for dataset in (self.other, self.internal):
            self.create_reports(dataset)
            for url in REPORT_URLS:
                with self.subTest(name=dataset.name, url=url):
                    response = self.client.get(f"/api/datasets/{dataset.pk}/{url}")

                    # No rows match a dataset the user can't see, so these two endpoints return an empty report,
                    # rather than 404, which would require an additional query.
                    if url.endswith(("dataset_level_report/", "time_based_report/")):
                        self.assertEqual(response.status_code, 200)
                        self.assertJSONEqual(response.text, {})
                    else:
                        self.assertEqual(response.status_code, 404)

    def test_data_item_own(self):
        data_item = self.create(DataItem, dataset=self.own, data={"ocid": "ocds-213czf-1"})

        response = self.client.get(f"/api/data_items/{data_item.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.text, {"id": data_item.pk, "data": {"ocid": "ocds-213czf-1"}})

    def test_data_item_other(self):
        data_item = self.create(DataItem, dataset=self.other, data={"ocid": "ocds-213czf-2"})

        response = self.client.get(f"/api/data_items/{data_item.pk}/")

        self.assertEqual(response.status_code, 404)

    def test_distinct_values_own(self):
        self.create(DataItem, dataset=self.own, data={"buyer": {"name": "MOF"}})

        response = self.client.get(f"/api/dataset-distinct-values/{self.own.pk}/buyer.name/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.text, [{"value": "MOF", "count": 1}])

    def test_distinct_values_other(self):
        self.create(DataItem, dataset=self.other, data={"buyer": {"name": "MOH"}})

        response = self.client.get(f"/api/dataset-distinct-values/{self.other.pk}/buyer.name/")

        self.assertEqual(response.status_code, 404)

    def test_filter_items_own(self):
        self.create(DataItem, dataset=self.own, data={"buyer": {"name": "MOF"}})

        response = self.client.post(
            "/api/dataset-filter-items/",
            {"dataset_id_original": self.own.pk, "filter_message": {}},
            "application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.text, {"items": 1})

    def test_filter_items_other(self):
        response = self.client.post(
            "/api/dataset-filter-items/",
            {"dataset_id_original": self.other.pk, "filter_message": {}},
            "application/json",
        )

        self.assertEqual(response.status_code, 404)

    @patch("api.views.publish")
    def test_filter_own(self, publish):
        response = self.client.post(f"/api/datasets/{self.own.pk}/filter/", {}, "application/json")

        self.assertEqual(response.status_code, 202)
        publish.assert_called_once_with(
            {"dataset_id_original": self.own.pk, "filter_message": {}}, "dataset_filter_extractor_init"
        )

    @patch("api.views.publish")
    def test_filter_other(self, publish):
        response = self.client.post(f"/api/datasets/{self.other.pk}/filter/", {}, "application/json")

        self.assertEqual(response.status_code, 404)
        publish.assert_not_called()

    @patch("api.views.publish")
    def test_create_is_staff_only(self, publish):
        response = self.client.post(
            "/api/datasets/", {"name": "chile_compra_bulk_2026-02-01", "collection_id": 123}, "application/json"
        )

        self.assertEqual(response.status_code, 403)
        publish.assert_not_called()

    @patch("api.views.publish")
    def test_destroy_is_staff_only(self, publish):
        response = self.client.delete(f"/api/datasets/{self.own.pk}/")

        self.assertEqual(response.status_code, 403)
        publish.assert_not_called()
