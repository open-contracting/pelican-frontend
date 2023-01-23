from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

LEVELS = ("coverage", "coverageSet", "coverageEmpty", "quality")


class PassedCountLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in LEVELS,
            description="The value must be one of the following: %s." % terms_enumeration(LEVELS),
            required=True,
        )

        self.set_required_data_field("coveragePassedCount")
        self.set_required_data_field("coverageSetPassedCount")
        self.set_required_data_field("coverageEmptyPassedCount")
        self.set_required_data_field("qualityPassedCount")

    def process_tag(self, data):
        return str(data["%sPassedCount" % self.get_param("level")])
