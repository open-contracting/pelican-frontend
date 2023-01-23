from exporter.tags.tag import LeafTag


class ValueLeafTag(LeafTag):
    required_data_fields = {"value"}

    def process_tag(self, data):
        if data["value"] is None:
            return "Undefined"
        else:
            return str(data["value"])
