import random

from exporter.elements import multiple_line_elements
from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration


class ExamplesLeafTag(LeafTag):
    RANKS = {"1", "2", "3", "4", "5"}
    MODES = ("oneLine", "multipleLines")

    def __init__(self, gdocs, dataset_id):
        super().__init__(self.process_tag, gdocs, dataset_id)

        self.set_param_validation(
            "rank",
            lambda v: v in ExamplesLeafTag.RANKS,
            description="The value must be one of the following: %s." % terms_enumeration(ExamplesLeafTag.RANKS),
        )
        self.set_param_validation("max", lambda v: v.isdigit(), description="The value must be a positive integer.")
        self.set_param_validation(
            "mode",
            lambda v: v in ExamplesLeafTag.MODES,
            description="The value must be one of the following: %s." % terms_enumeration(ExamplesLeafTag.MODES),
        )

        self.set_required_data_field("examples")

    def process_tag(self, data):
        if self.get_param("rank") is not None:
            rank_examples = data["examples"][self.get_param("rank")]
        else:
            rank_examples = [example for examples in data["examples"].values() for example in examples]

        max_count = self.get_param("max")
        if max_count is None:
            max_count = len(rank_examples)

        examples = random.sample(rank_examples, k=int(max_count))

        mode = self.get_param("mode")
        if mode is None:
            mode = "oneLine"

        if mode == "oneLine":
            return ", ".join(examples)
        elif mode == "multipleLines":
            return multiple_line_elements(examples)
