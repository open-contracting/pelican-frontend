# PostgreSQL allows `character varying` without a length specifier. However, Django requires `max_length` on
# `CharField`. As such, we set `max_length=255` on:
#
# - Report.type: an ENUM with known length strings
# - FieldLevelCheckExamples.path: with a maximum witnessed length of 75
# - ResourceLevelCheckExamples.check_name
# - DatasetLevelCheck.check_name
# - TimeVarianceLevelCheck.check_name
#
# https://code.djangoproject.com/ticket/14094
# https://www.postgresql.org/docs/current/datatype-character.html
from django.db import models


class DataItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.JSONField()
    dataset = models.ForeignKey("Dataset", on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "data_item"


class Dataset(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    meta = models.JSONField(blank=True, default=dict)
    ancestor_id = models.BigIntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dataset"


class DatasetFilter(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name="children", db_column="dataset_id_original"
    )
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name="filtered", db_column="dataset_id_filtered"
    )
    filter_message = models.JSONField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dataset_filter"


class DatasetLevelCheck(models.Model):
    id = models.BigAutoField(primary_key=True)
    check_name = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    result = models.BooleanField(blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    meta = models.JSONField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dataset_level_check"


class ExchangeRates(models.Model):
    id = models.BigAutoField(primary_key=True)
    valid_on = models.DateField(unique=True)
    rates = models.JSONField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "exchange_rates"


class FieldLevelCheck(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_item = models.ForeignKey(DataItem, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    result = models.JSONField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "field_level_check"


class FieldLevelCheckExamples(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "field_level_check_examples"


class ProgressMonitorDataset(models.Model):
    class State(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS"
        OK = "OK"

    class Phase(models.TextChoices):
        CONTRACTING_PROCESS = "CONTRACTING_PROCESS"
        DATASET = "DATASET"
        TIME_VARIANCE = "TIME_VARIANCE"
        CHECKED = "CHECKED"
        DELETED = "DELETED"

    id = models.BigAutoField(primary_key=True)
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name="progress")
    state = models.CharField(max_length=255, blank=True, null=True, choices=State.choices)  # noqa: DJ001
    phase = models.CharField(max_length=255, blank=True, null=True, choices=Phase.choices)  # noqa: DJ001
    size = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "progress_monitor_dataset"


class ProgressMonitorItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    data_item = models.ForeignKey(DataItem, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "progress_monitor_item"
        unique_together = (("dataset", "data_item"),)


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    data = models.JSONField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "report"


class ResourceLevelCheck(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_item = models.ForeignKey(DataItem, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    result = models.JSONField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "resource_level_check"


class ResourceLevelCheckExamples(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
    check_name = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "resource_level_check_examples"


class TimeVarianceLevelCheck(models.Model):
    id = models.BigAutoField(primary_key=True)
    check_name = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    coverage_result = models.BooleanField(blank=True, null=True)
    coverage_value = models.IntegerField(blank=True, null=True)
    check_result = models.BooleanField(blank=True, null=True)
    check_value = models.IntegerField(blank=True, null=True)
    meta = models.JSONField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "time_variance_level_check"
