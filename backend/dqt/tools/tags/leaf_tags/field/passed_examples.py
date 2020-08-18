
import random
from dqt.tools.tags.tag import LeafTag

class PassedExamplesLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            str,
            gdocs,
            dataset_id
        )
        
        self.set_param_validation('level', lambda v: v in ('coverage', 'quality'), required=True)
        self.set_param_validation('max', lambda v: v.isdigit())
        # self.set_param_validation('check', lambda v: v in FieldTemplateTag.CHECKS)

        self.set_required_data_field('coveragePassedExamples')
        self.set_required_data_field('qualityPassedExamples')
        
    def process_tag(self, data):
        max_count = self.get_param('max')
        examples = data['%sPassedExamples' % self.get_param('level')]
        if max_count is not None:
            return ', '.join(
                random.sample(
                    examples,
                    k=min(int(max_count), len(examples))
                )
            )
        else:
            return ', '.join(examples)
