from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from .api import (DataItemResource, DatasetLevelCheckResource,
                  FieldLevelCheckResource, ProgressMonitorDatasetResource,
                  ResourceLevelCheckResource)
from .views import resource_level_stats

data_item_resource = DataItemResource()
progress_monitor_dataset_resource = ProgressMonitorDatasetResource()
field_level_check_resource = FieldLevelCheckResource()
resource_level_check_resource = ResourceLevelCheckResource()
dataset_level_check_resource = DatasetLevelCheckResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/resource_level_stats/<dataset_id>', resource_level_stats, name='resource_level_stats'),
    url(r'^api/', include(data_item_resource.urls)),
    url(r'^api/', include(progress_monitor_dataset_resource.urls)),
    url(r'^api/', include(field_level_check_resource.urls)),
    url(r'^api/', include(resource_level_check_resource.urls)),
    url(r'^api/', include(dataset_level_check_resource.urls)),
]
