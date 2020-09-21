
from django.db import connections
from dqt.tools.tags.tag import TemplateTag
from dqt.tools.tags.leaf_tags.key_leaf_tag_factory import generate_key_leaf_tag
from dqt.tools.tags.leaf_tags.field.checked_count import CheckedCountLeafTag
from dqt.tools.tags.leaf_tags.field.passed_count import PassedCountLeafTag
from dqt.tools.tags.leaf_tags.field.failed_count import FailedCountLeafTag
from dqt.tools.tags.leaf_tags.field.result_box_image import ResultBoxImageLeafTag
from dqt.tools.tags.leaf_tags.field.passed_examples import PassedExamplesLeafTag
from dqt.tools.tags.leaf_tags.field.failed_examples import FailedExamplesLeafTag


class FieldTemplateTag(TemplateTag):
    CHECKS = set([
        'date_time',
        'document_description_length',
        'document_format_codelist',
        'document_type',
        'email',
        'exists',
        'identifier_scheme',
        'language',
        'non_empty',
        'number_checks',
        'ocid_prefix_check',
        'telephone',
    ])

    PATHS = set([
        'ocid',
        'id',
        'date',
        'tag',
        'initiationType',
        'parties',
        'parties.name',
        'parties.id',
        'parties.identifier',
        'parties.identifier.scheme',
        'parties.identifier.id',
        'parties.identifier.legalName',
        'parties.identifier.uri',
        'parties.additionalIdentifiers',
        'parties.additionalIdentifiers.scheme',
        'parties.additionalIdentifiers.id',
        'parties.additionalIdentifiers.legalName',
        'parties.additionalIdentifiers.uri',
        'parties.address',
        'parties.address.streetAddress',
        'parties.address.locality',
        'parties.address.region',
        'parties.address.postalCode',
        'parties.address.countryName',
        'parties.contactPoint',
        'parties.contactPoint.name',
        'parties.contactPoint.email',
        'parties.contactPoint.telephone',
        'parties.contactPoint.faxNumber',
        'parties.contactPoint.url',
        'parties.roles',
        'parties.details',
        'buyer',
        'buyer.name',
        'buyer.id',
        'buyer.identifier',
        'buyer.identifier.scheme',
        'buyer.identifier.id',
        'buyer.identifier.legalName',
        'buyer.identifier.uri',
        'buyer.address',
        'buyer.address.streetAddress',
        'buyer.address.locality',
        'buyer.address.region',
        'buyer.address.postalCode',
        'buyer.address.countryName',
        'buyer.additionalIdentifiers',
        'buyer.additionalIdentifiers.scheme',
        'buyer.additionalIdentifiers.id',
        'buyer.additionalIdentifiers.legalName',
        'buyer.additionalIdentifiers.uri',
        'buyer.contactPoint',
        'buyer.contactPoint.name',
        'buyer.contactPoint.email',
        'buyer.contactPoint.telephone',
        'buyer.contactPoint.faxNumber',
        'buyer.contactPoint.url',
        'planning',
        'planning.rationale',
        'planning.budget',
        'planning.budget.id',
        'planning.budget.description',
        'planning.budget.amount',
        'planning.budget.amount.amount',
        'planning.budget.amount.currency',
        'planning.budget.project',
        'planning.budget.projectID',
        'planning.budget.uri',
        'planning.budget.source',
        'planning.documents',
        'planning.documents.id',
        'planning.documents.documentType',
        'planning.documents.title',
        'planning.documents.description',
        'planning.documents.url',
        'planning.documents.datePublished',
        'planning.documents.dateModified',
        'planning.documents.format',
        'planning.documents.language',
        'planning.milestones',
        'planning.milestones.id',
        'planning.milestones.title',
        'planning.milestones.type',
        'planning.milestones.description',
        'planning.milestones.code',
        'planning.milestones.dueDate',
        'planning.milestones.dateMet',
        'planning.milestones.dateModified',
        'planning.milestones.status',
        'planning.milestones.documents',
        'planning.milestones.documents.id',
        'planning.milestones.documents.documentType',
        'planning.milestones.documents.title',
        'planning.milestones.documents.description',
        'planning.milestones.documents.url',
        'planning.milestones.documents.datePublished',
        'planning.milestones.documents.dateModified',
        'planning.milestones.documents.format',
        'planning.milestones.documents.language',
        'tender',
        'tender.id',
        'tender.title',
        'tender.description',
        'tender.status',
        'tender.procuringEntity',
        'tender.procuringEntity.name',
        'tender.procuringEntity.id',
        'tender.procuringEntity.identifier',
        'tender.procuringEntity.identifier.scheme',
        'tender.procuringEntity.identifier.id',
        'tender.procuringEntity.identifier.legalName',
        'tender.procuringEntity.identifier.uri',
        'tender.procuringEntity.address',
        'tender.procuringEntity.address.streetAddress',
        'tender.procuringEntity.address.locality',
        'tender.procuringEntity.address.region',
        'tender.procuringEntity.address.postalCode',
        'tender.procuringEntity.address.countryName',
        'tender.procuringEntity.additionalIdentifiers',
        'tender.procuringEntity.additionalIdentifiers.scheme',
        'tender.procuringEntity.additionalIdentifiers.id',
        'tender.procuringEntity.additionalIdentifiers.legalName',
        'tender.procuringEntity.additionalIdentifiers.uri',
        'tender.procuringEntity.contactPoint',
        'tender.procuringEntity.contactPoint.name',
        'tender.procuringEntity.contactPoint.email',
        'tender.procuringEntity.contactPoint.telephone',
        'tender.procuringEntity.contactPoint.faxNumber',
        'tender.procuringEntity.contactPoint.url',
        'tender.items',
        'tender.items.id',
        'tender.items.description',
        'tender.items.classification',
        'tender.items.classification.scheme',
        'tender.items.classification.id',
        'tender.items.classification.description',
        'tender.items.classification.uri',
        'tender.items.additionalClassifications',
        'tender.items.additionalClassifications.scheme',
        'tender.items.additionalClassifications.id',
        'tender.items.additionalClassifications.description',
        'tender.items.additionalClassifications.uri',
        'tender.items.quantity',
        'tender.items.unit',
        'tender.items.unit.scheme',
        'tender.items.unit.id',
        'tender.items.unit.name',
        'tender.items.unit.value',
        'tender.items.unit.value.amount',
        'tender.items.unit.value.currency',
        'tender.items.unit.uri',
        'tender.value',
        'tender.value.amount',
        'tender.value.currency',
        'tender.minValue',
        'tender.minValue.amount',
        'tender.minValue.currency',
        'tender.procurementMethod',
        'tender.procurementMethodDetails',
        'tender.procurementMethodRationale',
        'tender.mainProcurementCategory',
        'tender.additionalProcurementCategories',
        'tender.awardCriteria',
        'tender.awardCriteriaDetails',
        'tender.submissionMethod',
        'tender.submissionMethodDetails',
        'tender.tenderPeriod',
        'tender.tenderPeriod.startDate',
        'tender.tenderPeriod.endDate',
        'tender.tenderPeriod.maxExtentDate',
        'tender.tenderPeriod.durationInDays',
        'tender.enquiryPeriod',
        'tender.enquiryPeriod.durationInDays',
        'tender.enquiryPeriod.startDate',
        'tender.enquiryPeriod.endDate',
        'tender.enquiryPeriod.maxExtentDate',
        'tender.hasEnquiries',
        'tender.eligibilityCriteria',
        'tender.awardPeriod',
        'tender.awardPeriod.startDate',
        'tender.awardPeriod.endDate',
        'tender.awardPeriod.maxExtentDate',
        'tender.awardPeriod.durationInDays',
        'tender.contractPeriod',
        'tender.contractPeriod.startDate',
        'tender.contractPeriod.endDate',
        'tender.contractPeriod.maxExtentDate',
        'tender.contractPeriod.durationInDays',
        'tender.numberOfTenderers',
        'tender.tenderers',
        'tender.tenderers.name',
        'tender.tenderers.id',
        'tender.tenderers.identifier',
        'tender.tenderers.identifier.scheme',
        'tender.tenderers.identifier.id',
        'tender.tenderers.identifier.legalName',
        'tender.tenderers.identifier.uri',
        'tender.tenderers.address',
        'tender.tenderers.address.streetAddress',
        'tender.tenderers.address.locality',
        'tender.tenderers.address.region',
        'tender.tenderers.address.postalCode',
        'tender.tenderers.address.countryName',
        'tender.tenderers.additionalIdentifiers',
        'tender.tenderers.additionalIdentifiers.scheme',
        'tender.tenderers.additionalIdentifiers.id',
        'tender.tenderers.additionalIdentifiers.legalName',
        'tender.tenderers.additionalIdentifiers.uri',
        'tender.tenderers.contactPoint',
        'tender.tenderers.contactPoint.name',
        'tender.tenderers.contactPoint.email',
        'tender.tenderers.contactPoint.telephone',
        'tender.tenderers.contactPoint.faxNumber',
        'tender.tenderers.contactPoint.url',
        'tender.documents',
        'tender.documents.id',
        'tender.documents.documentType',
        'tender.documents.title',
        'tender.documents.description',
        'tender.documents.url',
        'tender.documents.datePublished',
        'tender.documents.dateModified',
        'tender.documents.format',
        'tender.documents.language',
        'tender.documents.datePublished',
        'tender.documents.dateModified',
        'tender.milestones',
        'tender.milestones.id',
        'tender.milestones.title',
        'tender.milestones.type',
        'tender.milestones.description',
        'tender.milestones.code',
        'tender.milestones.dueDate',
        'tender.milestones.dateMet',
        'tender.milestones.dateModified',
        'tender.milestones.status',
        'tender.milestones.documents',
        'tender.milestones.documents.id',
        'tender.milestones.documents.documentType',
        'tender.milestones.documents.title',
        'tender.milestones.documents.description',
        'tender.milestones.documents.url',
        'tender.milestones.documents.datePublished',
        'tender.milestones.documents.dateModified',
        'tender.milestones.documents.format',
        'tender.milestones.documents.language',
        'tender.amendments',
        'tender.amendments.date',
        'tender.amendments.rationale',
        'tender.amendments.id',
        'tender.amendments.description',
        'tender.amendments.amendsReleaseID',
        'tender.amendments.releaseID',
        'tender.amendments.changes',
        'tender.amendments.changes.property',
        'tender.amendments.changes.former_value',
        'tender.amendment',
        'tender.amendment.date',
        'tender.amendment.rationale',
        'tender.amendment.id',
        'tender.amendment.description',
        'tender.amendment.amendsReleaseID',
        'tender.amendment.releaseID',
        'tender.amendment.changes',
        'tender.amendment.changes.property',
        'tender.amendment.changes.former_value',
        'awards',
        'awards.id',
        'awards.title',
        'awards.description',
        'awards.status',
        'awards.date',
        'awards.value',
        'awards.value.amount',
        'awards.value.currency',
        'awards.suppliers',
        'awards.suppliers.name',
        'awards.suppliers.id',
        'awards.suppliers.identifier',
        'awards.suppliers.identifier.scheme',
        'awards.suppliers.identifier.id',
        'awards.suppliers.identifier.legalName',
        'awards.suppliers.identifier.uri',
        'awards.suppliers.address',
        'awards.suppliers.address.streetAddress',
        'awards.suppliers.address.locality',
        'awards.suppliers.address.region',
        'awards.suppliers.address.postalCode',
        'awards.suppliers.address.countryName',
        'awards.suppliers.additionalIdentifiers',
        'awards.suppliers.additionalIdentifiers.scheme',
        'awards.suppliers.additionalIdentifiers.id',
        'awards.suppliers.additionalIdentifiers.legalName',
        'awards.suppliers.additionalIdentifiers.uri',
        'awards.suppliers.contactPoint',
        'awards.suppliers.contactPoint.name',
        'awards.suppliers.contactPoint.email',
        'awards.suppliers.contactPoint.telephone',
        'awards.suppliers.contactPoint.faxNumber',
        'awards.suppliers.contactPoint.url',
        'awards.items',
        'awards.items.id',
        'awards.items.description',
        'awards.items.classification',
        'awards.items.classification.scheme',
        'awards.items.classification.id',
        'awards.items.classification.description',
        'awards.items.classification.uri',
        'awards.items.additionalClassifications',
        'awards.items.additionalClassifications.scheme',
        'awards.items.additionalClassifications.id',
        'awards.items.additionalClassifications.description',
        'awards.items.additionalClassifications.uri',
        'awards.items.quantity',
        'awards.items.unit',
        'awards.items.unit.scheme',
        'awards.items.unit.id',
        'awards.items.unit.name',
        'awards.items.unit.value',
        'awards.items.unit.value.amount',
        'awards.items.unit.value.currency',
        'awards.items.unit.uri',
        'awards.contractPeriod',
        'awards.contractPeriod.startDate',
        'awards.contractPeriod.endDate',
        'awards.contractPeriod.maxExtentDate',
        'awards.contractPeriod.durationInDays',
        'awards.documents',
        'awards.documents.id',
        'awards.documents.documentType',
        'awards.documents.title',
        'awards.documents.description',
        'awards.documents.url',
        'awards.documents.datePublished',
        'awards.documents.dateModified',
        'awards.documents.format',
        'awards.documents.language',
        'awards.documents.language',
        'awards.amendments',
        'awards.amendments.date',
        'awards.amendments.rationale',
        'awards.amendments.id',
        'awards.amendments.description',
        'awards.amendments.amendsReleaseID',
        'awards.amendments.releaseID',
        'awards.amendments.changes',
        'awards.amendments.changes.property',
        'awards.amendments.changes.former_value',
        'awards.amendment',
        'awards.amendment.date',
        'awards.amendment.rationale',
        'awards.amendment.id',
        'awards.amendment.description',
        'awards.amendment.amendsReleaseID',
        'awards.amendment.releaseID',
        'awards.amendment.changes',
        'awards.amendment.changes.property',
        'awards.amendment.changes.former_value',
        'contracts',
        'contracts.id',
        'contracts.awardID',
        'contracts.title',
        'contracts.description',
        'contracts.status',
        'contracts.period',
        'contracts.period.startDate',
        'contracts.period.endDate',
        'contracts.period.maxExtentDate',
        'contracts.period.durationInDays',
        'contracts.value',
        'contracts.value.amount',
        'contracts.value.currency',
        'contracts.items',
        'contracts.items.id',
        'contracts.items.description',
        'contracts.items.classification',
        'contracts.items.classification.scheme',
        'contracts.items.classification.id',
        'contracts.items.classification.description',
        'contracts.items.classification.uri',
        'contracts.items.additionalClassifications',
        'contracts.items.additionalClassifications.scheme',
        'contracts.items.additionalClassifications.id',
        'contracts.items.additionalClassifications.description',
        'contracts.items.additionalClassifications.uri',
        'contracts.items.quantity',
        'contracts.items.unit',
        'contracts.items.unit.scheme',
        'contracts.items.unit.id',
        'contracts.items.unit.name',
        'contracts.items.unit.value',
        'contracts.items.unit.value.amount',
        'contracts.items.unit.value.currency',
        'contracts.items.unit.uri',
        'contracts.dateSigned',
        'contracts.documents',
        'contracts.documents.id',
        'contracts.documents.documentType',
        'contracts.documents.title',
        'contracts.documents.description',
        'contracts.documents.url',
        'contracts.documents.datePublished',
        'contracts.documents.dateModified',
        'contracts.documents.format',
        'contracts.documents.language',
        'contracts.documents.language',
        'contracts.implementation',
        'contracts.implementation.transactions',
        'contracts.implementation.transactions.id',
        'contracts.implementation.transactions.source',
        'contracts.implementation.transactions.date',
        'contracts.implementation.transactions.value',
        'contracts.implementation.transactions.value.amount',
        'contracts.implementation.transactions.value.currency',
        'contracts.implementation.transactions.payer',
        'contracts.implementation.transactions.payer.name',
        'contracts.implementation.transactions.payer.id',
        'contracts.implementation.transactions.payer.identifier',
        'contracts.implementation.transactions.payer.identifier.scheme',
        'contracts.implementation.transactions.payer.identifier.id',
        'contracts.implementation.transactions.payer.identifier.legalName',
        'contracts.implementation.transactions.payer.identifier.uri',
        'contracts.implementation.transactions.payer.address',
        'contracts.implementation.transactions.payer.address.streetAddress',
        'contracts.implementation.transactions.payer.address.locality',
        'contracts.implementation.transactions.payer.address.region',
        'contracts.implementation.transactions.payer.address.postalCode',
        'contracts.implementation.transactions.payer.address.countryName',
        'contracts.implementation.transactions.payer.additionalIdentifiers',
        'contracts.implementation.transactions.payer.additionalIdentifiers.scheme',
        'contracts.implementation.transactions.payer.additionalIdentifiers.id',
        'contracts.implementation.transactions.payer.additionalIdentifiers.legalName',
        'contracts.implementation.transactions.payer.additionalIdentifiers.uri',
        'contracts.implementation.transactions.payer.contactPoint',
        'contracts.implementation.transactions.payer.contactPoint.name',
        'contracts.implementation.transactions.payer.contactPoint.email',
        'contracts.implementation.transactions.payer.contactPoint.telephone',
        'contracts.implementation.transactions.payer.contactPoint.faxNumber',
        'contracts.implementation.transactions.payer.contactPoint.url',
        'contracts.implementation.transactions.payee',
        'contracts.implementation.transactions.payee.name',
        'contracts.implementation.transactions.payee.id',
        'contracts.implementation.transactions.payee.identifier',
        'contracts.implementation.transactions.payee.identifier.scheme',
        'contracts.implementation.transactions.payee.identifier.id',
        'contracts.implementation.transactions.payee.identifier.legalName',
        'contracts.implementation.transactions.payee.identifier.uri',
        'contracts.implementation.transactions.payee.address',
        'contracts.implementation.transactions.payee.address.streetAddress',
        'contracts.implementation.transactions.payee.address.locality',
        'contracts.implementation.transactions.payee.address.region',
        'contracts.implementation.transactions.payee.address.postalCode',
        'contracts.implementation.transactions.payee.address.countryName',
        'contracts.implementation.transactions.payee.additionalIdentifiers',
        'contracts.implementation.transactions.payee.additionalIdentifiers.scheme',
        'contracts.implementation.transactions.payee.additionalIdentifiers.id',
        'contracts.implementation.transactions.payee.additionalIdentifiers.legalName',
        'contracts.implementation.transactions.payee.additionalIdentifiers.uri',
        'contracts.implementation.transactions.payee.contactPoint',
        'contracts.implementation.transactions.payee.contactPoint.name',
        'contracts.implementation.transactions.payee.contactPoint.email',
        'contracts.implementation.transactions.payee.contactPoint.telephone',
        'contracts.implementation.transactions.payee.contactPoint.faxNumber',
        'contracts.implementation.transactions.payee.contactPoint.url',
        'contracts.implementation.transactions.uri',
        'contracts.implementation.transactions.amount',
        'contracts.implementation.transactions.amount.amount',
        'contracts.implementation.transactions.currency',
        'contracts.implementation.transactions.providerOrganization',
        'contracts.implementation.transactions.providerOrganization.scheme',
        'contracts.implementation.transactions.providerOrganization.id',
        'contracts.implementation.transactions.providerOrganization.legalName',
        'contracts.implementation.transactions.providerOrganization.uri',
        'contracts.implementation.transactions.receiverOrganization',
        'contracts.implementation.transactions.receiverOrganization.scheme',
        'contracts.implementation.transactions.receiverOrganization.id',
        'contracts.implementation.transactions.receiverOrganization.legalName',
        'contracts.implementation.transactions.receiverOrganization.uri',
        'contracts.implementation.milestones',
        'contracts.implementation.milestones.id',
        'contracts.implementation.milestones.title',
        'contracts.implementation.milestones.type',
        'contracts.implementation.milestones.description',
        'contracts.implementation.milestones.code',
        'contracts.implementation.milestones.dueDate',
        'contracts.implementation.milestones.dateMet',
        'contracts.implementation.milestones.dateModified',
        'contracts.implementation.milestones.status',
        'contracts.implementation.milestones.documents',
        'contracts.implementation.milestones.documents.id',
        'contracts.implementation.milestones.documents.documentType',
        'contracts.implementation.milestones.documents.title',
        'contracts.implementation.milestones.documents.description',
        'contracts.implementation.milestones.documents.url',
        'contracts.implementation.milestones.documents.datePublished',
        'contracts.implementation.milestones.documents.dateModified',
        'contracts.implementation.milestones.documents.format',
        'contracts.implementation.milestones.documents.language',
        'contracts.implementation.documents',
        'contracts.implementation.documents.id',
        'contracts.implementation.documents.documentType',
        'contracts.implementation.documents.title',
        'contracts.implementation.documents.description',
        'contracts.implementation.documents.url',
        'contracts.implementation.documents.datePublished',
        'contracts.implementation.documents.dateModified',
        'contracts.implementation.documents.format',
        'contracts.implementation.documents.language',
        'contracts.relatedProcesses',
        'contracts.relatedProcesses.id',
        'contracts.relatedProcesses.relationship',
        'contracts.relatedProcesses.title',
        'contracts.relatedProcesses.scheme',
        'contracts.relatedProcesses.identifier',
        'contracts.relatedProcesses.uri',
        'contracts.milestones',
        'contracts.milestones.id',
        'contracts.milestones.title',
        'contracts.milestones.type',
        'contracts.milestones.description',
        'contracts.milestones.code',
        'contracts.milestones.dueDate',
        'contracts.milestones.dateMet',
        'contracts.milestones.dateModified',
        'contracts.milestones.status',
        'contracts.milestones.documents',
        'contracts.milestones.documents.id',
        'contracts.milestones.documents.documentType',
        'contracts.milestones.documents.title',
        'contracts.milestones.documents.description',
        'contracts.milestones.documents.url',
        'contracts.milestones.documents.datePublished',
        'contracts.milestones.documents.dateModified',
        'contracts.milestones.documents.format',
        'contracts.milestones.documents.language',
        'contracts.amendments',
        'contracts.amendments.date',
        'contracts.amendments.rationale',
        'contracts.amendments.id',
        'contracts.amendments.description',
        'contracts.amendments.amendsReleaseID',
        'contracts.amendments.releaseID',
        'contracts.amendments.changes',
        'contracts.amendments.changes.property',
        'contracts.amendments.changes.former_value',
        'contracts.amendment',
        'contracts.amendment.date',
        'contracts.amendment.rationale',
        'contracts.amendment.id',
        'contracts.amendment.description',
        'contracts.amendment.amendsReleaseID',
        'contracts.amendment.releaseID',
        'contracts.amendment.changes',
        'contracts.amendment.changes.property',
        'contracts.amendment.changes.former_value',
        'language',
        'relatedProcesses',
        'relatedProcesses.id',
        'relatedProcesses.relationship',
        'relatedProcesses.title',
        'relatedProcesses.scheme',
        'relatedProcesses.identifier',
        'relatedProcesses.uri',
    ])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.prepare_data,
            '1Is3yi1p3XRI1x98rTZcfQiKb7WAAC4P1nXb-VCCyVTk',
            gdocs,
            dataset_id
        )

        # TODO: checks for given path were calculated
        self.set_param_validation('path', lambda v: v in FieldTemplateTag.PATHS, required=True)

        self.set_sub_tag('name', generate_key_leaf_tag('name'))
        self.set_sub_tag('description', generate_key_leaf_tag('description'))

        self.set_sub_tag('checkedCount', CheckedCountLeafTag)
        self.set_sub_tag('passedCount', PassedCountLeafTag)
        self.set_sub_tag('failedCount', FailedCountLeafTag)
        self.set_sub_tag('resultBoxImage', ResultBoxImageLeafTag)
        self.set_sub_tag('passedExamples', PassedExamplesLeafTag)
        self.set_sub_tag('failedExamples', FailedExamplesLeafTag)

    def prepare_data(self):
        path = self.get_param('path')
        # TODO: the param check is necessary

        with connections["data"].cursor() as cursor:
            cursor.execute(
                """
                select data->%s
                from report
                where dataset_id = %s and
                    type = 'field_level_check' and
                    data ? %s;
                """, [path, self.dataset_id, path]
            )
            rows = cursor.fetchall()

            # TODO
            # if not rows:
            #     continue

            result = rows[0][0]

            # getting examples
            cursor.execute(
                """
                select data
                from field_level_check_examples
                where dataset_id = %s and path = %s;
                """, [self.dataset_id, path]
            )
            result_examples = cursor.fetchall()[0][0]

            # TODO: no rows retrieved
            return {
                "coverageCheckedCount": result['coverage']['total_count'],
                "coveragePassedCount": result['coverage']['passed_count'],
                "coverageFailedCount": result['coverage']['failed_count'],
                "qualityCheckedCount": result['quality']['total_count'],
                "qualityPassedCount": result['quality']['passed_count'],
                "qualityFailedCount": result['quality']['failed_count'],
                
                "name": path, # TODO: temporary
                "description": "placeholder", # TODO: placeholder
                "coveragePassedExamples": [example['meta']['ocid'] for example in result_examples['coverage']['passed_examples']],
                "coverageFailedExamples": [example['meta']['ocid'] for example in result_examples['coverage']['failed_examples']],
                "qualityPassedExamples": [example['meta']['ocid'] for example in result_examples['quality']['passed_examples']],
                "qualityFailedExamples": [example['meta']['ocid'] for example in result_examples['quality']['failed_examples']],
            }
