from django.utils.translation import gettext as _

from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

LEVELS = ("coverageSet", "coverageEmpty", "quality")


class DescriptionLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in LEVELS,
            description="The value must be one of the following: %s." % terms_enumeration(LEVELS),
            required=True,
        )

        self.required_data_fields = {"qualityCheck"}

    def process_tag(self, data):
        if self.get_param("level") == "quality" and data["qualityCheck"] is None:
            return ""

        if self.get_param("level") == "coverageSet":
            return _("field.exists.description")
        elif self.get_param("level") == "coverageEmpty":
            return _("field.non_empty.description")

        return _(str("field." + data["qualityCheck"] + ".description"))
