from django.utils.translation import gettext as _

from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration


class DescriptionLeafTag(LeafTag):
    LEVELS = ("coverageSet", "coverageEmpty", "quality")

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in DescriptionLeafTag.LEVELS,
            description="The value must be one of the following: %s." % terms_enumeration(DescriptionLeafTag.LEVELS),
            required=True,
        )

        self.set_required_data_field("qualityCheck")

    def process_tag(self, data):
        if self.get_param("level") == "quality" and data["qualityCheck"] is None:
            return ""

        if self.get_param("level") == "coverageSet":
            return _("field.exists.description")
        elif self.get_param("level") == "coverageEmpty":
            return _("field.non_empty.description")

        return _(str("field." + data["qualityCheck"] + ".description"))
