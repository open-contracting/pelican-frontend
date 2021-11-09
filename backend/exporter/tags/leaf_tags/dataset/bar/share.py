from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration


class ShareLeafTag(LeafTag):
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
            lambda v: v in ShareLeafTag.PERCENTAGE_RANGES,
            description="The value must be one of the following: %s."
            % terms_enumeration(ShareLeafTag.PERCENTAGE_RANGES),
        )

        self.set_param_validation(
            "decimals", lambda v: v.isdigit(), description="The value must be a non-negative integer."
        )

        self.set_required_data_field("shares")

    def process_tag(self, data):
        if self.get_param("percentageRange") is not None:
            share = 100 * data["shares"][self.get_param("percentageRange")]
        else:
            share = 100.0

        if self.get_param("decimals") is not None:
            decimals = int(self.get_param("decimals"))
        else:
            decimals = 0

        return ("%." + str(decimals) + "f") % share
