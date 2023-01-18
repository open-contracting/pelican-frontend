from django.urls import path

from exporter.views import generate_report

urlpatterns = [
    path("api/generate_report", generate_report, name="generate_report"),
]
