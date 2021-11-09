from dqt.models import Dataset
from exporter.tags.leaf_tags.key_leaf_tag_factory import generate_key_leaf_tag
from exporter.tags.leaf_tags.overview.lifecycle_image import LifecycleImageLeafTag
from exporter.tags.leaf_tags.overview.lifecycle_object_count import LifecycleObjectCountLeafTag
from exporter.tags.leaf_tags.overview.release_date_count import ReleaseDateCountLeafTag
from exporter.tags.leaf_tags.overview.release_date_distribution_image import ReleaseDateDistributionImageLeafTag
from exporter.tags.leaf_tags.timestamp_leaf_tag_factory import generate_timestamp_leaf_tag
from exporter.tags.tag import TemplateTag


class OverviewTemplateTag(TemplateTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.prepare_data, "1sYr5LipKRtegWWl3zfKIDoSZmZluawmAdAu3piKslTw", gdocs, dataset_id)

        self.set_sub_tag("id", generate_key_leaf_tag("id"))
        self.set_sub_tag("ancestorId", generate_key_leaf_tag("ancestorId"))
        self.set_sub_tag("url", generate_key_leaf_tag("url"))
        self.set_sub_tag("publisher", generate_key_leaf_tag("publisher"))
        self.set_sub_tag("publishingStart", generate_timestamp_leaf_tag("publishingStart", "%Y-%m-%d %H.%M.%S"))
        self.set_sub_tag("publishingEnd", generate_timestamp_leaf_tag("publishingEnd", "%Y-%m-%d %H.%M.%S"))
        self.set_sub_tag("ocidPrefix", generate_key_leaf_tag("ocidPrefix"))
        self.set_sub_tag("dataLicense", generate_key_leaf_tag("dataLicense"))
        self.set_sub_tag("totalUniqueOcids", generate_key_leaf_tag("totalUniqueOcids"))
        self.set_sub_tag("processingStart", generate_timestamp_leaf_tag("processingStart", "%Y-%m-%d %H.%M.%S"))
        self.set_sub_tag("processingEnd", generate_timestamp_leaf_tag("processingEnd", "%Y-%m-%d %H.%M.%S"))
        self.set_sub_tag("collectingStart", generate_timestamp_leaf_tag("collectingStart", "%Y-%m-%d %H.%M.%S"))
        self.set_sub_tag("collectingEnd", generate_timestamp_leaf_tag("collectingEnd", "%Y-%m-%d %H.%M.%S"))

        self.set_sub_tag("lifecycleObjectCount", LifecycleObjectCountLeafTag)
        self.set_sub_tag("releaseDateCount", ReleaseDateCountLeafTag)

        self.set_sub_tag("lifecycleImage", LifecycleImageLeafTag)
        self.set_sub_tag("releaseDateDistributionImage", ReleaseDateDistributionImageLeafTag)

    def prepare_data(self, data):
        dataset = Dataset.objects.filter(id=self.dataset_id).first()

        return {
            "id": dataset.id,
            "ancestorId": dataset.ancestor_id,  # TODO
            "url": dataset.meta["collection_metadata"]["url"],
            "publisher": dataset.meta["collection_metadata"]["publisher"],
            "publishingStart": dataset.meta["collection_metadata"]["published_from"],
            "publishingEnd": dataset.meta["collection_metadata"]["published_to"],
            "ocidPrefix": dataset.meta["collection_metadata"]["ocid_prefix"],
            "dataLicense": dataset.meta["collection_metadata"]["data_license"],
            "totalUniqueOcids": dataset.meta["compiled_releases"]["total_unique_ocids"],
            "processingStart": dataset.meta["data_quality_tool_metadata"]["processing_start"],
            "processingEnd": dataset.meta["data_quality_tool_metadata"]["processing_end"],
            "collectingStart": dataset.meta["kingfisher_metadata"]["processing_start"],
            "collectingEnd": dataset.meta["kingfisher_metadata"]["processing_end"],
            "lifecycle_object_counts": dataset.meta["tender_lifecycle"],
            "period_pairs": [(period["date_str"], period["count"]) for period in dataset.meta["period"]],
        }
