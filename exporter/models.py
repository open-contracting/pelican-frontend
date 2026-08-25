from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Export(models.Model):
    """A request to export a report to Google Drive, and its result."""

    class Status(models.TextChoices):
        WAITING = "waiting"
        OK = "ok"
        ERROR = "error"
        TEMPLATE_ERROR = "template_error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exports")
    # A ForeignKey to api.Dataset is impossible, because the two models are in different databases.
    dataset_id = models.BigIntegerField(help_text="The dataset's ID")
    template_id = models.TextField(help_text="The ID of the Google Docs template")
    folder_id = models.TextField(help_text="The ID of the Google Drive folder in which to create the report")
    language = models.TextField(blank=True, help_text="The report's language, defaulting to English")
    name = models.TextField(blank=True, help_text="The report's filename, defaulting to a generated name")
    status = models.TextField(
        choices=Status,
        default=Status.WAITING,
        help_text="Whether the report is waiting to be created, was created, or failed",
    )
    document_id = models.TextField(blank=True, help_text="The ID of the exported document in Google Docs")
    reason = models.TextField(blank=True, help_text="The reason the report couldn't be created")
    failed_checks = ArrayField(
        models.TextField(), blank=True, default=list, help_text="The checks that couldn't be computed"
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Export {self.pk} of dataset {self.dataset_id}"


class ExportError(models.Model):
    """An error that stopped a template from rendering."""

    export = models.ForeignKey(Export, on_delete=models.CASCADE, related_name="errors")
    reason = models.TextField(help_text="The reason the template couldn't be rendered")
    tag = models.TextField(blank=True, help_text="The tag as extracted from the template")
    template_id = models.TextField(blank=True, help_text="The ID of the Google Docs template")

    def __str__(self):
        return self.reason
