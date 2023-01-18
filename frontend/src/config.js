var config = {
    apiBaseUrl: process.env.VUE_APP_API_BASE_URL,
    apiEndpoints: {
        dataset: "api/dataset",
        resourceLevelStats: "api/resource_level_stats",
        resourceLevelCheckDetail: "api/resource_level_detail",
        datasetLevelStats: "api/dataset_level_stats",
        timeVarianceLevelStats: "api/time_variance_level_stats",
        dataItem: "api/data_item",
        fieldStats: "api/field_level_stats",
        fieldDetail: "api/field_level_detail",
        datasetDistinctValues: "api/dataset_distinct_values",
        createDatasetFilter: "datasets/{id}/filter/",
        datasetFilterItems: "api/dataset_filter_items",
        createDatasetReport: "api/generate_report"
    }
};

export const CONFIG = config;
