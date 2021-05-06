import datetime

from dqt.tools import graphs
from dqt.tools.elements import image_element
from dqt.tools.misc import parse_month_year
from dqt.tools.tags.tag import LeafTag


class ReleaseDateDistributionImageLeafTag(LeafTag):
    MONTH_YEAR_FORMAT = "%b-%-y"

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "from",
            lambda v: parse_month_year(v) is not None,
            description="The value must be in the following format: <month>-<year> (e.g. Feb-19).",
        )
        self.set_param_validation(
            "to",
            lambda v: parse_month_year(v) is not None,
            description="The value must be in the following format: <month>-<year> (e.g. Feb-19).",
        )

        self.set_required_data_field("period_pairs")

    def process_tag(self, data):
        if self.get_param("from") is not None:
            from_d = parse_month_year(self.get_param("from"))
        else:
            from_d = datetime.datetime.min

        if self.get_param("to") is not None:
            to_d = parse_month_year(self.get_param("to"))
        else:
            to_d = datetime.datetime.max

        filter_period_pairs = []
        for period_str, count in data["period_pairs"]:
            period_d = parse_month_year(period_str)
            if from_d <= period_d <= to_d:
                filter_period_pairs.append((period_str, count))

        buffer, aspect_ratio = graphs.histogram_result_box(filter_period_pairs, return_aspect_ratio=True)
        image_file_path = self.gdocs.add_image_file(buffer, "ReleaseDateDistributionImage.png")
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
