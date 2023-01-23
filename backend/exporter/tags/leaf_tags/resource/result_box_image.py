from exporter import graphs
from exporter.elements import image_element
from exporter.tags.tag import LeafTag


class ResultBoxImageLeafTag(LeafTag):
    required_data_fields = {"name", "passedCount", "failedCount", "notAvailableCount"}

    def process_tag(self, data):
        buffer, aspect_ratio = graphs.resource_result_box(
            data["passedCount"], data["failedCount"], data["notAvailableCount"], return_aspect_ratio=True
        )
        image_file_path = self.gdocs.add_image_file(buffer, "resultBoxImage_%s.png" % data["name"])
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
