from typing import Any

from django.conf import settings

from exporter.tag import TemplateTag, template
from exporter.template_tags.dataset import Dataset
from exporter.template_tags.field import field
from exporter.template_tags.overview import overview
from exporter.template_tags.resource import resource


@template(
    "base",
    settings.GDOCS_TEMPLATES["DEFAULT_BASE_TEMPLATE"],
    (overview, field, resource, Dataset),
)
def base(tag: TemplateTag) -> dict[str, Any]:
    return {}
