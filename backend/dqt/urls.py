from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from .api import DataItemResource, ProgressMonitorDatasetResource

data_item_resource = DataItemResource()
progress_monitor_dataset_resource = ProgressMonitorDatasetResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(data_item_resource.urls)),
    url(r'^api/', include(progress_monitor_dataset_resource.urls)),
]
