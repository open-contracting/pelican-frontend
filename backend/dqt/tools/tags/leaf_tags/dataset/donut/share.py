
from dqt.tools.tags.tag import LeafTag

class ShareLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )

        self.set_param_validation('value', lambda v: isinstance(v, str))
        self.set_param_validation(
            'decimals',
            lambda v: v.isdigit(),
            description='The value must be a non-negative integer.'
        )

        self.set_required_data_field('shares')

    def process_tag(self, data):
        if self.get_param('value') is None:
            return '1.0'

        if self.get_param('value') not in data['shares']:
            return '0.0'

        if self.get_param('decimals') is not None:
            return str(round(
                data['shares'][self.get_param('value')],
                int(self.get_param('decimals'))
            ))
        else:
            return str(data['shares'][self.get_param('value')])
