
from dqt.tools.tags.tag import TemplateTag

class FieldTemplateTag(TemplateTag):
    CHECKS = set([
        'date_time',
        'document_description_length',
        'document_format_codelist',
        'document_type',
        'email',
        'exists',
        'identifier_scheme',
        'language',
        'non_empty',
        'number_checks',
        'ocid_prefix_check',
        'telephone',
    ])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.prepare_data,
            '1Is3yi1p3XRI1x98rTZcfQiKb7WAAC4P1nXb-VCCyVTk',
            gdocs,
            dataset_id
        )
    
    def prepare_data(self):
        pass
