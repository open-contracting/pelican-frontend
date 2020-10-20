
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class CheckedCountLeafTag(LeafTag):
    LEVELS = ('coverage', 'coverageSet', 'coverageEmpty', 'quality')

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation(
            'level',
            lambda v: v in CheckedCountLeafTag.LEVELS,
            description='The value must be one of the following: %s.' % terms_enumeration(CheckedCountLeafTag.LEVELS),
            required=True
        )

        self.set_required_data_field('coverageCheckedCount')
        self.set_required_data_field('coverageSetCheckedCount')
        self.set_required_data_field('coverageEmptyCheckedCount')
        self.set_required_data_field('qualityCheckedCount')

    def process_tag(self, data):
        return data['%sCheckedCount' % self.get_param('level')]
