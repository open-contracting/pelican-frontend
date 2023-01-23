from exporter.tags.tag import LeafTag
from exporter.util import LEVELS, terms_enumeration


class FailedCountLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in LEVELS,
            description="The value must be one of the following: %s." % terms_enumeration(LEVELS),
            required=True,
        )

        self.set_required_data_field("coverageFailedCount")
        self.set_required_data_field("coverageSetFailedCount")
        self.set_required_data_field("coverageEmptyFailedCount")
        self.set_required_data_field("qualityFailedCount")

    def process_tag(self, data):
        return str(data["%sFailedCount" % self.get_param("level")])
