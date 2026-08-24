from django.contrib import admin

from accounts.models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name", "spider"]
    ordering = ["name"]
    search_fields = ["name", "spider"]
    filter_horizontal = ["users"]
