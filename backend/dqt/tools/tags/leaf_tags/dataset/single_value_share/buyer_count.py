
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class BuyerCountLeafTag(LeafTag):
    COUNT_RANGES = set([
        '1',
        '2-20',
        '21-50',
        '51-100',
        '100+',
    ])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )

        self.set_param_validation(
            'countRange',
            lambda v: v in BuyerCountLeafTag.COUNT_RANGES,
            description='The value must be one of the following: %s.' % terms_enumeration(BuyerCountLeafTag.COUNT_RANGES)
        )
        
        self.set_required_data_field('buyerCounts')

    def process_tag(self, data):
        if self.get_param('countRange') is None:
            return str(sum(data['buyerCounts'].values()))

        return str(data['buyerCounts'][self.get_param('countRange')])
