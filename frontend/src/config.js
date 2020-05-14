var config = {
    apiBaseUrl: "http://localhost:8000/",
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
        datasetFilterItems: "api/dataset_filter_items"
    }
};

if (process.env.VUE_APP_SERVER == "kuba_dev01") {
    Object.assign(config, {
        apiBaseUrl: "http://localhost:22004/"
    });
}

if (process.env.VUE_APP_SERVER == "mirek_dev01") {
    Object.assign(config, {
        apiBaseUrl: "http://localhost:25005/"
    });
}

if (process.env.NODE_ENV == "production") {
    Object.assign(config, {
        apiBaseUrl: "https://dqt.datlab.eu/"
    });
} else {
    Object.assign(config, {
        // development configuration here
    });
}

export const CONFIG = config;