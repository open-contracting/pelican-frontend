from exporter.tags.tag import LeafTag
from exporter.util import PERCENTAGE_RANGES, terms_enumeration


class ShareLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "percentageRange",
            lambda v: v in PERCENTAGE_RANGES,
            description="The value must be one of the following: %s." % terms_enumeration(PERCENTAGE_RANGES),
        )

        self.set_param_validation(
            "decimals", lambda v: v.isdigit(), description="The value must be a non-negative integer."
        )

        self.required_data_fields = {"shares"}

    def process_tag(self, data):
        if self.get_param("percentageRange") is not None:
            share = 100 * data["shares"][self.get_param("percentageRange")]
        else:
            share = 100.0

        decimals = int(self.get_param("decimals", 0))

        return ("%." + str(decimals) + "f") % share
