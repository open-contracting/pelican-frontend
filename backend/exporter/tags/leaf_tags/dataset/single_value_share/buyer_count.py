from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

COUNT_RANGES = {"1", "2-20", "21-50", "51-100", "100+"}


class BuyerCountLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "countRange",
            lambda v: v in COUNT_RANGES,
            description="The value must be one of the following: %s." % terms_enumeration(COUNT_RANGES),
        )

        self.set_required_data_field("buyerCounts")

    def process_tag(self, data):
        if self.get_param("countRange") is None:
            return str(sum(data["buyerCounts"].values()))

        return str(data["buyerCounts"][self.get_param("countRange")])
