from processor import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"datasets", views.DatasetViewSet, basename="dataset")

urlpatterns = router.urls
