from django.contrib.postgres.fields import JSONField
from django.db.models import (CASCADE, BigAutoField, BigIntegerField,
                              BooleanField, CharField, DateTimeField,
                              ForeignKey, IntegerField, Model)


class Dataset(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=255, blank=False)
    meta = JSONField()
    ancestor_id = BigIntegerField(blank=True, null=True)
    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    def get_state(self):
        for item in self.progress.all():
            return item.state

    def get_phase(self):
        for item in self.progress.all():
            return item.phase

    def get_size(self):
        for item in self.progress.all():
            return item.size

    class Meta:
        app_label = "data"
        managed = False
        db_table = "dataset"


class Report(Model):
    id = BigAutoField(primary_key=True)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)
    type = CharField(max_length=-1, blank=True, null=True)
    data = JSONField()
    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = "report"


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
    data_item = ForeignKey("DataItem", db_column="data_item_id", on_delete=CASCADE)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)
    result = JSONField()
    data_item = ForeignKey("DataItem", db_column="data_item_id", on_delete=CASCADE)

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'field_level_check'


class TimeVarianceLevelCheck(Model):
    id = BigAutoField(primary_key=True)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)

    check_name = CharField(max_length=-1, blank=True, null=True)
    coverage_result = BooleanField(blank=True, null=True)
    coverage_value = IntegerField(blank=True, null=True)
    check_result = BooleanField(blank=True, null=True)
    check_value = IntegerField(blank=True, null=True)
    meta = JSONField()

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'time_variance_level_check'


class ProgressMonitorDataset(Model):
    id = BigAutoField(primary_key=True)
    dataset = ForeignKey("Dataset", related_name='progress', db_column="dataset_id", to_field="id", on_delete=CASCADE)
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
    data_item = ForeignKey("DataItem", db_column="data_item_id", on_delete=CASCADE)
    dataset = ForeignKey("Dataset", db_column="dataset_id", to_field="id", on_delete=CASCADE)
    result = JSONField()
    data_item = ForeignKey("DataItem", db_column="data_item_id", on_delete=CASCADE)

    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'resource_level_check'
