
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class OcidCountLeafTag(LeafTag):
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
            str,
            gdocs,
            dataset_id
        )

        self.set_param_validation(
            'countRange',
            lambda v: v in OcidCountLeafTag.COUNT_RANGES,
            description='The value must be one of the following: %s.' % terms_enumeration(OcidCountLeafTag.COUNT_RANGES)
        )
        
        self.set_required_data_field('ocidCounts')

    def process_tag(self, data):
        if self.get_param('countRange') is None:
            return str(sum(data['ocidCounts'].values()))

        return str(data['ocidCounts'][self.get_param('countRange')])
