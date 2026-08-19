from typing import Any

from lxml import etree

from exporter import graphs
from exporter.messages import message
from exporter.tag import LeafTag, argument, leaf
from exporter.util import LEVELS, MODES, box_image, sample_and_format


@argument("level", required=True, choices={"coverageSet", "coverageEmpty", "quality"})
@leaf("name")
def name(tag: LeafTag, data: dict[str, Any]) -> str:
    if tag.arguments["level"] == "quality" and data["qualityCheck"] is None:
        return ""
    if tag.arguments["level"] == "coverageSet":
        return message(tag.language, "fieldDetail", "coverage", "exists", "name")
    if tag.arguments["level"] == "coverageEmpty":
        return message(tag.language, "fieldDetail", "coverage", "non_empty", "name")
    return message(tag.language, "fieldDetail", "quality", data["qualityCheck"], "name")


@argument("level", required=True, choices={"coverageSet", "coverageEmpty", "quality"})
@leaf("description")
def description(tag: LeafTag, data: dict[str, Any]) -> str:
    if tag.arguments["level"] == "quality" and data["qualityCheck"] is None:
        return ""
    if tag.arguments["level"] == "coverageSet":
        return message(tag.language, "fieldDetail", "coverage", "exists", "description")
    if tag.arguments["level"] == "coverageEmpty":
        return message(tag.language, "fieldDetail", "coverage", "non_empty", "description")
    return message(tag.language, "fieldDetail", "quality", data["qualityCheck"], "description")


@argument("level", required=True, choices=LEVELS)
@argument("mode", choices=MODES, default="oneLine")
@argument("max", type=int, nonzero=True)
@leaf("passedExamples")
def passed_examples(tag: LeafTag, data: dict[str, Any]) -> str | list[etree._Element]:
    examples = data[f"{tag.arguments['level']}PassedExamples"]
    return sample_and_format(examples, tag.arguments)


@argument("level", required=True, choices=LEVELS)
@argument("mode", choices=MODES, default="oneLine")
@argument("max", type=int, nonzero=True)
@leaf("failedExamples")
def failed_examples(tag: LeafTag, data: dict[str, Any]) -> str | list[etree._Element]:
    examples = data[f"{tag.arguments['level']}FailedExamples"]
    return sample_and_format(examples, tag.arguments)


@argument("level", required=True, choices=LEVELS)
@leaf("resultBoxImage")
def result_box_image(tag: LeafTag, data: dict[str, Any]) -> etree._Element:
    return box_image(
        tag,
        graphs.passed_result_box,
        f"resultBoxImage_{tag.arguments['level']}_{data['path']}.png",
        [data[f"{tag.arguments['level']}PassedCount"], data[f"{tag.arguments['level']}FailedCount"]],
    )
