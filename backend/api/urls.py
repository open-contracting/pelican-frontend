from django.urls import path
from drf_spectacular import views as drfviews
from rest_framework.routers import SimpleRouter

from api import views

router = SimpleRouter(use_regex_path=False)
router.register(r"datasets", views.DatasetViewSet, basename="dataset")
router.register(r"data_items", views.DataItemViewSet, basename="data-item")

urlpatterns = [
    *router.urls,
    # Django REST Framework's @action decorator uses underscores instead of hyphens (for field_level_report, etc.).
    # While we can override it, we instead allow the default behavior and use underscores here for consistency.
    # https://github.com/encode/django-rest-framework/pull/6891
    path("datasets/<int:pk>/field_level/<str:name>/", views.FieldLevelDetail.as_view()),
    path("datasets/<int:pk>/compiled_release_level/<str:name>/", views.ResourceLevelDetail.as_view()),
    path("schema/", drfviews.SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", drfviews.SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", drfviews.SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
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
