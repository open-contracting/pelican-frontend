from django.urls import include, path

urlpatterns = [
    path("", include("api.urls"), name="api"),
    path("", include("exporter.urls"), name="exporter"),
]
