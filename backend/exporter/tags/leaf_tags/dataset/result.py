from exporter.tags.tag import LeafTag


class ResultLeafTag(LeafTag):
    required_data_fields = {"result"}

    def process_tag(self, data):
        if data["result"] is True:
            return "Passed"
        elif data["result"] is False:
            return "Failed"
        elif data["result"] is None:
            return "Undefined"
        else:
            raise ValueError("Unknown results: '%s'" % str(data["result"]))
