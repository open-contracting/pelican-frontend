from django.urls import include, path

urlpatterns = [
    path("api/", include("api.urls"), name="api"),
    path("api/", include("exporter.urls"), name="exporter"),
]
