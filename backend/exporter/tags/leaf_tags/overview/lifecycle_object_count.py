from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

STAGES = {
    "planning",
    "tender",
    "award",
    "contract",
    "implementation",
}


class LifecycleObjectCountLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "stage",
            lambda v: v in STAGES,
            description="The value must be one of the following: %s." % terms_enumeration(STAGES),
            required=True,
        )

        self.required_data_fields = {"lifecycle_object_counts"}

    def process_tag(self, data):
        return str(data["lifecycle_object_counts"][self.get_param("stage")])
