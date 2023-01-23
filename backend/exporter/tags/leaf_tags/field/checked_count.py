from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

LEVELS = ("coverage", "coverageSet", "coverageEmpty", "quality")


class CheckedCountLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in LEVELS,
            description="The value must be one of the following: %s." % terms_enumeration(LEVELS),
            required=True,
        )

        self.set_required_data_field("coverageCheckedCount")
        self.set_required_data_field("coverageSetCheckedCount")
        self.set_required_data_field("coverageEmptyCheckedCount")
        self.set_required_data_field("qualityCheckedCount")

    def process_tag(self, data):
        return str(data["%sCheckedCount" % self.get_param("level")])
