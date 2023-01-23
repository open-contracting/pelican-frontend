from exporter import graphs
from exporter.elements import image_element
from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

TYPES = {"bar"}


class CountsResultBoxImageLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "type",
            lambda v: v in TYPES,
            description="The value must be one of the following: %s." % terms_enumeration(TYPES),
        )

        self.set_required_data_field("name")
        self.set_required_data_field("counts_pairs")

    def process_tag(self, data):
        if self.get_param("type", "bar") == "bar":
            buffer, aspect_ratio = graphs.bar_result_box(data["counts_pairs"], return_aspect_ratio=True)

        image_file_path = self.gdocs.add_image_file(buffer, "resultBoxImage_%s.png" % data["name"])
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
