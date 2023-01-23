from exporter.tags.tag import LeafTag
from exporter.util import PERCENTAGE_RANGES, terms_enumeration


class CountLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "percentageRange",
            lambda v: v in PERCENTAGE_RANGES,
            description="The value must be one of the following: %s." % terms_enumeration(PERCENTAGE_RANGES),
        )

        self.set_required_data_field("counts")

    def process_tag(self, data):
        if self.get_param("percentageRange") is None:
            return str(sum(data["counts"].values()))

        return str(data["counts"][self.get_param("percentageRange")])
