var config = {
    apiBaseUrl: process.env.VUE_APP_API_BASE_URL,
    apiEndpoints: {
        dataset: "api/dataset",
        dataItem: "api/data_item",
        // Stats
        fieldStats: "api/field_level_stats",
        resourceLevelStats: "api/resource_level_stats",
        datasetLevelStats: "api/dataset_level_stats",
        timeVarianceLevelStats: "api/time_variance_level_stats",
        // Detail
        fieldDetail: "api/field_level_detail",
        resourceLevelCheckDetail: "api/resource_level_detail",
        // Rest
        datasetFilterItems: "api/dataset_filter_items",
        datasetDistinctValues: "api/dataset_distinct_values",
        // Controller
        createDatasetFilter: "datasets/{id}/filter/",
        // Exporter
        createDatasetReport: "api/generate_report"
    }
};

export const CONFIG = config;
