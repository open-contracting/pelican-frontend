
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class PassedCountLeafTag(LeafTag):
    LEVELS = ('coverage', 'quality')

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        
        self.set_param_validation(
            'level',
            lambda v: v in PassedCountLeafTag.LEVELS,
            description='The value must be one of the following: %s.' % terms_enumeration(PassedCountLeafTag.LEVELS),
            required=True
        )
        # self.set_param_validation('check', lambda v: v in FieldTemplateTag.CHECKS)

        self.set_required_data_field('coveragePassedCount')
        self.set_required_data_field('qualityPassedCount')
        # self.set_required_data_field('checks')

    def process_tag(self, data):
        return data['%sPassedCount' % self.get_param('level')]
