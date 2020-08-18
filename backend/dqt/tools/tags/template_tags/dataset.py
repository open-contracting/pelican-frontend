
from dqt.tools.tags.tag import TemplateTag

class DatasetTemplateTag(TemplateTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.prepare_data,
            None,
            gdocs,
            dataset_id
        )
    
    def prepare_data(self):
        pass



