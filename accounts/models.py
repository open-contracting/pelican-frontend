from django.conf import settings
from django.db import models


class Publisher(models.Model):
    """A publisher, and the users who see the datasets in its namespace."""

    name = models.TextField(help_text="The publisher's name")
    # A ForeignKey to api.Dataset is impossible, because the two models are in different databases.
    spider = models.TextField(unique=True, help_text="The spider's name in Kingfisher Collect")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="publishers")

    def __str__(self):
        return self.name


class Profile(models.Model):
    """A user's preferences, which follow them between browsers."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    language = models.TextField(blank=True, help_text="The user's preferred language")

    def __str__(self):
        return str(self.user)
