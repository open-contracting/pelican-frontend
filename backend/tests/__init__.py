from django.db import connections
from django.test import TestCase

from api.models import (
    DataItem,
    Dataset,
    DatasetFilter,
    DatasetLevelCheck,
    FieldLevelCheck,
    FieldLevelCheckExamples,
    ProgressMonitorDataset,
    Report,
    ResourceLevelCheckExamples,
    TimeVarianceLevelCheck,
)


class PelicanTestCase(TestCase):
    databases = {"default", "data"}
    unmanaged = {
        DataItem,
        Dataset,
        DatasetFilter,
        DatasetLevelCheck,
        FieldLevelCheck,
        FieldLevelCheckExamples,
        ProgressMonitorDataset,
        Report,
        ResourceLevelCheckExamples,
        TimeVarianceLevelCheck,
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connections["data"].schema_editor() as schema_editor:
            for model in cls.unmanaged:
                schema_editor.create_model(model)

    @classmethod
    def tearDownClass(cls):
        with connections["data"].schema_editor() as schema_editor:
            for model in cls.unmanaged:
                schema_editor.delete_model(model)
        super().tearDownClass()

    def create(self, model, **kwargs):
        obj = model(**kwargs)
        obj.full_clean()
        obj.save()
        return obj
