from exporter import graphs
from exporter.elements import image_element
from exporter.tags.tag import LeafTag


class TableResultBoxImageLeafTag(LeafTag):
    required_data_fields = {"name", "counts_pairs", "total_count"}

    def process_tag(self, data):
        buffer, aspect_ratio = graphs.table_result_box(
            data["counts_pairs"], total_count=data["total_count"], return_aspect_ratio=True
        )

        image_file_path = self.gdocs.add_image_file(buffer, "resultBoxImage_%s.png" % data["name"])
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
