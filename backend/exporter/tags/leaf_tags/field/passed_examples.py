import random

from exporter.elements import multiple_line_elements
from exporter.tags.tag import LeafTag
from exporter.util import LEVELS, MODES, terms_enumeration


class PassedExamplesLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "level",
            lambda v: v in LEVELS,
            description="The value must be one of the following: %s." % terms_enumeration(LEVELS),
            required=True,
        )
        self.set_param_validation("max", lambda v: v.isdigit(), description="The value must be a positive integer.")
        self.set_param_validation(
            "mode",
            lambda v: v in MODES,
            description="The value must be one of the following: %s." % terms_enumeration(MODES),
        )

        self.set_required_data_field("coveragePassedExamples")
        self.set_required_data_field("coverageSetPassedExamples")
        self.set_required_data_field("coverageEmptyPassedExamples")
        self.set_required_data_field("qualityPassedExamples")

    def process_tag(self, data):
        all_examples = data["%sPassedExamples" % self.get_param("level")]
        max_count = self.get_param("max")
        if max_count is None:
            max_count = len(all_examples)

        examples = random.sample(all_examples, k=int(max_count))

        if self.get_param("mode", "oneLine") == "oneLine":
            return ", ".join(examples)
        # multipleLines
        return multiple_line_elements(examples)
