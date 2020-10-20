
import random
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class FailedExamplesLeafTag(LeafTag):
    LEVELS = ('coverage', 'coverageSet', 'coverageEmpty', 'quality')

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation(
            'level',
            lambda v: v in FailedExamplesLeafTag.LEVELS,
            description='The value must be one of the following: %s.' % terms_enumeration(FailedExamplesLeafTag.LEVELS),
            required=True
        )
        self.set_param_validation(
            'max',
            lambda v: v.isdigit(),
            description='The value must be a positive integer.'
        )

        self.set_required_data_field('coverageFailedExamples')
        self.set_required_data_field('coverageSetFailedExamples')
        self.set_required_data_field('coverageEmptyFailedExamples')
        self.set_required_data_field('qualityFailedExamples')
        
    def process_tag(self, data):
        max_count = self.get_param('max')
        examples = data['%sFailedExamples' % self.get_param('level')]
        if max_count is not None:
            return ', '.join(
                random.sample(
                    examples,
                    k=min(int(max_count), len(examples))
                )
            )
        else:
            return ', '.join(examples)
