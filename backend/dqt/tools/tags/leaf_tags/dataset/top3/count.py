
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class CountLeafTag(LeafTag):
    RANKS = set(['1', '2', '3', '4', '5'])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )

        self.set_param_validation(
            'rank',
            lambda v: v in CountLeafTag.RANKS,
            description='The value must be one of the following: %s.' % terms_enumeration(CountLeafTag.RANKS)
        )
        
        self.set_required_data_field('counts')

    def process_tag(self, data):
        if self.get_param('rank') is None:
            return str(sum(data['counts'].values()))

        return str(data['counts'][self.get_param('rank')])
