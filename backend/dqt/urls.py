from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from .api import (DatasetResource, DataItemResource, DatasetLevelCheckResource,
                  FieldLevelCheckResource, ProgressMonitorDatasetResource,
                  ResourceLevelCheckResource, ReportResource, TimeVarianceLevelCheckResource)
from .views import dataset_stats, dataset_level_stats, field_level_stats, resource_level_stats, \
    field_level_detail, resource_level_detail, time_variance_level_stats, create_dataset_filter, \
    dataset_distinct_values, dataset_filter_items, generate_report

dataset_resource = DatasetResource()
data_item_resource = DataItemResource()
progress_monitor_dataset_resource = ProgressMonitorDatasetResource()
field_level_check_resource = FieldLevelCheckResource()
resource_level_check_resource = ResourceLevelCheckResource()
dataset_level_check_resource = DatasetLevelCheckResource()
report_resource = ReportResource()
time_variance_level_check_resource = TimeVarianceLevelCheckResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dataset_stats/<dataset_id>', dataset_stats, name='dataset_stats'),
    path('api/field_level_stats/<dataset_id>', field_level_stats, name='field_level_stats'),
    path('api/resource_level_stats/<dataset_id>', resource_level_stats, name='resource_level_stats'),
    path('api/dataset_level_stats/<dataset_id>', dataset_level_stats, name='dataset_level_stats'),
    path('api/time_variance_level_stats/<dataset_id>', time_variance_level_stats, name='time_variance_level_stats'),
    path('api/field_level_detail/<dataset_id>/<path>', field_level_detail, name='field_level_detail'),
    path('api/resource_level_detail/<dataset_id>/<check_name>', resource_level_detail, name='resource_level_detail'),
    path('api/create_dataset_filter', create_dataset_filter, name='create_dataset_filter'),
    path('api/dataset_filter_items', dataset_filter_items, name='dataset_filter_items'),
    path('api/dataset_distinct_values/<dataset_id>/<json_path>', dataset_distinct_values, name='dataset_distinct_values'),
    path('api/dataset_distinct_values/<dataset_id>/<json_path>/<sub_string>', dataset_distinct_values, name='dataset_distinct_values'),
    path('api/generate_report', generate_report, name='generate_report'),
    url(r'^api/', include(dataset_resource.urls)),
    url(r'^api/', include(data_item_resource.urls)),
    url(r'^api/', include(progress_monitor_dataset_resource.urls)),
    url(r'^api/', include(field_level_check_resource.urls)),
    url(r'^api/', include(resource_level_check_resource.urls)),
    url(r'^api/', include(dataset_level_check_resource.urls)),
    url(r'^api/', include(report_resource.urls)),
    url(r'^api/', include(time_variance_level_check_resource.urls))
]
