var config = {
    apiBaseUrl: process.env.VUE_APP_API_BASE_URL,
    apiEndpoints: {
        // List/detail
        dataset: "datasets/",
        dataItem: "api/data_item",
        // Check stats
        fieldStats: "api/field_level_stats",
        resourceLevelStats: "api/resource_level_stats",
        datasetLevelStats: "api/dataset_level_stats",
        timeVarianceLevelStats: "api/time_variance_level_stats",
        // Check detail
        fieldDetail: "api/field_level_detail",
        resourceLevelCheckDetail: "api/resource_level_detail",
        // Filter datasets
        datasetFilterItems: "api/dataset_filter_items",
        datasetDistinctValues: "api/dataset_distinct_values",
        // Controller
        createDatasetFilter: "datasets/{id}/filter/",
        // Exporter
        createDatasetReport: "api/generate_report"
    }
};

export const CONFIG = config;
