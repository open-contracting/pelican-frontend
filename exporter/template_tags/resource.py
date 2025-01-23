from typing import Any  # noqa: A005

from django.conf import settings
from django.utils.translation import gettext as _

from api.models import Report, ResourceLevelCheckExamples
from exporter.leaf_tags.generic import generate_key_leaf_tag, generate_sample_leaf_tag
from exporter.leaf_tags.resource import result_box_image
from exporter.tag import TemplateTag, argument, template

CHECKS = {
    "coherent.amendments_dates",
    "coherent.awards_status",
    "coherent.contracts_status",
    "coherent.dates",
    "coherent.documents_dates",
    "coherent.milestone_status",
    "coherent.milestones_dates",
    "coherent.period",
    "coherent.procurement_method_vs_number_of_tenderers",
    "coherent.release_date",
    "coherent.tender_status",
    "coherent.value_realistic",
    "consistent.buyer_in_parties_roles",
    "consistent.buyer_name_in_parties",
    "consistent.contracts_implementation_transactions_value",
    "consistent.contracts_value",
    "consistent.number_of_tenderers",
    "consistent.parties_roles",
    "consistent.payee_in_parties_roles",
    "consistent.payee_name_in_parties",
    "consistent.payer_in_parties_roles",
    "consistent.payer_name_in_parties",
    "consistent.period_duration_in_days",
    "consistent.procuring_entity_in_parties_roles",
    "consistent.procuring_entity_name_in_parties",
    "consistent.supplier_in_parties_roles",
    "consistent.supplier_name_in_parties",
    "consistent.tender_value",
    "consistent.tenderer_in_parties_roles",
    "consistent.tenderer_name_in_parties",
    "reference.buyer_in_parties",
    "reference.contract_in_awards",
    "reference.payee_in_parties",
    "reference.payer_in_parties",
    "reference.procuring_entity_in_parties",
    "reference.supplier_in_parties",
    "reference.tenderer_in_parties",
}


@argument("check", required=True, choices=CHECKS)
@template(
    "resource",
    settings.GDOCS_TEMPLATES["DEFAULT_RESOURCE_TEMPLATE"],
    (
        generate_key_leaf_tag("name"),
        generate_key_leaf_tag("description"),
        generate_key_leaf_tag("checkedCount"),
        generate_key_leaf_tag("passedCount"),
        generate_key_leaf_tag("failedCount"),
        generate_key_leaf_tag("notAvailableCount"),
        generate_sample_leaf_tag("passedExamples"),
        generate_sample_leaf_tag("failedExamples"),
        generate_sample_leaf_tag("notAvailableExamples"),
        result_box_image,
    ),
)
def resource(tag: TemplateTag) -> dict[str, Any]:
    name = tag.arguments["check"]

    result = Report.objects.get(dataset=tag.dataset_id, type="resource_level_check", data__has_key=name).data[name]
    examples = ResourceLevelCheckExamples.objects.get(dataset=tag.dataset_id, check_name=name).data

    result.update(examples)

    return {
        "name": _(str("resource." + name + ".name")),
        "description": _(str("resource." + name + ".description")),
        "checkedCount": result["total_count"],
        "passedCount": result["passed_count"],
        "failedCount": result["failed_count"],
        "notAvailableCount": result["undefined_count"],
        "passedExamples": [example["meta"]["ocid"] for example in result["passed_examples"]],
        "failedExamples": [example["meta"]["ocid"] for example in result["failed_examples"]],
        "notAvailableExamples": [example["meta"]["ocid"] for example in result["undefined_examples"]],
    }
