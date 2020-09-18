
import random
from dqt.tools.tags.tag import LeafTag

class ExamplesLeafTag(LeafTag):
    PERCENTAGE_RANGES = set([
        '0-1',
        '1-5',
        '5-20',
        '20-50',
        '50-100',
    ])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation('percentageRange', lambda v: v in ExamplesLeafTag.PERCENTAGE_RANGES)
        self.set_param_validation('max', lambda v: v.isdigit())

        self.set_required_data_field('examples')
        
    def process_tag(self, data):
        if self.get_param('percentageRange') is not None:
            percentage_range_examples = data['examples'][self.get_param('percentageRange')]
        else:
            percentage_range_examples = [
                example
                for examples in data['examples'].values()
                for example in examples
            ]

        max_count = self.get_param('max')
        if max_count is not None:
            return ', '.join(
                random.sample(
                    percentage_range_examples,
                    k=min(int(max_count), len(percentage_range_examples))
                )
            )
        else:
            return ', '.join(percentage_range_examples)
