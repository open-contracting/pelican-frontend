
from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

class FailedCountLeafTag(LeafTag):
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
            lambda v: v in FailedCountLeafTag.LEVELS,
            description='The value must be one of the following: %s.' % terms_enumeration(FailedCountLeafTag.LEVELS),
            required=True
        )
        # self.set_param_validation('check', lambda v: v in FieldTemplateTag.CHECKS)

        self.set_required_data_field('coverageFailedCount')
        self.set_required_data_field('qualityFailedCount')
        # self.set_required_data_field('checks')

    def process_tag(self, data):
        return data['%sFailedCount' % self.get_param('level')]
