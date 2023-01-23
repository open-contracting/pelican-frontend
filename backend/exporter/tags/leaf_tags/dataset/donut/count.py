from exporter.tags.tag import LeafTag


class CountLeafTag(LeafTag):
    required_data_fields = {"counts"}

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation("value", lambda v: isinstance(v, str))

    def process_tag(self, data):
        if self.get_param("value") is None:
            return str(sum(data["counts"].values()))

        if self.get_param("value") not in data["counts"]:
            return "0"

        return str(data["counts"][self.get_param("value")])
