from typing import Any

from api.models import DatasetLevelCheck
from django.conf import settings
from django.utils.translation import gettext as _

from exporter.exceptions import CheckNotComputedError
from exporter.gdocs import Gdocs
from exporter.leaf_tags.dataset import (
    bar_count,
    bar_examples,
    bar_share,
    bar_sum,
    buyer_count,
    counts_result_box_image,
    donut_count,
    donut_examples,
    donut_share,
    ocid_count,
    passed_result_box_image,
    result,
    sums_result_box_image,
    table_result_box_image,
    top3_amount,
    top3_count,
    top3_examples,
    top3_share,
)
from exporter.leaf_tags.dataset import value as value_tag
from exporter.leaf_tags.generic import generate_key_leaf_tag, generate_sample_leaf_tag
from exporter.tag import Tag, TemplateTag
from exporter.util import quote_list

# Keep in sync with checkTypes in datasetMixins.js
CHECK_TYPES = {
    # donut
    "distribution.main_procurement_category": "donut",
    "distribution.tender_status": "donut",
    "distribution.tender_procurement_method": "donut",
    "distribution.tender_award_criteria": "donut",
    "distribution.tender_submission_method": "donut",
    "distribution.awards_status": "donut",
    "distribution.contracts_status": "donut",
    "distribution.milestone_status": "donut",
    "distribution.milestone_type": "donut",
    "distribution.document_document_type": "donut",
    "distribution.value_currency": "donut",
    "distribution.related_process_relation": "donut",
    # bar
    "distribution.tender_value": "bar",
    "distribution.contracts_value": "bar",
    "distribution.awards_value": "bar",
    # numeric
    "misc.url_availability": "numeric",
    "unique.tender_id": "numeric",
    "consistent.related_process_title": "numeric",
    "reference.related_process_identifier": "numeric",
    # top3
    "distribution.tender_value_repetition": "top3",
    "distribution.contracts_value_repetition": "top3",
    "distribution.awards_value_repetition": "top3",
    # biggest_share
    "distribution.buyer_repetition": "biggest_share",
    # single_value_share
    "distribution.buyer": "single_value_share",
}


