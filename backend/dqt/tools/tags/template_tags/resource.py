
from django.db import connections
from dqt.tools.tags.tag import TemplateTag
from dqt.tools.tags.leaf_tags.name import NameLeafTag
from dqt.tools.tags.leaf_tags.description import DescriptionLeafTag
from dqt.tools.tags.leaf_tags.resource.checked_count import CheckedCountLeafTag
from dqt.tools.tags.leaf_tags.resource.passed_count import PassedCountLeafTag
from dqt.tools.tags.leaf_tags.resource.failed_count import FailedCountLeafTag
from dqt.tools.tags.leaf_tags.resource.not_available_count import NotAvailableCountLeafTag
from dqt.tools.tags.leaf_tags.resource.result_box_image import ResultBoxImageLeafTag
from dqt.tools.tags.leaf_tags.resource.passed_examples import PassedExamplesLeafTag
from dqt.tools.tags.leaf_tags.resource.failed_examples import FailedExamplesLeafTag
from dqt.tools.tags.leaf_tags.resource.not_available_examples import NotAvailableExamplesLeafTag


class ResourceTemplateTag(TemplateTag):
    CHECKS = set([
        "consistent.number_of_tenderers",
        "consistent.tender_value",
        "consistent.contracts_value",
        "consistent.parties_roles",
        "consistent.supplier_in_parties_roles",
        "consistent.tenderer_in_parties_roles",
        "consistent.buyer_in_parties_roles",
        "consistent.procuring_entity_in_parties_roles",
        "consistent.payer_in_parties_roles",
        "consistent.payee_in_parties_roles",
        "consistent.contracts_implementation_transactions_value",
        "consistent.period_duration_in_days",
        "consistent.supplier_name_in_parties",
        "consistent.tenderer_name_in_parties",
        "consistent.buyer_name_in_parties",
        "consistent.procuring_entity_name_in_parties",
        "consistent.payer_name_in_parties",
        "consistent.payee_name_in_parties",
        "reference.supplier_in_parties",
        "reference.tenderer_in_parties",
        "reference.buyer_in_parties",
        "reference.procuring_entity_in_parties",
        "reference.payer_in_parties",
        "reference.payee_in_parties",
        "reference.contract_in_awards",
        "coherent.procurement_method_vs_number_of_tenderers",
        "coherent.tender_status",
        "coherent.period",
        "coherent.dates",
        "coherent.contracts_status",
        "coherent.awards_status",
        "coherent.milestones_dates",
        "coherent.milestone_status",
        "coherent.amendments_dates",
        "coherent.documents_dates",
        "coherent.value_realistic",
    ])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.prepare_data,
            '1ZgKP1TWU8AbnOFhjEqlBO--lR71dAlNMyiGDUh8MZ-8',
            gdocs,
            dataset_id
        )

        # TODO: check if check was calculated
        self.set_param_validation('check', lambda v: v in ResourceTemplateTag.CHECKS, required=True)

        self.set_sub_tag('name', NameLeafTag)
        self.set_sub_tag('description', DescriptionLeafTag)
        self.set_sub_tag('checkedCount', CheckedCountLeafTag)
        self.set_sub_tag('passedCount', PassedCountLeafTag)
        self.set_sub_tag('failedCount', FailedCountLeafTag)
        self.set_sub_tag('notAvailableCount', NotAvailableCountLeafTag)
        self.set_sub_tag('resultBoxImage', ResultBoxImageLeafTag)
        self.set_sub_tag('passedExamples', PassedExamplesLeafTag)
        self.set_sub_tag('failedExamples', FailedExamplesLeafTag)
        self.set_sub_tag('notAvailableExamples', NotAvailableExamplesLeafTag)
    
    def prepare_data(self):
        check_name = self.get_param('check')
        with connections["data"].cursor() as cursor:
            cursor.execute(
                """
                select data->%s
                from report
                where dataset_id = %s and
                    type = 'resource_level_check' and
                    data ? %s;
                """, [check_name, self.dataset_id, check_name]
            )
            rows = cursor.fetchall()

            # TODO
            # if not rows:
            #     continue

            result_report = rows[0][0]

            # getting examples
            cursor.execute(
                """
                select data
                from resource_level_check_examples
                where dataset_id = %s and
                    check_name = %s;
                """, [self.dataset_id, check_name]
            )
            result_examples = cursor.fetchall()[0][0]
            result = {**result_report, **result_examples}

            # TODO: no rows retrieved
            return {
                "name": check_name, # TODO: temporary
                "description": "placeholder", # TODO: placeholder
                "checkedCount": result['total_count'],
                "passedCount": result['passed_count'],
                "failedCount": result['failed_count'],
                "notAvailableCount": result['undefined_count'],
                "passedExamples": [example['meta']['ocid'] for example in result['passed_examples']],
                "failedExamples": [example['meta']['ocid'] for example in result['failed_examples']],
                "notAvailableExamples": [example['meta']['ocid'] for example in result['undefined_examples']],
            }