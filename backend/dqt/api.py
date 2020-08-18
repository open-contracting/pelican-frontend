# myapp/api.py
from tastypie.fields import DictField, ToOneField, ListField, CharField, IntegerField, ListField
from tastypie.resources import ModelResource
from .models import (Dataset, DataItem, DatasetLevelCheck, FieldLevelCheck,
                     ProgressMonitorDataset, ResourceLevelCheck, Report, TimeVarianceLevelCheck)


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
    filtered_children_ids = ListField(attribute='get_filtered_children_ids', readonly=True)
    filtered_parent_id = IntegerField(attribute='get_filtered_parent_id', readonly=True)
    filtered_parent_name = CharField(attribute='get_filtered_parent_name', readonly=True)
    filter_message = DictField(attribute='get_filter_message', readonly=True)

    class Meta:
        queryset = Dataset.objects.all()
        resource_name = 'dataset'
        limit = 1000


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


class TimeVarianceLevelCheckResource(ModelResource):
    meta = DictField(attribute='meta')

    class Meta:
        queryset = TimeVarianceLevelCheck.objects.all()
        resource_name = 'time_variance_level_check'
        filtering = {
            "dataset": ('exact'),
        }
