from exporter.tags.tag import LeafTag
from exporter.util import PERCENTAGE_RANGES, terms_enumeration


class SumLeafTag(LeafTag):
    required_data_fields = {"sums"}

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "percentageRange",
            lambda v: v in PERCENTAGE_RANGES,
            description="The value must be one of the following: %s." % terms_enumeration(PERCENTAGE_RANGES),
        )

    def process_tag(self, data):
        if self.get_param("percentageRange") is None:
            return str(sum(data["sums"].values()))

        return str(data["sums"][self.get_param("percentageRange")])
