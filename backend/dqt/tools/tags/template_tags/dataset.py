
from django.db import connections
from dqt.models import DatasetLevelCheck
from dqt.tools.tags.tag import TemplateTag
from dqt.tools.tags.leaf_tags.name import NameLeafTag
from dqt.tools.tags.leaf_tags.description import DescriptionLeafTag
from dqt.tools.tags.leaf_tags.dataset.result import ResultLeafTag
from dqt.tools.tags.leaf_tags.dataset.value import ValueLeafTag
from dqt.tools.tags.leaf_tags.dataset.donut.share import ShareLeafTag as donut_ShareLeafTag
from dqt.tools.tags.leaf_tags.dataset.donut.count import CountLeafTag as donut_CountLeafTag
from dqt.tools.tags.leaf_tags.dataset.donut.examples import ExamplesLeafTag as donut_ExamplesLeafTag
from dqt.tools.tags.leaf_tags.dataset.bar.share import ShareLeafTag as bar_ShareLeafTag
from dqt.tools.tags.leaf_tags.dataset.bar.count import CountLeafTag as bar_CountLeafTag
from dqt.tools.tags.leaf_tags.dataset.bar.examples import ExamplesLeafTag as bar_ExamplesLeafTag
from dqt.tools.tags.leaf_tags.dataset.bar.sum import SumLeafTag as bar_SumLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.share import ShareLeafTag as top3_ShareLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.count import CountLeafTag as top3_CountLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.examples import ExamplesLeafTag as top3_ExamplesLeafTag
from dqt.tools.tags.leaf_tags.dataset.top3.amount import AmountLeafTag as top3_AmountLeafTag
from dqt.tools.tags.leaf_tags.checked_count import CheckedCountLeafTag
from dqt.tools.tags.leaf_tags.passed_count import PassedCountLeafTag
from dqt.tools.tags.leaf_tags.failed_count import FailedCountLeafTag
from dqt.tools.tags.leaf_tags.passed_examples import PassedExamplesLeafTag
from dqt.tools.tags.leaf_tags.failed_examples import FailedExamplesLeafTag

