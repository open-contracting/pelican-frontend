from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

from controller import views

router = SimpleRouter()
router.register(r"", views.DatasetViewSet, basename="dataset")

urlpatterns = router.urls + [
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
]
