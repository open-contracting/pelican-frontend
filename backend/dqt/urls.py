from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from .api import (DatasetResource, DataItemResource, DatasetLevelCheckResource,
                  FieldLevelCheckResource, ProgressMonitorDatasetResource,
                  ResourceLevelCheckResource, ReportResource)
from .views import dataset_stats, dataset_level_stats, resource_level_stats, field_level_path_stats

dataset_resource = DatasetResource()
data_item_resource = DataItemResource()
progress_monitor_dataset_resource = ProgressMonitorDatasetResource()
field_level_check_resource = FieldLevelCheckResource()
resource_level_check_resource = ResourceLevelCheckResource()
dataset_level_check_resource = DatasetLevelCheckResource()
report_resource = ReportResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dataset_stats/<dataset_id>', dataset_stats, name='dataset_stats'),
    path('api/resource_level_stats/<dataset_id>', resource_level_stats, name='resource_level_stats'),
    path('api/dataset_level_stats/<dataset_id>', dataset_level_stats, name='dataset_level_stats'),
    path('api/field_level_path_stats/<dataset_id>/<path>', field_level_path_stats, name='field_level_path_stats'),
    url(r'^api/', include(dataset_resource.urls)),
    url(r'^api/', include(data_item_resource.urls)),
    url(r'^api/', include(progress_monitor_dataset_resource.urls)),
    url(r'^api/', include(field_level_check_resource.urls)),
    url(r'^api/', include(resource_level_check_resource.urls)),
    url(r'^api/', include(dataset_level_check_resource.urls)),
    url(r'^api/', include(report_resource.urls))
]
