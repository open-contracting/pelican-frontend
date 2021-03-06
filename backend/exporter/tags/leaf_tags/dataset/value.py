from exporter.tags.tag import LeafTag


class ValueLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_required_data_field("value")

    def process_tag(self, data):
        if data["value"] is None:
            return "Undefined"
        else:
            return str(data["value"])
