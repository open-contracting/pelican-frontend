from exporter.tags.tag import LeafTag
from exporter.util import COUNT_RANGES, terms_enumeration


class OcidCountLeafTag(LeafTag):
    required_data_fields = {"ocidCounts"}

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "countRange",
            lambda v: v in COUNT_RANGES,
            description="The value must be one of the following: %s." % terms_enumeration(COUNT_RANGES),
        )

    def process_tag(self, data):
        if self.get_param("countRange") is None:
            return str(sum(data["ocidCounts"].values()))

        return str(data["ocidCounts"][self.get_param("countRange")])
