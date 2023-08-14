var config = {
    apiBaseUrl: process.env.VUE_APP_API_BASE_URL || "/api/",
    apiEndpoints: {
        // GET
        dataset: "datasets/",
        dataItem: "data_items/{id}/",
        fieldLevelReport: "datasets/{id}/field_level_report/",
        resourceLevelReport: "datasets/{id}/compiled_release_level_report/",
        datasetLevelReport: "datasets/{id}/dataset_level_report/",
        timeVarianceLevelReport: "datasets/{id}/time_based_report/",
        fieldLevelDetail: "datasets/{id}/field_level/{name}/",
        resourceLevelDetail: "datasets/{id}/compiled_release_level/{name}/",
        datasetFilterItems: "dataset-filter-items/",
        datasetDistinctValues: "dataset-distinct-values/",
        // POST
        createDatasetFilter: "datasets/{id}/filter/",
        createDatasetReport: "generate-report"
    }
};

export const CONFIG = config;
