from exporter import graphs
from exporter.elements import image_element
from exporter.tags.tag import LeafTag


class PassedResultBoxImageLeafTag(LeafTag):
    required_data_fields = {"name", "passedCount", "failedCount"}

    def process_tag(self, data):
        buffer, aspect_ratio = graphs.passed_result_box(
            data["passedCount"], data["failedCount"], return_aspect_ratio=True
        )
        image_file_path = self.gdocs.add_image_file(
            buffer, "resultBoxImage_%s_%s.png" % (self.get_param("level"), data["name"])
        )
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
