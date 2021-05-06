
from dqt.tools.tags.tag import LeafTag


def generate_key_leaf_tag(key):
    class KeyLeafTag(LeafTag):
        def __init__(self, gdocs, dataset_id):
            super().__init__(
                self.process_tag,
                gdocs,
                dataset_id
            )
            
            self.set_required_data_field(key)

        def process_tag(self, data):
            return str(data[key])

    return KeyLeafTag