class Dataset(TemplateTag):
    name = "dataset"
    argument_names = set()
    argument_required = set()
    argument_validators = {}
    argument_validation_messages = {}
    argument_converters = {}
    argument_defaults = {}

    default_template = settings.GDOCS_TEMPLATES["DEFAULT_DATASET_TEMPLATE"]
    tags: tuple[type[Tag], ...] = (
        generate_key_leaf_tag("name"),
        generate_key_leaf_tag("description"),
        result,
        value_tag,
    )

    def __init__(self, gdocs: Gdocs, dataset_id: int):
        super().__init__(gdocs, dataset_id)
        self.argument_names.add("check")
        self.argument_required.add("check")
        self.argument_validators["check"] = lambda v: v in CHECK_TYPES
        self.argument_validation_messages["check"] = f"The value must be one of: {quote_list(CHECK_TYPES)}."

    def finalize_arguments(self) -> None:
        check_name = self.arguments["check"]
        check_type = CHECK_TYPES[check_name]
        check = DatasetLevelCheck.objects.filter(dataset=self.dataset_id, check_name=check_name).first()

        if check.result is not None:
            if check_type == "donut":
                self.tags += (donut_share, donut_count, donut_examples, counts_result_box_image)
            elif check_type == "bar":
                self.tags += (bar_share, bar_count, bar_examples, bar_sum, sums_result_box_image)
            elif check_type == "top3":
                self.tags += (top3_share, top3_count, top3_examples, top3_amount, table_result_box_image)
            elif check_type == "numeric":
                self.tags += (
                    generate_key_leaf_tag("checkedCount"),
                    generate_key_leaf_tag("passedCount"),
                    generate_key_leaf_tag("failedCount"),
                    generate_sample_leaf_tag("passedExamples"),
                    generate_sample_leaf_tag("failedExamples"),
                    passed_result_box_image,
                )
            elif check_type == "biggest_share":
                self.tags += (
                    generate_key_leaf_tag("buyerIdentifierId"),
                    generate_key_leaf_tag("buyerIdentifierScheme"),
                    generate_key_leaf_tag("ocidCount"),
                    generate_key_leaf_tag("ocidShare"),
                    generate_key_leaf_tag("totalOcidCount"),
                    generate_sample_leaf_tag("examples"),
                )
            elif check_type == "single_value_share":
                self.tags += (
                    ocid_count,
                    buyer_count,
                    generate_key_leaf_tag("totalOcidCount"),
                    generate_key_leaf_tag("totalBuyerCount"),
                    generate_sample_leaf_tag("examples"),
                )
        else:
            raise CheckNotComputedError(check_name)

        super().finalize_arguments()

    def get_context(self) -> dict[str, Any]:
        check_name = self.arguments["check"]
        check_type = CHECK_TYPES[check_name]
        check = DatasetLevelCheck.objects.filter(dataset=self.dataset_id, check_name=check_name).first()

        data = {
            "name": _(str("dataset." + check_name + ".name")),
            "description": _(str("dataset." + check_name + ".description")),
            "result": check.result,
            "value": check.value,
        }

        if check.result is not None:
            if check_type == "donut":
                if check.result is not None:
                    data["shares"] = {key: value["share"] for key, value in check.meta["shares"].items()}
                    data["counts"] = {key: value["count"] for key, value in check.meta["shares"].items()}
                    data["counts_pairs"] = [(key, value["count"]) for key, value in check.meta["shares"].items()]
                    data["examples"] = {
                        key: [example["ocid"] for example in value["examples"]]
                        for key, value in check.meta["shares"].items()
                    }
                else:
                    data["shares"] = {}
                    data["counts"] = {}
                    data["counts_pairs"] = []
                    data["examples"] = {}
            elif check_type == "bar":
                if check.result is not None:
                    data["shares"] = {key.replace("_", "-"): value for key, value in check.meta["shares"].items()}
                    data["counts"] = {key.replace("_", "-"): value for key, value in check.meta["counts"].items()}
                    data["sums"] = {key.replace("_", "-"): value for key, value in check.meta["sums"].items()}
                    data["sums_pairs"] = [(key.replace("_", "-"), value) for key, value in check.meta["sums"].items()]
                    data["examples"] = {
                        key.replace("_", "-"): [example["ocid"] for example in examples]
                        for key, examples in check.meta["examples"].items()
                    }
                else:
                    data["shares"] = {}
                    data["counts"] = {}
                    data["sums"] = {}
                    data["sums_pairs"] = []
                    data["examples"] = {}
            elif check_type == "top3":
                data["shares"] = {str(index + 1): el["share"] for index, el in enumerate(check.meta["most_frequent"])}
                data["counts"] = {str(index + 1): el["count"] for index, el in enumerate(check.meta["most_frequent"])}
                data["counts_pairs"] = [(el["value_str"], el["count"]) for el in check.meta["most_frequent"]]
                data["total_count"] = check.meta["total_processed"]
                data["examples"] = {
                    str(index + 1): [example["ocid"] for example in el["examples"]]
                    for index, el in enumerate(check.meta["most_frequent"])
                }
                data["amounts"] = {
                    str(index + 1): el["value_str"] for index, el in enumerate(check.meta["most_frequent"])
                }
            elif check_type == "numeric":
                data["checkedCount"] = check.meta["total_processed"]
                data["passedCount"] = check.meta["total_passed"]
                data["failedCount"] = check.meta["total_failed"]
                data["passedExamples"] = [example["ocid"] for example in check.meta["passed_examples"]]
                data["failedExamples"] = [example["ocid"] for example in check.meta["failed_examples"]]
            elif check_type == "biggest_share":
                data["buyerIdentifierId"] = check.meta["specifics"]["buyer.identifier.id"]
                data["buyerIdentifierScheme"] = check.meta["specifics"]["buyer.identifier.scheme"]
                data["ocidCount"] = check.meta["ocid_count"]
                data["ocidShare"] = check.meta["ocid_share"]
                data["totalOcidCount"] = check.meta["total_ocid_count"]
                data["examples"] = [example["ocid"] for example in check.meta["examples"]]
            elif check_type == "single_value_share":
                data["ocidCounts"] = {
                    key.replace("_", "-"): value["total_ocid_count"] for key, value in check.meta["counts"].items()
                }
                data["buyerCounts"] = {
                    key.replace("_", "-"): value["total_buyer_count"] for key, value in check.meta["counts"].items()
                }
                data["totalOcidCount"] = check.meta["total_ocid_count"]
                data["totalBuyerCount"] = check.meta["total_buyer_count"]
                data["examples"] = [example["ocid"] for example in check.meta["examples"]]

        return data
