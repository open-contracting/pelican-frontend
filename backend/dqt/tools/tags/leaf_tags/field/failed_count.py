
from dqt.tools.tags.tag import LeafTag

class FailedCountLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation('level', lambda v: v in ('coverage', 'quality'), required=True)
        # self.set_param_validation('check', lambda v: v in FieldTemplateTag.CHECKS)

        self.set_required_data_field('coverageFailedCount')
        self.set_required_data_field('qualityFailedCount')
        # self.set_required_data_field('checks')

    def process_tag(self, data):
        return data['%sFailedCount' % self.get_param('level')]
