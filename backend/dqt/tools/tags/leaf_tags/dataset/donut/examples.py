
import random
from dqt.tools.tags.tag import LeafTag

class ExamplesLeafTag(LeafTag):

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
        if max_count is not None:
            return ', '.join(
                random.sample(
                    value_examples,
                    k=min(int(max_count), len(value_examples))
                )
            )
        else:
            return ', '.join(value_examples)
