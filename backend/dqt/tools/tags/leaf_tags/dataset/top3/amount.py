
from dqt.tools.tags.tag import LeafTag

class AmountLeafTag(LeafTag):
    RANKS = set(['1', '2', '3', '4', '5'])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )

        self.set_param_validation('rank', lambda v: v in AmountLeafTag.RANKS, required=True)
        
        self.set_required_data_field('amounts')

    def process_tag(self, data):
        return str(data['amounts'][self.get_param('rank')])
