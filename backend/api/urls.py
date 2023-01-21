from django.urls import path

from api.views import dataset_distinct_values, dataset_filter_items, resource_level_detail

urlpatterns = [
    # Check details
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
