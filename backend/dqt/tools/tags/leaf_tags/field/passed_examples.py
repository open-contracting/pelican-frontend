
import random
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class PassedExamplesLeafTag(LeafTag):
    LEVELS = ('coverage', 'coverageSet', 'coverageEmpty', 'quality')

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation(
            'level',
            lambda v: v in PassedExamplesLeafTag.LEVELS,
            description='The value must be one of the following: %s.' % terms_enumeration(PassedExamplesLeafTag.LEVELS),
            required=True
        )
        self.set_param_validation(
            'max',
            lambda v: v.isdigit(),
            description='The value must be a positive integer.'
        )

        self.set_required_data_field('coveragePassedExamples')
        self.set_required_data_field('coverageSetPassedExamples')
        self.set_required_data_field('coverageEmptyPassedExamples')
        self.set_required_data_field('qualityPassedExamples')
        
    def process_tag(self, data):
        max_count = self.get_param('max')
        examples = data['%sPassedExamples' % self.get_param('level')]
        if max_count is not None:
            return ', '.join(
                random.sample(
                    examples,
                    k=min(int(max_count), len(examples))
                )
            )
        else:
            return ', '.join(examples)
