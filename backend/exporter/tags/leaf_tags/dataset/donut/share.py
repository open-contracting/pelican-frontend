from exporter.tags.tag import LeafTag


class ShareLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation("value", lambda v: isinstance(v, str))
        self.set_param_validation(
            "decimals", lambda v: v.isdigit(), description="The value must be a non-negative integer."
        )

        self.required_data_fields = {"shares"}

    def process_tag(self, data):
        if self.get_param("value") is None:
            share = 100.0
        elif self.get_param("value") not in data["shares"]:
            share = 0.0
        else:
            share = 100 * data["shares"][self.get_param("value")]

        decimals = int(self.get_param("decimals", 0))

        return ("%." + str(decimals) + "f") % share
