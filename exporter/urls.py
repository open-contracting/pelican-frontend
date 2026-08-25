from rest_framework.routers import SimpleRouter

from exporter import views

router = SimpleRouter(use_regex_path=False)
router.register(r"exports", views.ExportViewSet, basename="export")

urlpatterns = router.urls
