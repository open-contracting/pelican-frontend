from django.conf import settings
from django.db import connections
from django.utils.translation import gettext as _

from exporter.tags.leaf_tags.factories import generate_examples_leaf_tag, generate_key_leaf_tag
from exporter.tags.leaf_tags.resource.result_box_image import ResultBoxImageLeafTag
from exporter.tags.tag import TemplateTag
from exporter.util import terms_enumeration

CHECKS = {
    "coherent.period",
    "coherent.procurement_method_vs_number_of_tenderers",
    "coherent.tender_status",
    "coherent.awards_status",
    "coherent.contracts_status",
    "coherent.milestone_status",
    "coherent.value_realistic",
    "coherent.dates",
    "coherent.milestones_dates",
    "coherent.amendments_dates",
    "coherent.documents_dates",
    "consistent.number_of_tenderers",
    "consistent.tender_value",
    "consistent.contracts_value",
    "consistent.contracts_implementation_transactions_value",
    "consistent.parties_roles",
    "consistent.period_duration_in_days",
    "consistent.buyer_in_parties_roles",
    "consistent.supplier_in_parties_roles",
    "consistent.tenderer_in_parties_roles",
    "consistent.procuring_entity_in_parties_roles",
    "consistent.payer_in_parties_roles",
    "consistent.payee_in_parties_roles",
    "consistent.buyer_name_in_parties",
    "consistent.payee_name_in_parties",
    "consistent.payer_name_in_parties",
    "consistent.procuring_entity_name_in_parties",
    "consistent.supplier_name_in_parties",
    "consistent.tenderer_name_in_parties",
    "reference.buyer_in_parties",
    "reference.payee_in_parties",
    "reference.payer_in_parties",
    "reference.procuring_entity_in_parties",
    "reference.supplier_in_parties",
    "reference.tenderer_in_parties",
    "reference.contract_in_awards",
}


class ResourceTemplateTag(TemplateTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.prepare_data, settings.GDOCS_TEMPLATES["DEFAULT_RESOURCE_TEMPLATE"], gdocs, dataset_id)

        self.set_param_validation(
            "check",
            lambda v: v in CHECKS,
            description="The value must be one of the following: %s." % terms_enumeration(CHECKS),
            required=True,
        )

        self.set_sub_tag("name", generate_key_leaf_tag("name"))
        self.set_sub_tag("description", generate_key_leaf_tag("description"))
        self.set_sub_tag("checkedCount", generate_key_leaf_tag("checkedCount"))
        self.set_sub_tag("passedCount", generate_key_leaf_tag("passedCount"))
        self.set_sub_tag("failedCount", generate_key_leaf_tag("failedCount"))
        self.set_sub_tag("notAvailableCount", generate_key_leaf_tag("notAvailableCount"))

        self.set_sub_tag("resultBoxImage", ResultBoxImageLeafTag)
        self.set_sub_tag("passedExamples", generate_examples_leaf_tag("passedExamples"))
        self.set_sub_tag("failedExamples", generate_examples_leaf_tag("failedExamples"))
        self.set_sub_tag("notAvailableExamples", generate_examples_leaf_tag("notAvailableExamples"))

    def prepare_data(self, data):
        check_name = self.get_param("check")
        with connections["data"].cursor() as cursor:
            cursor.execute(
                """
                select data->%s
                from report
                where dataset_id = %s and
                    type = 'resource_level_check' and
                    data ? %s;
                """,
                [check_name, self.dataset_id, check_name],
            )
            rows = cursor.fetchall()
            result_report = rows[0][0]

            # getting examples
            cursor.execute(
                """
                select data
                from resource_level_check_examples
                where dataset_id = %s and
                    check_name = %s;
                """,
                [self.dataset_id, check_name],
            )
            result_examples = cursor.fetchall()[0][0]
            result = {**result_report, **result_examples}

            return {
                "name": _(str("resource." + check_name + ".name")),
                "description": _(str("resource." + check_name + ".description")),
                "checkedCount": result["total_count"],
                "passedCount": result["passed_count"],
                "failedCount": result["failed_count"],
                "notAvailableCount": result["undefined_count"],
                "passedExamples": [example["meta"]["ocid"] for example in result["passed_examples"]],
                "failedExamples": [example["meta"]["ocid"] for example in result["failed_examples"]],
                "notAvailableExamples": [example["meta"]["ocid"] for example in result["undefined_examples"]],
            }
