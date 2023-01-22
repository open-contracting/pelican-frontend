from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

from api import views

router = SimpleRouter()
router.register(r"datasets", views.DatasetViewSet, basename="dataset")
router.register(r"data_items", views.DataItemViewSet, basename="data-item")

urlpatterns = router.urls + [
    path("datasets/<pk>/field_level/<name>/", views.FieldLevelDetail.as_view()),
    path("datasets/<pk>/compiled_release_level/<name>/", views.ResourceLevelDetail.as_view()),
    # https://www.django-rest-framework.org/api-guide/schemas/#generating-a-dynamic-schema-with-schemaview
    path(
        "openapi",
        get_schema_view(
            title="Controller API", description="Endpoints for managing datasets in Pelican backend.", version="1.0.0"
        ),
        name="openapi-schema",
    ),
    # https://www.django-rest-framework.org/topics/documenting-your-api/#a-minimal-example-with-swagger-ui
    path(
        "swagger-ui/",
        TemplateView.as_view(template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"}),
        name="swagger-ui",
    ),
    path("api/dataset_filter_items", views.dataset_filter_items, name="dataset_filter_items"),
    path(
        "api/dataset_distinct_values/<dataset_id>/<json_path>",
        views.dataset_distinct_values,
        name="dataset_distinct_values",
    ),
    path(
        "api/dataset_distinct_values/<dataset_id>/<json_path>/<sub_string>",
        views.dataset_distinct_values,
        name="dataset_distinct_values",
    ),
]
