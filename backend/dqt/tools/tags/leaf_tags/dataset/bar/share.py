
from dqt.tools.tags.tag import LeafTag

class ShareLeafTag(LeafTag):
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

        self.set_param_validation('range', lambda v: v in ShareLeafTag.RANGES)
        self.set_param_validation('decimals', lambda v: v.isdigit())

        self.set_required_data_field('shares')

    def process_tag(self, data):
        if self.get_param('range') is None:
            return '1.0'

        if self.get_param('decimals') is not None:
            return str(round(
                data['shares'][self.get_param('range')],
                int(self.get_param('decimals'))
            ))
        else:
            return str(data['shares'][self.get_param('range')])
