from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db import models

from accounts.models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": AdminTextInputWidget}}
    list_display = ["name", "spider"]
    ordering = ["name"]
    search_fields = ["name", "spider"]
    filter_horizontal = ["users"]
