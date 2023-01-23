import random

from exporter.elements import multiple_line_elements
from exporter.tags.tag import LeafTag
from exporter.util import MODES, PERCENTAGE_RANGES, terms_enumeration


class ExamplesLeafTag(LeafTag):
    required_data_fields = {"examples"}

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "percentageRange",
            lambda v: v in PERCENTAGE_RANGES,
            description="The value must be one of the following: %s." % terms_enumeration(PERCENTAGE_RANGES),
        )
        self.set_param_validation("max", lambda v: v.isdigit(), description="The value must be a positive integer.")
        self.set_param_validation(
            "mode",
            lambda v: v in MODES,
            description="The value must be one of the following: %s." % terms_enumeration(MODES),
        )

    def process_tag(self, data):
        if self.get_param("percentageRange") is not None:
            percentage_range_examples = data["examples"][self.get_param("percentageRange")]
        else:
            percentage_range_examples = [example for examples in data["examples"].values() for example in examples]

        max_count = self.get_param("max")
        if max_count is None:
            max_count = len(percentage_range_examples)

        examples = random.sample(percentage_range_examples, k=int(max_count))

        mode = self.get_param("mode", "oneLine")

        if mode == "oneLine":
            return ", ".join(examples)
        # multipleLines
        return multiple_line_elements(examples)
