from django.urls import include, path
from processor import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"datasets", views.DatasetViewSet, basename="dataset")

urlpatterns = [
    path("api/create_dataset_filter", views.create_dataset_filter, name="create_dataset_filter"),
    path("", include(router.urls)),
]
