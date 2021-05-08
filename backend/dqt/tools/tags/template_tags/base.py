from dqt.tools.tags.tag import TemplateTag

from .dataset import DatasetTemplateTag
from .field import FieldTemplateTag
from .overview import OverviewTemplateTag
from .resource import ResourceTemplateTag


class BaseTemplateTag(TemplateTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(lambda _: {}, "1YMG5KZCPmI6GEcd2XQktrHD8uxEL626g3uuBjLWqQlE", gdocs, dataset_id)

        self.set_sub_tag("resource", ResourceTemplateTag)
        self.set_sub_tag("field", FieldTemplateTag)
        self.set_sub_tag("dataset", DatasetTemplateTag)
        self.set_sub_tag("overview", OverviewTemplateTag)
