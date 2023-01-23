import random

from exporter.elements import multiple_line_elements
from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

MODES = ("oneLine", "multipleLines")


def generate_examples_leaf_tag(key):
    class ExamplesLeafTag(LeafTag):
        def __init__(self, gdocs, dataset_id):
            super().__init__(self.process_tag, gdocs, dataset_id)

            self.set_param_validation(
                "max", lambda v: v.isdigit(), description="The value must be a positive integer."
            )
            self.set_param_validation(
                "mode",
                lambda v: v in MODES,
                description="The value must be one of the following: %s." % terms_enumeration(MODES),
            )

            self.set_required_data_field(key)

        def process_tag(self, data):
            max_count = self.get_param("max")
            if max_count is None:
                max_count = len(data[key])

            # Choosing examples, if max count bigger than sample size, choosing all the samples instead
            examples = random.sample(data[key], k=min(len(data[key]), int(max_count)))

            if self.get_param("mode", "oneLine") == "oneLine":
                return ", ".join(examples)
            # multipleLines
            return multiple_line_elements(examples)

    return ExamplesLeafTag
