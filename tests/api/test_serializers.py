import json
from pathlib import Path

from django.test import SimpleTestCase

from api.serializers import (
    DatasetLevelCheckSerializer,
    DatasetMetaSerializer,
    FieldLevelCheckDetailSerializer,
    FieldLevelCheckSerializer,
    ResourceLevelCheckDetailSerializer,
    ResourceLevelCheckSerializer,
    TimeVarianceLevelCheckSerializer,
)

# Entries from tests/fixtures/pelican-backend.sql.gz, written by the refreshfixtures command.
with (Path(__file__).parent.parent / "fixtures" / "reports.json").open() as f:
    REPORTS = json.load(f)


class SerializerTests(SimpleTestCase):
    """
    The report views return the ``report`` table's JSON verbatim. Nothing checks it against the serializers that
    describe it, so these tests do, using entries from the fixture.
    """

    def test_field_level_report(self):
        for path, check in REPORTS["field_level_report"].items():
            with self.subTest(path=path):
                serializer = FieldLevelCheckSerializer(data=check)

                self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_field_level_detail(self):
        serializer = FieldLevelCheckDetailSerializer(data=REPORTS["field_level_detail"])

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_compiled_release_level_report(self):
        for name, check in REPORTS["compiled_release_level_report"].items():
            with self.subTest(name=name):
                serializer = ResourceLevelCheckSerializer(data=check)

                self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_compiled_release_level_detail(self):
        serializer = ResourceLevelCheckDetailSerializer(data=REPORTS["compiled_release_level_detail"])

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_dataset_level_report(self):
        for name, check in REPORTS["dataset_level_report"].items():
            with self.subTest(name=name):
                serializer = DatasetLevelCheckSerializer(data=check)

                self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_time_based_report(self):
        for name, check in REPORTS["time_based_report"].items():
            with self.subTest(name=name):
                serializer = TimeVarianceLevelCheckSerializer(data=check)

                self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_dataset_meta(self):
        # The sparse entry's collection metadata is null, apart from its dates.
        # The in-progress entry has no Pelican metadata, since Pelican writes it last.
        for key in ("dataset_meta", "dataset_meta_sparse", "dataset_meta_in_progress"):
            with self.subTest(key=key):
                serializer = DatasetMetaSerializer(data=REPORTS[key])

                self.assertTrue(serializer.is_valid(), serializer.errors)
