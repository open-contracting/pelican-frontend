
import random

from dqt.tools.elements import multiple_line_elements
from dqt.tools.misc import terms_enumeration
from dqt.tools.tags.tag import LeafTag


class ExamplesLeafTag(LeafTag):
    MODES = ('oneLine', 'multipleLines')

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation('value', lambda v: isinstance(v, str))
        self.set_param_validation(
            'max',
            lambda v: v.isdigit(),
            description='The value must be a positive integer.'
        )
        self.set_param_validation(
            'mode',
            lambda v: v in ExamplesLeafTag.MODES,
            description='The value must be one of the following: %s.' % terms_enumeration(ExamplesLeafTag.MODES),
        )

        self.set_required_data_field('examples')
        
    def process_tag(self, data):
        if self.get_param('value') in data['examples']:
            value_examples = data['examples'][self.get_param('value')]
        elif self.get_param('value') is None:
            value_examples = [
                example
                for examples in data['examples'].values()
                for example in examples
            ]
        else:
            value_examples = []

        max_count = self.get_param('max')
        if max_count is None:
            max_count = len(value_examples)

        examples = random.sample(value_examples, k=int(max_count))

        mode = self.get_param('mode')
        if mode is None:
            mode = 'oneLine'

        if mode == 'oneLine':
            return ', '.join(examples)
        elif mode == 'multipleLines':
            return multiple_line_elements(examples)
