from exporter import graphs
from exporter.elements import image_element
from exporter.tags.tag import LeafTag
from exporter.util import LEVELS, terms_enumeration


class ResultBoxImageLeafTag(LeafTag):
    required_data_fields = {
        "path",
        "coveragePassedCount",
        "coverageFailedCount",
        "qualityPassedCount",
        "qualityFailedCount",
    }

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in LEVELS,
            description="The value must be one of the following: %s." % terms_enumeration(LEVELS),
            required=True,
        )

    def process_tag(self, data):
        buffer, aspect_ratio = graphs.passed_result_box(
            data["%sPassedCount" % self.get_param("level")],
            data["%sFailedCount" % self.get_param("level")],
            return_aspect_ratio=True,
        )
        image_file_path = self.gdocs.add_image_file(
            buffer, "resultBoxImage_%s_%s.png" % (self.get_param("level"), data["path"])
        )
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
