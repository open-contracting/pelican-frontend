from django.urls import path

from exporter.views import generate_report

urlpatterns = [
    path("generate-report", generate_report, name="generate-report"),
]
