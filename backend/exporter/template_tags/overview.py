from typing import Any

from django.conf import settings

from api.models import Dataset
from exporter.leaf_tags.generic import generate_key_leaf_tag, generate_timestamp_leaf_tag
from exporter.leaf_tags.overview import lifecycle_image, lifecycle_object_count
from exporter.tag import TemplateTag, template


@template(
    "overview",
    settings.GDOCS_TEMPLATES["DEFAULT_OVERVIEW_TEMPLATE"],
    (
        generate_key_leaf_tag("id"),
        generate_key_leaf_tag("ancestorId"),
        generate_key_leaf_tag("publisher"),
        generate_key_leaf_tag("ocidPrefix"),
        generate_key_leaf_tag("dataLicense"),
        generate_key_leaf_tag("totalUniqueOcids"),
        # Note: The datetime formats must match DATETIME_STR_FORMAT in pelican-backend.
        generate_timestamp_leaf_tag("publishingStart", "%Y-%m-%d %H.%M.%S"),
        generate_timestamp_leaf_tag("publishingEnd", "%Y-%m-%d %H.%M.%S"),
        generate_timestamp_leaf_tag("processingStart", "%Y-%m-%d %H.%M.%S"),
        generate_timestamp_leaf_tag("processingEnd", "%Y-%m-%d %H.%M.%S"),
        generate_timestamp_leaf_tag("collectingStart", "%Y-%m-%d %H.%M.%S"),
        generate_timestamp_leaf_tag("collectingEnd", "%Y-%m-%d %H.%M.%S"),
        lifecycle_object_count,
        lifecycle_image,
    ),
)
def overview(tag: TemplateTag) -> dict[str, Any]:
    dataset = Dataset.objects.filter(id=tag.dataset_id).first()

    return {
        "id": dataset.id,
        "ancestorId": dataset.ancestor_id,
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
        "lifecycleObjectCounts": dataset.meta["tender_lifecycle"],
    }
