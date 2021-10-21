var config = {
    apiBaseUrl: "/",
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
        createDatasetFilter: "api/create_dataset_filter",
        datasetFilterItems: "api/dataset_filter_items",
        createDatasetReport: "api/generate_report"
    }
};

if (process.env.VUE_APP_SERVER == "dev") {
    Object.assign(config, {
        apiBaseUrl: "/some_other_url"
    });
}

export const CONFIG = config;
