
from dqt.tools.misc import terms_enumeration
from dqt.tools.tags.tag import LeafTag


class LifecycleObjectCountLeafTag(LeafTag):
    STAGES = set([
        'planning',
        'tender',
        'award',
        'contract',
        'implementation',
    ])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )

        self.set_param_validation(
            'stage',
            lambda v: v in LifecycleObjectCountLeafTag.STAGES,
            description='The value must be one of the following: %s.' % terms_enumeration(LifecycleObjectCountLeafTag.STAGES),
            required=True
        )
        
        self.set_required_data_field('lifecycle_object_counts')

    def process_tag(self, data):
        return str(data['lifecycle_object_counts'][self.get_param('stage')])
