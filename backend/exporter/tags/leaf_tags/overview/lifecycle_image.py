from exporter import graphs
from exporter.elements import image_element
from exporter.tags.tag import LeafTag


class LifecycleImageLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.required_data_fields = {"lifecycle_object_counts"}

    def process_tag(self, data):
        buffer, aspect_ratio = graphs.lifecycle_image(
            planning_count=data["lifecycle_object_counts"]["planning"],
            tender_count=data["lifecycle_object_counts"]["tender"],
            award_count=data["lifecycle_object_counts"]["award"],
            contract_count=data["lifecycle_object_counts"]["contract"],
            implementation_count=data["lifecycle_object_counts"]["implementation"],
            return_aspect_ratio=True,
        )
        image_file_path = self.gdocs.add_image_file(buffer, "LifecycleImage.png")
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
