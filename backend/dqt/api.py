# myapp/api.py
from tastypie.fields import DictField, ToOneField, ListField, CharField, IntegerField
from tastypie.resources import ModelResource
from .models import (Dataset, DataItem, DatasetLevelCheck, FieldLevelCheck,
                     ProgressMonitorDataset, ResourceLevelCheck, Report)


class DataItemResource(ModelResource):
    id = IntegerField(attribute="id")
    data = DictField(attribute="data")

    class Meta:
        queryset = DataItem.objects.all()
        resource_name = 'data_item'


class ProgressMonitorDatasetResource(ModelResource):
    class Meta:
        queryset = ProgressMonitorDataset.objects.all()
        resource_name = 'dataset_progress'


class DatasetResource(ModelResource):
    meta = DictField(attribute='meta')
    state = CharField(attribute='get_state', readonly=True)
    phase = CharField(attribute='get_phase', readonly=True)
    size = IntegerField(attribute='get_size', readonly=True)

    class Meta:
        queryset = Dataset.objects.all()
        resource_name = 'dataset'


class ReportResource(ModelResource):
    data = DictField(attribute='data')

    class Meta:
        queryset = Report.objects.all()
        resource_name = 'report'


class ResourceLevelCheckResource(ModelResource):
    result = DictField(attribute='result')

    class Meta:
        queryset = ResourceLevelCheck.objects.all()
        resource_name = 'resource_level_check'


class FieldLevelCheckResource(ModelResource):
    result = DictField(attribute='result')

    class Meta:
        queryset = FieldLevelCheck.objects.all()
        resource_name = 'field_level_check'


class DatasetLevelCheckResource(ModelResource):
    class Meta:
        queryset = DatasetLevelCheck.objects.all()
        resource_name = 'dataset_level_check'
