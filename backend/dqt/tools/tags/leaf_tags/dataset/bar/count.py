
from dqt.tools.tags.tag import LeafTag

class CountLeafTag(LeafTag):
    RANGES = set([
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

        self.set_param_validation('range', lambda v: v in CountLeafTag.RANGES)
        
        self.set_required_data_field('counts')

    def process_tag(self, data):
        if self.get_param('range') is None:
            return str(sum(data['counts'].values()))

        return str(data['counts'][self.get_param('range')])
