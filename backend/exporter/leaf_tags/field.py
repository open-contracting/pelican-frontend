from django.utils.translation import gettext as _

from exporter import graphs
from exporter.decorators import argument, leaf
from exporter.util import LEVELS, MODES, box_image, sample_and_format


@argument("level", required=True, choices={"coverageSet", "coverageEmpty", "quality"})
@leaf("name")
def name(tag, data):
    if tag.arguments["level"] == "quality" and data["qualityCheck"] is None:
        return ""
    if tag.arguments["level"] == "coverageSet":
        return _("field.exists.name")
    if tag.arguments["level"] == "coverageEmpty":
        return _("field.non_empty.name")
    return _(str("field." + data["qualityCheck"] + ".name"))


@argument("level", required=True, choices={"coverageSet", "coverageEmpty", "quality"})
@leaf("description")
def description(tag, data):
    if tag.arguments["level"] == "quality" and data["qualityCheck"] is None:
        return ""
    if tag.arguments["level"] == "coverageSet":
        return _("field.exists.description")
    if tag.arguments["level"] == "coverageEmpty":
        return _("field.non_empty.description")
    return _(str("field." + data["qualityCheck"] + ".description"))


@argument("level", required=True, choices=LEVELS)
@argument("mode", choices=MODES, default="oneLine")
@argument("max", type=int, nonzero=True)
@leaf("passedExamples")
def passed_examples(tag, data):
    examples = data[f"{tag.arguments['level']}PassedExamples"]
    return sample_and_format(examples, tag.arguments)


@argument("level", required=True, choices=LEVELS)
@argument("mode", choices=MODES, default="oneLine")
@argument("max", type=int, nonzero=True)
@leaf("failedExamples")
def failed_examples(tag, data):
    examples = data[f"{tag.arguments['level']}FailedExamples"]
    return sample_and_format(examples, tag.arguments)


@argument("level", required=True, choices=LEVELS)
@leaf("resultBoxImage")
def result_box_image(tag, data):
    return box_image(
        tag,
        graphs.passed_result_box,
        f"resultBoxImage_{tag.arguments['level']}_{data['path']}.png",
        data[f"{tag.arguments['level']}PassedCount"],
        data[f"{tag.arguments['level']}FailedCount"],
    )
