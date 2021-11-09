from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration


class SumLeafTag(LeafTag):
    PERCENTAGE_RANGES = set(
        [
            "0-1",
            "1-5",
            "5-20",
            "20-50",
            "50-100",
        ]
    )

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "percentageRange",
            lambda v: v in SumLeafTag.PERCENTAGE_RANGES,
            description="The value must be one of the following: %s."
            % terms_enumeration(SumLeafTag.PERCENTAGE_RANGES),
        )

        self.set_required_data_field("sums")

    def process_tag(self, data):
        if self.get_param("percentageRange") is None:
            return str(sum(data["sums"].values()))

        return str(data["sums"][self.get_param("percentageRange")])
