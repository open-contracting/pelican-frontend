from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

from api import views

router = SimpleRouter()
router.register(r"datasets", views.DatasetViewSet, basename="dataset")
router.register(r"data_items", views.DataItemViewSet, basename="data-item")

urlpatterns = router.urls + [
    # Django REST Framework's @action decorator uses underscores instead of hyphens (for field_level_report, etc.).
    # While we can override it, we instead allow the default behavior and use underscores here for consistency.
    # https://github.com/encode/django-rest-framework/pull/6891
    path("datasets/<pk>/field_level/<name>/", views.FieldLevelDetail.as_view()),
    path("datasets/<pk>/compiled_release_level/<name>/", views.ResourceLevelDetail.as_view()),
    # https://www.django-rest-framework.org/api-guide/schemas/#generating-a-dynamic-schema-with-schemaview
    path(
        "openapi",
        get_schema_view(
            title="API", description="Endpoints for managing datasets in Pelican backend.", version="1.0.0"
        ),
        name="openapi-schema",
    ),
    # https://www.django-rest-framework.org/topics/documenting-your-api/#a-minimal-example-with-swagger-ui
    path(
        "swagger-ui/",
        TemplateView.as_view(template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"}),
        name="swagger-ui",
    ),
    path("dataset-filter-items/", views.dataset_filter_items, name="dataset-filter-items"),
    path(
        "dataset-distinct-values/<dataset_id>/<field>/",
        views.dataset_distinct_values,
        name="dataset-distinct-values",
    ),
    path(
        "dataset-distinct-values/<dataset_id>/<field>/<query>/",
        views.dataset_distinct_values,
        name="dataset-distinct-values-query",
    ),
    path("settings/", views.app_settings, name="settings"),
]
