
from dqt.tools.misc import terms_enumeration
from dqt.tools.tags.tag import LeafTag


class PassedCountLeafTag(LeafTag):
    LEVELS = ('coverage', 'coverageSet', 'coverageEmpty', 'quality')

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )
        
        
        self.set_param_validation(
            'level',
            lambda v: v in PassedCountLeafTag.LEVELS,
            description='The value must be one of the following: %s.' % terms_enumeration(PassedCountLeafTag.LEVELS),
            required=True
        )

        self.set_required_data_field('coveragePassedCount')
        self.set_required_data_field('coverageSetPassedCount')
        self.set_required_data_field('coverageEmptyPassedCount')
        self.set_required_data_field('qualityPassedCount')

    def process_tag(self, data):
        return str(data['%sPassedCount' % self.get_param('level')])
