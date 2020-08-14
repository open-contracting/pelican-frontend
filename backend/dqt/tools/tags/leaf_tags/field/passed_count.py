
from dqt.tools.tags.tag import LeafTag

class PassedCountLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        self.set_required_data_field('passedCount')

    def process_tag(self, data):
        return data['passedCount']

