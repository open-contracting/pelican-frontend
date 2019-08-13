var config = {
    apiBaseUrl: "http://localhost:8000/",
    apiEndpoints: {
        resourceLevelStats: "api/resource_level_stats",
        datasetLevelStats: "api/dataset_level_stats",
    },
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