from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter

from controller import views

router = SimpleRouter()
router.register(r"", views.DatasetViewSet, basename="dataset")

urlpatterns = router.urls + [path("docs/", include_docs_urls(public=False))]
