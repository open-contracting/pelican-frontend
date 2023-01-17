from django.urls import include, path

urlpatterns = [
    path("", include("api.urls"), name="api"),
    path("datasets/", include("controller.urls"), name="controller"),
    path("", include("exporter.urls"), name="exporter"),
]
