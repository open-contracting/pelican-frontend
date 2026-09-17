import re

from django.conf import settings
from django.test import SimpleTestCase

from api.models import ProgressMonitorDataset
from exporter.template_tags.dataset import CHECK_TYPES

CONFIG = (settings.BASE_DIR / "frontend" / "src" / "config.ts").read_text()

ARRAY = r"export const {} = \[(.*?)\];"
DATASET_CHECKS = r"export const DATASET_CHECKS: Record<string, DatasetCheck \| undefined> = \{(.*)\n\};"


def array(name):
    """Return a string array that config.ts exports."""
    return re.findall(r'"([^"]+)"', re.search(ARRAY.format(name), CONFIG, re.DOTALL).group(1))


def dataset_checks():
    """Return the check types that config.ts declares, by check name."""
    body = re.search(DATASET_CHECKS, CONFIG, re.DOTALL).group(1)
    return {
        name: re.search(r'type: "(\w+)"', entry).group(1)
        for name, entry in re.findall(r'"([\w.]+)": \{([^}]*)\}', body)
    }


class ConstantsTests(SimpleTestCase):
    def test_dataset_checks(self):
        self.assertEqual(dataset_checks(), CHECK_TYPES)

    def test_states(self):
        self.assertEqual(array("STATES"), list(ProgressMonitorDataset.State.values))

    def test_phases(self):
        # The frontend's phases are the steps of the progress bar, which a deleted dataset never reaches.
        self.assertEqual([*array("PHASES"), "DELETED"], list(ProgressMonitorDataset.Phase.values))
