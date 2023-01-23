from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

RANKS = {"1", "2", "3", "4", "5"}


class ShareLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "rank",
            lambda v: v in RANKS,
            description="The value must be one of the following: %s." % terms_enumeration(RANKS),
        )
        self.set_param_validation(
            "decimals", lambda v: v.isdigit(), description="The value must be a non-negative integer."
        )

        self.set_required_data_field("shares")

    def process_tag(self, data):
        if self.get_param("rank") is not None:
            share = 100 * data["shares"][self.get_param("rank")]
        else:
            share = 100.0

        decimals = int(self.get_param("decimals", 0))

        return ("%." + str(decimals) + "f") % share
