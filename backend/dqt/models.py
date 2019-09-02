from django.contrib.postgres.fields import JSONField
from django.db.models import (CASCADE, BigAutoField, BigIntegerField,
                              BooleanField, CharField, DateTimeField,
                              ForeignKey, IntegerField, Model)

class Dataset(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=255, blank=False)
    meta = JSONField()
    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = "dataset"


class DataItem(Model):
    id = BigAutoField(primary_key=True)
    data = JSONField()
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)
    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'data_item'


class DatasetLevelCheck(Model):
    id = BigAutoField(primary_key=True)
    check_name = CharField(max_length=-1, blank=True, null=True)
    result = BooleanField(blank=True, null=True)
    value = IntegerField(blank=True, null=True)
    meta = JSONField()
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'dataset_level_check'


class FieldLevelCheck(Model):
    id = BigAutoField(primary_key=True)
    path = CharField(max_length=-1, blank=True, null=True)
    result = BooleanField(blank=True, null=True)
    meta = JSONField()
    data_item = ForeignKey("DataItem", db_column="data_item_id", on_delete=CASCADE)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'field_level_check'


class ProgressMonitorDataset(Model):
    id = BigAutoField(primary_key=True)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)
    state = CharField(max_length=255, blank=True, null=True)
    phase = CharField(max_length=255, blank=True, null=True)
    size = IntegerField(blank=True, null=True)

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'progress_monitor_dataset'


class ProgressMonitorItem(Model):
    id = BigAutoField(primary_key=True)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)
    data_item = ForeignKey("DataItem", db_column="item_id", on_delete=CASCADE)
    state = CharField(max_length=255, blank=True, null=True)

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'progress_monitor_item'
        unique_together = (('dataset_id', 'item_id'),)


class ResourceLevelCheck(Model):
    id = BigAutoField(primary_key=True)
    check_name = CharField(max_length=-1, blank=True, null=True)
    result = BooleanField(blank=True, null=True)
    pass_count = IntegerField(blank=True, null=True)
    application_count = IntegerField(blank=True, null=True)
    meta = JSONField()
    data_item = ForeignKey("DataItem", db_column="data_item_id", on_delete=CASCADE)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'resource_level_check'
