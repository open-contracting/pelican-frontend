var config = {
    apiBaseUrl: "http://localhost:8000/",
    apiEndpoints: {
        dataset: "api/dataset",
        resourceLevelStats: "api/resource_level_stats",
        datasetLevelStats: "api/dataset_level_stats",
        dataItem: "api/data_item",
    },
}

if (process.env.VUE_APP_SERVER == "kuba_dev01") {
    Object.assign(config, {
        apiBaseUrl: "http://localhost:22004/",
    });
}

if (process.env.NODE_ENV == "production") {
    Object.assign(config, {
        apiBaseUrl: "https://dqt.datlab.eu/",
    });
} else {
    Object.assign(config, {
        // development configuration here
    });
}

export const CONFIG = config;