from rest_framework.routers import SimpleRouter

from exporter.views import ExportViewSet

router = SimpleRouter(use_regex_path=False)
router.register(r"exports", ExportViewSet, basename="export")

urlpatterns = router.urls
