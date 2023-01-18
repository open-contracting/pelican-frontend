from django.conf import settings

from exporter.tags.tag import TemplateTag
from exporter.tags.template_tags.dataset import DatasetTemplateTag
from exporter.tags.template_tags.field import FieldTemplateTag
from exporter.tags.template_tags.overview import OverviewTemplateTag
from exporter.tags.template_tags.resource import ResourceTemplateTag


class BaseTemplateTag(TemplateTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(lambda _: {}, settings.GDOCS_TEMPLATES["DEFAULT_BASE_TEMPLATE"], gdocs, dataset_id)

        self.set_sub_tag("resource", ResourceTemplateTag)
        self.set_sub_tag("field", FieldTemplateTag)
        self.set_sub_tag("dataset", DatasetTemplateTag)
        self.set_sub_tag("overview", OverviewTemplateTag)
