
import random
from dqt.tools.tags.tag import LeafTag

class ExamplesLeafTag(LeafTag):
    RANKS = set(['1', '2', '3', '4', '5'])


    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation('rank', lambda v: v in ExamplesLeafTag.RANKS)
        self.set_param_validation('max', lambda v: v.isdigit())

        self.set_required_data_field('examples')
        
    def process_tag(self, data):
        if self.get_param('rank') is not None:
            rank_examples = data['examples'][self.get_param('rank')]
        else:
            rank_examples = [
                example
                for examples in data['examples'].values()
                for example in examples
            ]

        max_count = self.get_param('max')
        if max_count is not None:
            return ', '.join(
                random.sample(
                    rank_examples,
                    k=min(int(max_count), len(rank_examples))
                )
            )
        else:
            return ', '.join(rank_examples)