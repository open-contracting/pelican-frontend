from dqt.tools import graphs
from dqt.tools.elements import image_element
from dqt.tools.misc import terms_enumeration
from dqt.tools.tags.tag import LeafTag


class ResultBoxImageLeafTag(LeafTag):
    LEVELS = ("coverage", "coverageSet", "coverageEmpty", "quality")

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in ResultBoxImageLeafTag.LEVELS,
            description="The value must be one of the following: %s."
            % terms_enumeration(ResultBoxImageLeafTag.LEVELS),
            required=True,
        )
        # self.set_param_validation('check', lambda v: v in FieldTemplateTag.CHECKS)
        self.set_required_data_field("path")
        self.set_required_data_field("coveragePassedCount")
        self.set_required_data_field("coverageFailedCount")
        self.set_required_data_field("qualityPassedCount")
        self.set_required_data_field("qualityFailedCount")

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
