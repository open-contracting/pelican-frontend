from django.urls import path
from processor import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"", views.DatasetViewSet, basename="dataset")

urlpatterns = router.urls + [path("docs/", include_docs_urls(public=False))]
