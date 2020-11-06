
import random
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration
from dqt.tools.elements import multiple_line_elements

class PassedExamplesLeafTag(LeafTag):
    LEVELS = ('coverage', 'coverageSet', 'coverageEmpty', 'quality')
    MODES = ('oneLine', 'multipleLines')

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
        self.set_param_validation(
            'mode',
            lambda v: v in PassedExamplesLeafTag.MODES,
            description='The value must be one of the following: %s.' % terms_enumeration(PassedExamplesLeafTag.MODES),
        )

        self.set_required_data_field('coveragePassedExamples')
        self.set_required_data_field('coverageSetPassedExamples')
        self.set_required_data_field('coverageEmptyPassedExamples')
        self.set_required_data_field('qualityPassedExamples')
        
    def process_tag(self, data):
        all_examples = data['%sPassedExamples' % self.get_param('level')]
        max_count = self.get_param('max')
        if max_count is None:
            max_count = len(all_examples)

        examples = random.sample(all_examples, k=int(max_count))

        mode = self.get_param('mode')
        if mode is None:
            mode = 'oneLine'

        if mode == 'oneLine':
            return ', '.join(examples)
        elif mode == 'multipleLines':
            return multiple_line_elements(examples)
