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

// Sync with Phase in services.py
export const PHASES = ["CONTRACTING_PROCESS", "DATASET", "TIME_VARIANCE", "CHECKED"];

// Sync with State in services.py
export const STATES = ["IN_PROGRESS", "OK"];

export const DATASET_CHECK_REPORT_ONLY = {
    "distribution.tender_award_criteria": true,
    "distribution.tender_submission_method": true,
    "distribution.milestone_type": true,
    "distribution.document_document_type": true,
    "distribution.value_currency": true,
    "distribution.related_process_relation": true,
};

// Sync with CHECK_TYPES in dataset.py
export const DATASET_CHECK_TYPES = {
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

// Sync with check descriptions.
export const DATASET_CHECK_TICKS = {
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

// Key order determines the order of the sections in the dataset-level view.
export const DATASET_CHECK_SECTIONS = {
    status_distribution: [
        "distribution.tender_status",
        "distribution.awards_status",
        "distribution.contracts_status",
        "distribution.milestone_status",
    ],
    value_distribution: ["distribution.tender_value", "distribution.awards_value", "distribution.contracts_value"],
    other_distribution: [
        "distribution.value_currency",
        "distribution.main_procurement_category",
        "distribution.tender_procurement_method",
        "distribution.tender_submission_method",
        "distribution.tender_award_criteria",
        "distribution.buyer",
        "distribution.document_document_type",
        "distribution.milestone_type",
        "distribution.related_process_relation",
    ],
    repetition: [
        "distribution.tender_value_repetition",
        "distribution.awards_value_repetition",
        "distribution.contracts_value_repetition",
        "distribution.buyer_repetition",
    ],
    other: [
        "misc.url_availability",
        "consistent.related_process_title",
        "reference.related_process_identifier",
        "unique.tender_id",
    ],
};

// Checks are assigned to a section by name prefix, in this order.
export const RESOURCE_CHECK_SECTIONS = ["reference", "consistent", "coherent"];

// Checks absent from this list sort after it, alphabetically.
export const RESOURCE_CHECK_ORDER = [
    "reference.buyer_in_parties",
    "reference.procuring_entity_in_parties",
    "reference.tenderer_in_parties",
    "reference.supplier_in_parties",
    "reference.payer_in_parties",
    "reference.payee_in_parties",
    "reference.contract_in_awards",
    "consistent.tender_value",
    "consistent.contracts_value",
    "consistent.contracts_implementation_transactions_value",
    "consistent.parties_roles",
    "consistent.period_duration_in_days",
    "consistent.number_of_tenderers",
    "consistent.buyer_in_parties_roles",
    "consistent.tenderer_in_parties_roles",
    "consistent.procuring_entity_in_parties_roles",
    "consistent.supplier_in_parties_roles",
    "consistent.payer_in_parties_roles",
    "consistent.payee_in_parties_roles",
    "consistent.buyer_name_in_parties",
    "consistent.tenderer_name_in_parties",
    "consistent.procuring_entity_name_in_parties",
    "consistent.supplier_name_in_parties",
    "consistent.payer_name_in_parties",
    "consistent.payee_name_in_parties",
    "coherent.tender_status",
    "coherent.awards_status",
    "coherent.contracts_status",
    "coherent.milestone_status",
    "coherent.dates",
    "coherent.release_date",
    "coherent.milestones_dates",
    "coherent.amendments_dates",
    "coherent.documents_dates",
    "coherent.value_realistic",
    "coherent.period",
    "coherent.procurement_method_vs_number_of_tenderers",
];

// Sync with check descriptions.
export const DATASET_CHECK_STYLES = {
    // donut
    "distribution.main_procurement_category": [],
    "distribution.tender_status": ["active", "complete"],
    "distribution.awards_status": ["active"],
    "distribution.contracts_status": ["active", "terminated"],
    "distribution.milestone_status": ["met"],
    "distribution.tender_procurement_method": ["open"],
};
