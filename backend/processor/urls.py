from django.urls import path

from .views import (
    create_dataset_filter,
    dataset_availability,
    dataset_id,
    dataset_metadata,
    dataset_progress,
    dataset_start,
    dataset_wipe,
)

urlpatterns = [
    path("api/create_dataset_filter", create_dataset_filter, name="create_dataset_filter"),
    path("api/dataset_status/<dataset_id>", dataset_progress, name="dataset_status"),
    path("api/dataset_id", dataset_id, name="dataset_id"),
    path("api/dataset_availability/<dataset_id>", dataset_availability, name="dataset_availability"),
    path("api/dataset_metadata/<dataset_id>", dataset_metadata, name="dataset_metadata"),
    path("api/dataset_start", dataset_start, name="dataset_start"),
    path("api/dataset_wipe", dataset_wipe, name="dataset_wipe"),
]
