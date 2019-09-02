# myapp/api.py
from tastypie.resources import ModelResource

from .models import (Dataset, DataItem, DatasetLevelCheck, FieldLevelCheck,
                     ProgressMonitorDataset, ResourceLevelCheck)

class DatasetResource(ModelResource):
    class Meta:
        queryset = Dataset.objects.all()
        resource_name = 'dataset'


class DataItemResource(ModelResource):
    class Meta:
        queryset = DataItem.objects.all()
        resource_name = 'data_item'


class ProgressMonitorDatasetResource(ModelResource):
    class Meta:
        queryset = ProgressMonitorDataset.objects.all()
        resource_name = 'dataset'


class ResourceLevelCheckResource(ModelResource):
    class Meta:
        queryset = ResourceLevelCheck.objects.all()
        resource_name = 'resource_level_check'


class FieldLevelCheckResource(ModelResource):
    class Meta:
        queryset = FieldLevelCheck.objects.all()
        resource_name = 'field_level_check'

class DatasetLevelCheckResource(ModelResource):
    class Meta:
        queryset = DatasetLevelCheck.objects.all()
        resource_name = 'dataset_level_check'
