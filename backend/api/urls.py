from django.urls import path

from api.views import (
    dataset_distinct_values,
    dataset_filter_items,
    dataset_level_stats,
    field_level_detail,
    field_level_stats,
    resource_level_detail,
    resource_level_stats,
    time_variance_level_stats,
)

urlpatterns = [
    # Check stats
    path("api/field_level_stats/<dataset_id>", field_level_stats, name="field_level_stats"),
    path("api/resource_level_stats/<dataset_id>", resource_level_stats, name="resource_level_stats"),
    path("api/dataset_level_stats/<dataset_id>", dataset_level_stats, name="dataset_level_stats"),
    path("api/time_variance_level_stats/<dataset_id>", time_variance_level_stats, name="time_variance_level_stats"),
    # Check details
    path("api/field_level_detail/<dataset_id>/<path>", field_level_detail, name="field_level_detail"),
    path("api/resource_level_detail/<dataset_id>/<check_name>", resource_level_detail, name="resource_level_detail"),
    # Filter datasets
    path("api/dataset_filter_items", dataset_filter_items, name="dataset_filter_items"),
    path(
        "api/dataset_distinct_values/<dataset_id>/<json_path>", dataset_distinct_values, name="dataset_distinct_values"
    ),
    path(
        "api/dataset_distinct_values/<dataset_id>/<json_path>/<sub_string>",
        dataset_distinct_values,
        name="dataset_distinct_values",
    ),
]
