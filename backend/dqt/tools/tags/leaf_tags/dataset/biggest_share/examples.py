
import random
from dqt.tools.tags.tag import LeafTag

class ExamplesLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation(
            'max',
            lambda v: v.isdigit(),
            description='The value must be a positive integer.'
        )            

        self.set_required_data_field('examples')

    def process_tag(self, data):
        max_count = self.get_param('max')
        if max_count is not None:
            return ', '.join(
                random.sample(
                    data['examples'],
                    k=min(int(max_count), len(data['examples']))
                )
            )
        else:
            return ', '.join(data['examples'])
