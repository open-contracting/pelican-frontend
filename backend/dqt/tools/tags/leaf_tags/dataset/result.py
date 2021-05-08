from dqt.tools.tags.tag import LeafTag


class ResultLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_required_data_field("result")

    def process_tag(self, data):
        if data["result"] is True:
            return "Passed"
        elif data["result"] is False:
            return "Failed"
        elif data["result"] is None:
            return "Undefined"
        else:
            raise ValueError("Unknown results: '%s'" % str(data["result"]))
