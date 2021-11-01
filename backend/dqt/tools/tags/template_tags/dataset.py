from django.utils.translation import gettext as _
from dqt.models import DatasetLevelCheck
from dqt.settings import GDOCS_TEMPLATES
from dqt.tools.errors import CheckNotComputedError
from dqt.tools.misc import terms_enumeration
from dqt.tools.tags.leaf_tags.dataset.bar.count import CountLeafTag as bar_CountLeafTag
from dqt.tools.tags.leaf_tags.dataset.bar.examples import ExamplesLeafTag as bar_ExamplesLeafTag
from dqt.tools.tags.leaf_tags.dataset.bar.share import ShareLeafTag as bar_ShareLeafTag
from dqt.tools.tags.leaf_tags.dataset.bar.sum import SumLeafTag as bar_SumLeafTag
from dqt.tools.tags.leaf_tags.dataset.counts_result_box_image import CountsResultBoxImageLeafTag
from dqt.tools.tags.leaf_tags.dataset.donut.count import CountLeafTag as donut_CountLeafTag
from dqt.tools.tags.leaf_tags.dataset.donut.examples import ExamplesLeafTag as donut_ExamplesLeafTag
from dqt.tools.tags.leaf_tags.dataset.donut.share import ShareLeafTag as donut_ShareLeafTag
from dqt.tools.tags.leaf_tags.dataset.passed_result_box_image import PassedResultBoxImageLeafTag
from dqt.tools.tags.leaf_tags.dataset.result import ResultLeafTag
from dqt.tools.tags.leaf_tags.dataset.single_value_share.buyer_count import (
    BuyerCountLeafTag as single_value_share_BuyerCountLeafTag,
)
from dqt.tools.tags.leaf_tags.dataset.single_value_share.ocid_count import (
    OcidCountLeafTag as single_value_share_OcidCountLeafTag,
)
from dqt.tools.tags.leaf_tags.dataset.table_result_box_image import TableResultBoxImageLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.amount import AmountLeafTag as top3_AmountLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.count import CountLeafTag as top3_CountLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.examples import ExamplesLeafTag as top3_ExamplesLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.share import ShareLeafTag as top3_ShareLeafTag
from dqt.tools.tags.leaf_tags.dataset.value import ValueLeafTag
from dqt.tools.tags.leaf_tags.examples_leaf_tag_factory import generate_examples_leaf_tag
from dqt.tools.tags.leaf_tags.key_leaf_tag_factory import generate_key_leaf_tag
from dqt.tools.tags.tag import TemplateTag


