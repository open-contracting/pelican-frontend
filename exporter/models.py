from django.conf import settings
from django.db import models


class Export(models.Model):
    """A report requested by a user, and the outcome of exporting it to Google Drive."""

    class Status(models.TextChoices):
        WAITING = "waiting"
        OK = "ok"
        REPORT_ERROR = "report_error"
        TEMPLATE_ERROR = "template_error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exports")
    # A ForeignKey to api.Dataset is impossible, because the two models are in different databases.
    dataset_id = models.BigIntegerField(help_text="The dataset's ID")
    document_id = models.CharField(max_length=255, help_text="The ID of the Google Docs template")
    folder_id = models.CharField(
        max_length=255, help_text="The ID of the Google Drive folder in which to create the report"
    )
    language = models.CharField(max_length=255, blank=True, help_text="The report's language, defaulting to English")
    report_name = models.CharField(
        max_length=255, blank=True, help_text="The report's filename, defaulting to a generated name"
    )
    status = models.CharField(
        max_length=255,
        choices=Status,
        default=Status.WAITING,
        help_text="Whether the report is waiting to be created, was created, or failed",
    )
    file_id = models.CharField(max_length=255, blank=True, help_text="The ID of the Google Docs report")
    reason = models.TextField(blank=True, help_text="The reason the report could not be created")
    tag_errors = models.JSONField(
        blank=True, default=list, help_text="The errors that stopped the template from rendering"
    )
    failed_tags = models.JSONField(blank=True, default=list, help_text="The tags that could not be rendered")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Export {self.pk} of dataset {self.dataset_id}"
