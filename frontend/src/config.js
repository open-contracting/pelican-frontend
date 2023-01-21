var config = {
    apiBaseUrl: process.env.VUE_APP_API_BASE_URL,
    apiEndpoints: {
        dataset: "datasets/",
        dataItem: "data_items/{id}/",
        fieldLevelReport: "datasets/{id}/field_level_report/",
        resourceLevelReport: "datasets/{id}/compiled_release_level_report/",
        datasetLevelReport: "datasets/{id}/dataset_level_report/",
        timeVarianceLevelReport: "datasets/{id}/time_based_report/",
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
