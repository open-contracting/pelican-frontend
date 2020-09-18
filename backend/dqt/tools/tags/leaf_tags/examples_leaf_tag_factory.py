
import random
from dqt.tools.tags.tag import LeafTag

def generate_examples_leaf_tag(key):
    class ExamplesLeafTag(LeafTag):
        def __init__(self, gdocs, dataset_id):
            super().__init__(
                self.process_tag,
                str,
                gdocs,
                dataset_id
            )
            
            self.set_param_validation('max', lambda v: v.isdigit())

            self.set_required_data_field(key)

        def process_tag(self, data):
            max_count = self.get_param('max')
            if max_count is not None:
                return ', '.join(
                    random.sample(
                        data[key],
                        k=min(int(max_count), len(data[key]))
                    )
                )
            else:
                return ', '.join(data[key])

    return ExamplesLeafTag
