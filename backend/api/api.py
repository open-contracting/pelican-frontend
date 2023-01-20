# myapp/api.py
from tastypie.fields import DictField, IntegerField
from tastypie.resources import ModelResource

from api.models import DataItem


class DataItemResource(ModelResource):
    id = IntegerField(attribute="id")
    data = DictField(attribute="data")

    class Meta:
        queryset = DataItem.objects.all()
        resource_name = "data_item"
