
from django.db import connections
from dqt.tools.misc import terms_enumeration
from dqt.tools.tags.tag import TemplateTag
from dqt.tools.tags.leaf_tags.key_leaf_tag_factory import generate_key_leaf_tag
from dqt.tools.tags.leaf_tags.examples_leaf_tag_factory import generate_examples_leaf_tag
from dqt.tools.tags.leaf_tags.resource.result_box_image import ResultBoxImageLeafTag


class ResourceTemplateTag(TemplateTag):
    CHECK_MAPPING = {
        "coherent.period": "Start dates aren't after end dates",
        "coherent.procurement_method_vs_number_of_tenderers": "At most one tenderer for sole sourcing",
        "coherent.tender_status": "No awards or contracts for incomplete tenders",
        "coherent.awards_status": "No contracts for inactive awards",
        "coherent.contracts_status": "No transactions for unsigned contracts",
        "coherent.milestone_status": "No date met for unmet milestones",
        "coherent.value_realistic": "Monetary values are realistic",
        "coherent.dates": "Contracting process timeline",
        "coherent.milestones_dates": "Milestone dates",
        "coherent.amendments_dates": "Amendment dates",
        "coherent.documents_dates": "Document dates",
        "consistent.number_of_tenderers": "Number of tenderers is consistent",
        "consistent.tender_value": "Planning budget is commensurate with tender value",
        "consistent.contracts_value": "Contract values are commensurate with award value",
        "consistent.contracts_implementation_transactions_value": "Transaction values are commensurate with contract value",
        "consistent.parties_roles": "Parties are referenced",
        "consistent.period_duration_in_days": "Period's duration is consistent with start and end dates",
        "consistent.buyer_in_parties_roles": "Buyer's role is set",
        "consistent.supplier_in_parties_roles": "Supplier's role is set",
        "consistent.tenderer_in_parties_roles": "Tenderer's role is set",
        "consistent.procuring_entity_in_parties_roles": "Procuring entity's role is set",
        "consistent.payer_in_parties_roles": "Payer's role is set",
        "consistent.payee_in_parties_roles": "Payee's role is set",
        "consistent.buyer_name_in_parties": "Buyer's name is consistent",
        "consistent.payee_name_in_parties": "Payee's name is consistent",
        "consistent.payer_name_in_parties": "Payer's name is consistent",
        "consistent.procuring_entity_name_in_parties": "Procuring entity's name is consistent",
        "consistent.supplier_name_in_parties": "Supplier's name is consistent",
        "consistent.tenderer_name_in_parties": "Tenderer's name is consistent",
        "reference.buyer_in_parties": "Buyer organization reference",
        "reference.payee_in_parties": "Payee organization reference",
        "reference.payer_in_parties": "Payer organization reference",
        "reference.procuring_entity_in_parties": "Procuring entity organization reference",
        "reference.supplier_in_parties": "Supplier organization references",
        "reference.tenderer_in_parties": "Tenderer organization references",
        "reference.contract_in_awards": "Award reference",
    }

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.prepare_data,
            '1ZgKP1TWU8AbnOFhjEqlBO--lR71dAlNMyiGDUh8MZ-8',
            gdocs,
            dataset_id
        )

        # TODO: check if check was calculated
        self.set_param_validation(
            'check',
            lambda v: v in ResourceTemplateTag.CHECK_MAPPING,
            description='The value must be one of the following: %s.' % terms_enumeration(ResourceTemplateTag.CHECK_MAPPING),
            required=True
        )

        self.set_sub_tag('name', generate_key_leaf_tag('name'))
        self.set_sub_tag('description', generate_key_leaf_tag('description'))
        self.set_sub_tag('checkedCount', generate_key_leaf_tag('checkedCount'))
        self.set_sub_tag('passedCount', generate_key_leaf_tag('passedCount'))
        self.set_sub_tag('failedCount', generate_key_leaf_tag('failedCount'))
        self.set_sub_tag('notAvailableCount', generate_key_leaf_tag('notAvailableCount'))

        self.set_sub_tag('resultBoxImage', ResultBoxImageLeafTag)
        self.set_sub_tag('passedExamples', generate_examples_leaf_tag('passedExamples'))
        self.set_sub_tag('failedExamples', generate_examples_leaf_tag('failedExamples'))
        self.set_sub_tag('notAvailableExamples', generate_examples_leaf_tag('notAvailableExamples'))

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
                "name": ResourceTemplateTag.CHECK_MAPPING[check_name],
                "description": "placeholder", # TODO: placeholder
                "checkedCount": result['total_count'],
                "passedCount": result['passed_count'],
                "failedCount": result['failed_count'],
                "notAvailableCount": result['undefined_count'],
                "passedExamples": [example['meta']['ocid'] for example in result['passed_examples']],
                "failedExamples": [example['meta']['ocid'] for example in result['failed_examples']],
                "notAvailableExamples": [example['meta']['ocid'] for example in result['undefined_examples']],
            }
