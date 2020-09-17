
from dqt.tools.tags.tag import LeafTag

class CountLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )

        self.set_param_validation('value', lambda v: isinstance(v, str))
        
        self.set_required_data_field('counts')

    def process_tag(self, data):
        if self.get_param('value') is None:
            return str(sum(data['counts'].values()))

        if self.get_param('value') not in data['counts']:
            return '0'

        return str(data['counts'][self.get_param('value')])

