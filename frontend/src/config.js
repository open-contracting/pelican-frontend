export const CONFIG = {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || "/api/",
    apiEndpoints: {
        // GET
        settings: "settings/",
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
        createDatasetReport: "generate-report",
    },
};

export const REPORT_ONLY_CHECKS = {
    "distribution.tender_award_criteria": true,
    "distribution.tender_submission_method": true,
    "distribution.milestone_type": true,
    "distribution.document_document_type": true,
    "distribution.value_currency": true,
    "distribution.related_process_relation": true,
};

// Keep in sync with CHECK_TYPES in dataset.py
export const CHECK_TYPES = {
    // donut
    "distribution.main_procurement_category": "donut",
    "distribution.tender_status": "donut",
    "distribution.tender_procurement_method": "donut",
    "distribution.tender_award_criteria": "donut",
    "distribution.tender_submission_method": "donut",
    "distribution.awards_status": "donut",
    "distribution.contracts_status": "donut",
    "distribution.milestone_status": "donut",
    "distribution.milestone_type": "donut",
    "distribution.document_document_type": "donut",
    "distribution.value_currency": "donut",
    "distribution.related_process_relation": "donut",
    // bar
    "distribution.tender_value": "bar",
    "distribution.contracts_value": "bar",
    "distribution.awards_value": "bar",
    // numeric
    "misc.url_availability": "numeric",
    "unique.tender_id": "numeric",
    "consistent.related_process_title": "numeric",
    "reference.related_process_identifier": "numeric",
    // top3
    "distribution.tender_value_repetition": "top3",
    "distribution.contracts_value_repetition": "top3",
    "distribution.awards_value_repetition": "top3",
    // biggest_share
    "distribution.buyer_repetition": "biggest_share",
    // single_value_share
    "distribution.buyer": "single_value_share",
};

// Keep in sync with check descriptions.
export const CHECK_TICKS = {
    // donut
    "distribution.main_procurement_category": [0, 0.95],
    "distribution.tender_status": [0.001, 0.99],
    "distribution.awards_status": [0.001, 0.99],
    "distribution.contracts_status": [0.001, 0.99],
    "distribution.milestone_status": [0.001, 0.99],
    "distribution.tender_procurement_method": [0.001, 0.99],
    // bar
    "distribution.tender_value": [0, 0.5],
    "distribution.contracts_value": [0, 0.5],
    "distribution.awards_value": [0, 0.5],
    // single_value_share
    "distribution.buyer": [0, 0.5],
};

// Keep in sync with check descriptions.
export const CHECK_STYLES = {
    // donut
    "distribution.main_procurement_category": [],
    "distribution.tender_status": ["active", "complete"],
    "distribution.awards_status": ["active"],
    "distribution.contracts_status": ["active", "terminated"],
    "distribution.milestone_status": ["met"],
    "distribution.tender_procurement_method": ["open"],
};
