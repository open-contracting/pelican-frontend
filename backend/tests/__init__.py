from django.db import connections
from django.test import TransactionTestCase

from api.models import DataItem, Dataset, FieldLevelCheck, ProgressMonitorDataset


class TestCase(TransactionTestCase):
    databases = {"default", "data"}
    unmanaged = {DataItem, Dataset, FieldLevelCheck, ProgressMonitorDataset}

    def setUp(self):
        with connections["data"].schema_editor() as schema_editor:
            for model in self.unmanaged:
                schema_editor.create_model(model)

    def tearDown(self):
        with connections["data"].schema_editor() as schema_editor:
            for model in self.unmanaged:
                schema_editor.delete_model(model)

    def create(self, model, **kwargs):
        obj = model(**kwargs)
        obj.full_clean()
        obj.save()
        return obj
