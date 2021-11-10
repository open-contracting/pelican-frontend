from django.urls import include, path

urlpatterns = [
    path("", include("dqt.urls"), name="api"),
    path("datasets/", include("processor.urls"), name="processor"),
    path("", include("exporter.urls"), name="exporter"),
]
