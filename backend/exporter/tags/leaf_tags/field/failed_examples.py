import random

from exporter.elements import multiple_line_elements
from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

LEVELS = ("coverage", "coverageSet", "coverageEmpty", "quality")
MODES = ("oneLine", "multipleLines")


class FailedExamplesLeafTag(LeafTag):
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

        self.set_required_data_field("coverageFailedExamples")
        self.set_required_data_field("coverageSetFailedExamples")
        self.set_required_data_field("coverageEmptyFailedExamples")
        self.set_required_data_field("qualityFailedExamples")

    def process_tag(self, data):
        all_examples = data["%sFailedExamples" % self.get_param("level")]

        max_count = self.get_param("max")
        if max_count is None:
            max_count = len(all_examples)

        # Choosing examples, if max count bigger than sample size, choosing all the samples instead
        examples = random.sample(all_examples, k=min(len(all_examples), int(max_count)))

        mode = self.get_param("mode", "oneLine")

        if mode == "oneLine":
            return ", ".join(examples)
        # multipleLines
        return multiple_line_elements(examples)
