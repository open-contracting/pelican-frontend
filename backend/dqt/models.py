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

    def get_filtered_children_ids(self):
        return [
            item.dataset_filtered.id
            for item in self.dataset_filter_parent.all()
        ]

    def get_filtered_parent_id(self):
        items = self.dataset_filter_child.all()
        return items[0].dataset_original.id if items else None

    def get_filtered_parent_name(self):
        items = self.dataset_filter_child.all()
        return items[0].dataset_original.name if items else None

    def get_filter_message(self):
        items = self.dataset_filter_child.all()
        return items[0].filter_message if items else None

    class Meta:
        app_label = "data"
        managed = False
        db_table = "dataset"


class DatasetFilter(Model):
    id = BigAutoField(primary_key=True)
    dataset_original = ForeignKey(
        "Dataset", related_name='dataset_filter_parent', db_column="dataset_id_original",
        to_field="id", on_delete=CASCADE
    )
    dataset_filtered = ForeignKey(
        "Dataset", related_name='dataset_filter_child', db_column="dataset_id_filtered",
        to_field="id", on_delete=CASCADE
    )
    filter_message = JSONField()
    created = DateTimeField(blank=True, null=True)
    modified = DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "data"
        managed = False
        db_table = 'dataset_filter'


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