class DatasetTemplateTag(TemplateTag):
    CHECK_TYPE_VERSION_CONTROL = {
        'distribution.main_procurement_category': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.tender_status': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.tender_procurement_method': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.tender_award_criteria': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.tender_submission_method': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.awards_status': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.contracts_status': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.milestone_status': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.milestone_type': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.document_document_type': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.value_currency': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.related_process_relation': {
            'check_type': 'donut',
            'version': 1
        },
        'distribution.tender_value': {
            'check_type': 'bar',
            'version': 1
        },
        'distribution.contracts_value': {
            'check_type': 'bar',
            'version': 1
        },
        'distribution.awards_value': {
            'check_type': 'bar',
            'version': 1
        },
        'misc.url_availability': {
            'check_type': 'numeric',
            'version': 1
        },
        'unique.tender_id': {
            'check_type': 'numeric',
            'version': 2
        },
        'consistent.related_process_title': {
            'check_type': 'numeric',
            'version': 1
        },
        'reference.related_process_identifier': {
            'check_type': 'numeric',
            'version': 2
        },
        'distribution.tender_value_repetition': {
            'check_type': 'top3',
            'version': 1
        },
        'distribution.contracts_value_repetition': {
            'check_type': 'top3',
            'version': 1
        },
        'distribution.awards_value_repetition': {
            'check_type': 'top3',
            'version': 1
        },
        'distribution.buyer_repetition': {
            'check_type': 'biggest_share',
            'version': 1
        },
        'distribution.buyer': {
            'check_type': 'single_value_share',
            'version': 1
        }
    }

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.prepare_data,
            None,
            gdocs,
            dataset_id
        )

        # TODO: check if check was calculated and version compatability
        self.set_param_validation('check', lambda v: v in DatasetTemplateTag.CHECK_TYPE_VERSION_CONTROL, required=True)

        self.set_sub_tag('name', NameLeafTag)
        self.set_sub_tag('description', DescriptionLeafTag)
        self.set_sub_tag('result', ResultLeafTag)
        self.set_sub_tag('value', ValueLeafTag)
    
    def prepare_data(self):
        check_name = self.get_param('check')
        check_type = DatasetTemplateTag.CHECK_TYPE_VERSION_CONTROL[check_name]['check_type']

        data = {}
        check = DatasetLevelCheck.objects.filter(dataset=self.dataset_id, check_name=check_name).first()
        if check is None:
            # TODO
            pass
        data['name'] = check_name
        data['description'] = 'placeholder'
        data['result'] = check.result
        data['value'] = check.value

        if check_type == 'donut':
            self.set_sub_tag('share', donut_ShareLeafTag)
            self.set_sub_tag('count', donut_CountLeafTag)
            self.set_sub_tag('examples', donut_ExamplesLeafTag)
            # self.set_sub_tag('resultBoxImage')

            data['shares'] = {
                key: value['share']
                for key, value in check.meta['shares'].items()
            }
            data['counts'] = {
                key: value['count']
                for key, value in check.meta['shares'].items()
            }
            data['examples'] = {
                key: [
                    example['ocid']
                    for example in value['examples']
                ]
                for key, value in check.meta['shares'].items()
            }
        elif check_type == 'bar':
            self.set_sub_tag('share', bar_ShareLeafTag)
            self.set_sub_tag('count', bar_CountLeafTag)
            self.set_sub_tag('examples', bar_ExamplesLeafTag)
            self.set_sub_tag('sum', bar_SumLeafTag)
            # self.set_sub_tag('resultBoxImage')

            data['shares'] = {
                key.replace('_', '-'): value
                for key, value in check.meta['shares'].items()
            }
            data['counts'] = {
                key.replace('_', '-'): value
                for key, value in check.meta['counts'].items()
            }
            data['examples'] = {
                key.replace('_', '-'): [
                    example['ocid']
                    for example in examples
                ]
                for key, examples in check.meta['examples'].items()
            }
            data['sums'] = {
                key.replace('_', '-'): value
                for key, value in check.meta['sums'].items()
            }
        elif check_type == 'top3':
            self.set_sub_tag('share', top3_ShareLeafTag)
            self.set_sub_tag('count', top3_CountLeafTag)
            self.set_sub_tag('examples', top3_ExamplesLeafTag)
            self.set_sub_tag('amount', top3_AmountLeafTag)
            # self.set_sub_tag('resultBoxImage')

            data['shares'] = {
                str(index + 1): el['share']
                for index, el in enumerate(check.meta['most_frequent'])
            }
            data['counts'] = {
                str(index + 1): el['count']
                for index, el in enumerate(check.meta['most_frequent'])
            }
            data['examples'] = {
                str(index + 1): [
                    example['ocid']
                    for example in el['examples']
                ]
                for index, el in enumerate(check.meta['most_frequent'])
            }
            data['amounts'] = {
                str(index + 1): el['value_str']
                for index, el in enumerate(check.meta['most_frequent'])
            }
        elif check_type == 'numeric':
            self.set_sub_tag('checkedCount', CheckedCountLeafTag)
            self.set_sub_tag('passedCount', PassedCountLeafTag)
            self.set_sub_tag('failedCount', FailedCountLeafTag)
            self.set_sub_tag('passedExamples', PassedExamplesLeafTag)
            self.set_sub_tag('failedExamples', FailedExamplesLeafTag)
            # self.set_sub_tag('resultBoxImage')

            data['checkedCount'] = check.meta['total_processed']
            data['passedCount'] = check.meta['total_passed']
            data['failedCount'] = check.meta['total_failed']
            data['passedExamples'] = [
                example['ocid']
                for example in check.meta['passed_examples']
            ]
            data['failedExamples'] = [
                example['ocid']
                for example in check.meta['failed_examples']
            ]

        return data
