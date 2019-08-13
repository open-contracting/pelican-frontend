var config = {
    api: {
        baseUrl: "http://localhost:8000/",
        endpoints: {
            resourceLevelStats: "api/resource_level_stats",
        },
    },
}

if (process.env.NODE_ENV == "production") {
    Object.assign(config, {
        api: {
            baseUrl: "https://dqt.datlab.eu/",
            endpoints: {
                resourceLevelStats: "api/resource_level_stats",
            },
        },
    });
} else {
    Object.assign(config, {
        // development configuration here
    });
}

export const CONFIG = config;