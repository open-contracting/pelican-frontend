from django.urls import include, path

urlpatterns = [
    path("", include("dqt.urls"), name="api"),
    path("", include("exporter.urls"), name="exporter"),
]
