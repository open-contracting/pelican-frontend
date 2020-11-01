
from dqt.tools.tags.tag import TemplateTag
from .resource import ResourceTemplateTag
from .field import FieldTemplateTag
from .dataset import DatasetTemplateTag
from .overview import OverviewTemplateTag

class BaseTemplateTag(TemplateTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(
            lambda _: {},
            '1YMG5KZCPmI6GEcd2XQktrHD8uxEL626g3uuBjLWqQlE',
            gdocs,
            dataset_id
        )

        self.set_sub_tag('resource', ResourceTemplateTag)
        self.set_sub_tag('field', FieldTemplateTag)
        self.set_sub_tag('dataset', DatasetTemplateTag)
        self.set_sub_tag('overview', OverviewTemplateTag)

