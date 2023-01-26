from typing import Any, Dict, Generator, Optional, Tuple

import jsonref
from django.conf import settings

from api.models import FieldLevelCheckExamples, Report
from exporter.decorators import argument, template
from exporter.leaf_tags.field import description, failed_examples, name, passed_examples, result_box_image
from exporter.leaf_tags.generic import generate_count_leaf_tag, generate_key_leaf_tag
from exporter.tag import TemplateTag


# See similar code in Pelican backend's field_level/definitions.py.
def _descend(
    value: Dict[str, Any], new_path: Tuple[str, ...], dot_path: str, refs: Tuple[str, ...]
) -> Generator[str, None, None]:
    if hasattr(value, "__reference__"):
        refs += (value.__reference__["$ref"][14:],)  # remove #/definitions/

    yield dot_path
    yield from _paths(value["properties"], path=new_path, refs=refs)


def _paths(
    properties: Dict[str, Any], path: Optional[Tuple[str, ...]] = None, refs: Optional[Tuple[str, ...]] = None
) -> Generator[str, None, None]:
    if path is None:
        path = ()
    if refs is None:
        refs = ()

    for key, value in properties.items():
        new_path = path + (key,)
        dot_path = ".".join(new_path)

        if "object" in value["type"] and "properties" in value:
            yield from _descend(value, new_path, dot_path, refs)
        elif (
            "array" in value["type"]
            and "items" in value
            and "object" in value["items"]["type"]
            and "properties" in value["items"]
        ):
            yield from _descend(value["items"], new_path, dot_path, refs)
        else:
            yield dot_path


with (settings.BASE_DIR / "release-schema.json").open() as f:
    schema = jsonref.load(f)

PATHS = set(_paths(schema["properties"]))


@argument("path", required=True, choices=PATHS)
@template(
    "field",
    settings.GDOCS_TEMPLATES["DEFAULT_FIELD_TEMPLATE"],
    (
        generate_key_leaf_tag("path"),
        name,
        description,
        generate_count_leaf_tag("Checked"),
        generate_count_leaf_tag("Passed"),
        generate_count_leaf_tag("Failed"),
        passed_examples,
        failed_examples,
        result_box_image,
    ),
)
def field(tag: TemplateTag) -> Dict[str, Any]:
    path = tag.arguments["path"]

    result = Report.objects.get(dataset=tag.dataset_id, type="field_level_check", data__has_key=path).data[path]
    examples = FieldLevelCheckExamples.objects.get(dataset=tag.dataset_id, path=path).data

    return {
        "path": path,
        "qualityCheck": list(result["quality"]["checks"])[0] if result["quality"]["checks"] else None,
        "coverageCheckedCount": result["coverage"]["total_count"],
        "coverageSetCheckedCount": result["coverage"]["checks"]["exists"]["total_count"],
        "coverageEmptyCheckedCount": result["coverage"]["checks"]["non_empty"]["total_count"],
        "qualityCheckedCount": result["quality"]["total_count"],
        "coveragePassedCount": result["coverage"]["passed_count"],
        "coverageSetPassedCount": result["coverage"]["checks"]["exists"]["passed_count"],
        "coverageEmptyPassedCount": result["coverage"]["checks"]["non_empty"]["passed_count"],
        "qualityPassedCount": result["quality"]["passed_count"],
        "coverageFailedCount": result["coverage"]["failed_count"],
        "coverageSetFailedCount": result["coverage"]["checks"]["exists"]["failed_count"],
        "coverageEmptyFailedCount": result["coverage"]["checks"]["non_empty"]["failed_count"],
        "qualityFailedCount": result["quality"]["failed_count"],
        "coveragePassedExamples": [example["meta"]["ocid"] for example in examples["coverage"]["passed_examples"]],
        "coverageSetPassedExamples": [
            example["meta"]["ocid"] for example in examples["coverage"]["checks"]["exists"]["passed_examples"]
        ],
        "coverageEmptyPassedExamples": [
            example["meta"]["ocid"] for example in examples["coverage"]["checks"]["non_empty"]["passed_examples"]
        ],
        "qualityPassedExamples": [example["meta"]["ocid"] for example in examples["quality"]["passed_examples"]],
        "coverageFailedExamples": [example["meta"]["ocid"] for example in examples["coverage"]["failed_examples"]],
        "coverageSetFailedExamples": [
            example["meta"]["ocid"] for example in examples["coverage"]["checks"]["exists"]["failed_examples"]
        ],
        "coverageEmptyFailedExamples": [
            example["meta"]["ocid"] for example in examples["coverage"]["checks"]["non_empty"]["failed_examples"]
        ],
        "qualityFailedExamples": [example["meta"]["ocid"] for example in examples["quality"]["failed_examples"]],
    }
