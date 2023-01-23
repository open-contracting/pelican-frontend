from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

RANKS = {"1", "2", "3", "4", "5"}


class CountLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "rank",
            lambda v: v in RANKS,
            description="The value must be one of the following: %s." % terms_enumeration(RANKS),
        )

        self.set_required_data_field("counts")

    def process_tag(self, data):
        if self.get_param("rank") is None:
            return str(sum(data["counts"].values()))

        return str(data["counts"][self.get_param("rank")])
