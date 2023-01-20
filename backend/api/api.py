# myapp/api.py
from tastypie.fields import CharField, DictField, IntegerField, ListField
from tastypie.resources import ModelResource

from api.models import DataItem, Dataset


class DataItemResource(ModelResource):
    id = IntegerField(attribute="id")
    data = DictField(attribute="data")

    class Meta:
        queryset = DataItem.objects.all()
        resource_name = "data_item"


class DatasetResource(ModelResource):
    meta = DictField(attribute="meta")
    state = CharField(attribute="get_state", readonly=True)
    phase = CharField(attribute="get_phase", readonly=True)
    size = IntegerField(attribute="get_size", readonly=True)
    filtered_children_ids = ListField(attribute="get_filtered_children_ids", readonly=True)
    filtered_parent_id = IntegerField(attribute="get_filtered_parent_id", readonly=True)
    filtered_parent_name = CharField(attribute="get_filtered_parent_name", readonly=True)
    filter_message = DictField(attribute="get_filter_message", readonly=True)

    class Meta:
        queryset = Dataset.objects.all()
        resource_name = "dataset"
        limit = 1000