class DatasetTemplateTag(TemplateTag):
    CHECK_MAPPING = {
        "distribution.main_procurement_category": {"check_type": "donut", "version": 1},
        "distribution.tender_status": {"check_type": "donut", "version": 1},
        "distribution.tender_procurement_method": {"check_type": "donut", "version": 1},
        "distribution.tender_award_criteria": {"check_type": "donut", "version": 1},
        "distribution.tender_submission_method": {"check_type": "donut", "version": 1},
        "distribution.awards_status": {"check_type": "donut", "version": 1},
        "distribution.contracts_status": {"check_type": "donut", "version": 1},
        "distribution.milestone_status": {"check_type": "donut", "version": 1},
        "distribution.milestone_type": {"check_type": "donut", "version": 1},
        "distribution.document_document_type": {"check_type": "donut", "version": 1},
        "distribution.value_currency": {"check_type": "donut", "version": 1},
        "distribution.related_process_relation": {"check_type": "donut", "version": 1},
        "distribution.tender_value": {"check_type": "bar", "version": 1},
        "distribution.contracts_value": {"check_type": "bar", "version": 1},
        "distribution.awards_value": {"check_type": "bar", "version": 1},
        "misc.url_availability": {"check_type": "numeric", "version": 1},
        "unique.tender_id": {"check_type": "numeric", "version": 2},
        "consistent.related_process_title": {"check_type": "numeric", "version": 1},
        "reference.related_process_identifier": {"check_type": "numeric", "version": 2},
        "distribution.tender_value_repetition": {"check_type": "top3", "version": 1},
        "distribution.contracts_value_repetition": {"check_type": "top3", "version": 1},
        "distribution.awards_value_repetition": {"check_type": "top3", "version": 1},
        "distribution.buyer_repetition": {"check_type": "biggest_share", "version": 1},
        "distribution.buyer": {"check_type": "single_value_share", "version": 1},
    }

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.prepare_data, GDOCS_TEMPLATES["DEFAULT_DATASET_TEMPLATE"], gdocs, dataset_id)

        # TODO: check if check was calculated and version compatability
        self.set_param_validation(
            "check",
            lambda v: v in DatasetTemplateTag.CHECK_MAPPING,
            description="The value must be one of the following: %s."
            % terms_enumeration(DatasetTemplateTag.CHECK_MAPPING),
            required=True,
        )

        self.set_sub_tag("name", generate_key_leaf_tag("name"))
        self.set_sub_tag("description", generate_key_leaf_tag("description"))
        self.set_sub_tag("result", ResultLeafTag)
        self.set_sub_tag("value", ValueLeafTag)

    def finalize_params(self):
        check_name = self.get_param("check")
        check_type = DatasetTemplateTag.CHECK_MAPPING[check_name]["check_type"]
        check = DatasetLevelCheck.objects.filter(dataset=self.dataset_id, check_name=check_name).first()

        if check.result is not None:
            if check_type == "donut":
                self.set_sub_tag("share", donut_ShareLeafTag)
                self.set_sub_tag("count", donut_CountLeafTag)
                self.set_sub_tag("examples", donut_ExamplesLeafTag)
                self.set_sub_tag("resultBoxImage", CountsResultBoxImageLeafTag)

            elif check_type == "bar":
                self.set_sub_tag("share", bar_ShareLeafTag)
                self.set_sub_tag("count", bar_CountLeafTag)
                self.set_sub_tag("examples", bar_ExamplesLeafTag)
                self.set_sub_tag("sum", bar_SumLeafTag)
                self.set_sub_tag("resultBoxImage", CountsResultBoxImageLeafTag)

            elif check_type == "top3":
                self.set_sub_tag("share", top3_ShareLeafTag)
                self.set_sub_tag("count", top3_CountLeafTag)
                self.set_sub_tag("examples", top3_ExamplesLeafTag)
                self.set_sub_tag("amount", top3_AmountLeafTag)
                self.set_sub_tag("resultBoxImage", TableResultBoxImageLeafTag)

            elif check_type == "numeric":
                self.set_sub_tag("checkedCount", generate_key_leaf_tag("checkedCount"))
                self.set_sub_tag("passedCount", generate_key_leaf_tag("passedCount"))
                self.set_sub_tag("failedCount", generate_key_leaf_tag("failedCount"))

                self.set_sub_tag("passedExamples", generate_examples_leaf_tag("passedExamples"))
                self.set_sub_tag("failedExamples", generate_examples_leaf_tag("failedExamples"))
                self.set_sub_tag("resultBoxImage", PassedResultBoxImageLeafTag)

            elif check_type == "biggest_share":
                self.set_sub_tag("buyerIdentifierId", generate_key_leaf_tag("buyerIdentifierId"))
                self.set_sub_tag("buyerIdentifierScheme", generate_key_leaf_tag("buyerIdentifierScheme"))
                self.set_sub_tag("ocidCount", generate_key_leaf_tag("ocidCount"))
                self.set_sub_tag("ocidShare", generate_key_leaf_tag("ocidShare"))
                self.set_sub_tag("totalOcidCount", generate_key_leaf_tag("totalOcidCount"))

                self.set_sub_tag("examples", generate_examples_leaf_tag("examples"))
                # self.set_sub_tag('resultBoxImage')

            elif check_type == "single_value_share":
                self.set_sub_tag("ocidCount", single_value_share_OcidCountLeafTag)
                self.set_sub_tag("buyerCount", single_value_share_BuyerCountLeafTag)
                self.set_sub_tag("totalOcidCount", generate_key_leaf_tag("totalOcidCount"))
                self.set_sub_tag("totalBuyerCount", generate_key_leaf_tag("totalBuyerCount"))
                self.set_sub_tag("examples", generate_examples_leaf_tag("examples"))
        else:  # check not found
            raise CheckNotComputedError(reason="Check was not computed", check=check_name)

        super().finalize_params()

    def prepare_data(self, data):
        check_name = self.get_param("check")
        check_type = DatasetTemplateTag.CHECK_MAPPING[check_name]["check_type"]

        new_data = {}
        check = DatasetLevelCheck.objects.filter(dataset=self.dataset_id, check_name=check_name).first()

        new_data["name"] = _(str("dataset." + check_name + ".name"))
        new_data["description"] = _(str("dataset." + check_name + ".description"))
        new_data["result"] = check.result
        new_data["value"] = check.value

        if check.result is not None:
            if check_type == "donut":
                if check.result is not None:
                    new_data["shares"] = {key: value["share"] for key, value in check.meta["shares"].items()}
                    new_data["counts"] = {key: value["count"] for key, value in check.meta["shares"].items()}
                    new_data["counts_pairs"] = [(key, value["count"]) for key, value in check.meta["shares"].items()]
                    new_data["examples"] = {
                        key: [example["ocid"] for example in value["examples"]]
                        for key, value in check.meta["shares"].items()
                    }
                else:
                    new_data["shares"] = {}
                    new_data["counts"] = {}
                    new_data["counts_pairs"] = []
                    new_data["examples"] = {}

            elif check_type == "bar":
                if check.result is not None:
                    new_data["shares"] = {key.replace("_", "-"): value for key, value in check.meta["shares"].items()}
                    new_data["counts"] = {key.replace("_", "-"): value for key, value in check.meta["counts"].items()}
                    new_data["counts_pairs"] = [
                        (key.replace("_", "-"), value) for key, value in check.meta["counts"].items()
                    ]
                    new_data["examples"] = {
                        key.replace("_", "-"): [example["ocid"] for example in examples]
                        for key, examples in check.meta["examples"].items()
                    }
                    new_data["sums"] = {key.replace("_", "-"): value for key, value in check.meta["sums"].items()}
                else:
                    new_data["shares"] = {}
                    new_data["counts"] = {}
                    new_data["counts_pairs"] = []
                    new_data["examples"] = {}
                    new_data["sums"] = {}
            elif check_type == "top3":
                new_data["shares"] = {
                    str(index + 1): el["share"] for index, el in enumerate(check.meta["most_frequent"])
                }
                new_data["counts"] = {
                    str(index + 1): el["count"] for index, el in enumerate(check.meta["most_frequent"])
                }
                new_data["counts_pairs"] = [(el["value_str"], el["count"]) for el in check.meta["most_frequent"]]
                new_data["total_count"] = check.meta["total_processed"]
                new_data["examples"] = {
                    str(index + 1): [example["ocid"] for example in el["examples"]]
                    for index, el in enumerate(check.meta["most_frequent"])
                }
                new_data["amounts"] = {
                    str(index + 1): el["value_str"] for index, el in enumerate(check.meta["most_frequent"])
                }
            elif check_type == "numeric":
                new_data["checkedCount"] = check.meta["total_processed"]
                new_data["passedCount"] = check.meta["total_passed"]
                new_data["failedCount"] = check.meta["total_failed"]
                new_data["passedExamples"] = [
                    example["original_process"]["ocid"] if "original_process" in example else example["ocid"]
                    for example in check.meta["passed_examples"]
                ]
                new_data["failedExamples"] = [
                    example["original_process"]["ocid"] if "original_process" in example else example["ocid"]
                    for example in check.meta["failed_examples"]
                ]
            elif check_type == "biggest_share":
                new_data["buyerIdentifierId"] = check.meta["specifics"]["buyer.identifier.id"]
                new_data["buyerIdentifierScheme"] = check.meta["specifics"]["buyer.identifier.scheme"]
                new_data["ocidCount"] = check.meta["ocid_count"]
                new_data["ocidShare"] = check.meta["ocid_share"]
                new_data["totalOcidCount"] = check.meta["total_ocid_count"]
                new_data["examples"] = [example["ocid"] for example in check.meta["examples"]]

            elif check_type == "single_value_share":
                new_data["ocidCounts"] = {
                    key.replace("_", "-"): value["total_ocid_count"] for key, value in check.meta["counts"].items()
                }
                new_data["buyerCounts"] = {
                    key.replace("_", "-"): value["total_buyer_count"] for key, value in check.meta["counts"].items()
                }
                new_data["totalOcidCount"] = check.meta["total_ocid_count"]
                new_data["totalBuyerCount"] = check.meta["total_buyer_count"]
                new_data["examples"] = [example["ocid"] for example in check.meta["examples"]]

        return new_data
