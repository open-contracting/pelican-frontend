from typing import TYPE_CHECKING, Any

from exporter import graphs
from exporter.tag import LeafTag, argument, leaf
from exporter.util import box_image

if TYPE_CHECKING:
    from lxml import etree


@argument("stage", required=True, choices={"planning", "tender", "award", "contract", "implementation"})
@leaf("lifecycleObjectCount")
def lifecycle_object_count(tag: LeafTag, data: dict[str, Any]) -> str:
    return str(data["lifecycleObjectCounts"][tag.arguments["stage"]])


@leaf("lifecycleImage")
def lifecycle_image(tag: LeafTag, data: dict[str, Any]) -> etree._Element:
    return box_image(
        tag,
        graphs.lifecycle_image,
        "LifecycleImage.png",
        data["lifecycleObjectCounts"]["planning"],
        data["lifecycleObjectCounts"]["tender"],
        data["lifecycleObjectCounts"]["award"],
        data["lifecycleObjectCounts"]["contract"],
        data["lifecycleObjectCounts"]["implementation"],
    )
