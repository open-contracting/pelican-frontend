from typing import Any  # noqa: A005

from lxml import etree

from exporter import graphs
from exporter.tag import LeafTag, leaf
from exporter.util import box_image


@leaf("resultBoxImage")
def result_box_image(tag: LeafTag, data: dict[str, Any]) -> etree._Element:
    return box_image(
        tag,
        graphs.resource_result_box,
        f"resultBoxImage_{data['name']}.png",
        [data["passedCount"], data["failedCount"], data["notAvailableCount"]],
    )
