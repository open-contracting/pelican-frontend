# myapp/api.py
from tastypie.resources import ModelResource

from .models import DataItem, ProgressMonitorDataset


class DataItemResource(ModelResource):
    class Meta:
        queryset = DataItem.objects.all()
        resource_name = 'data_item'


class ProgressMonitorDatasetResource(ModelResource):
    class Meta:
        queryset = ProgressMonitorDataset.objects.all()
        resource_name = 'dataset'
