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

// Sync with the example keys in the dataset-level and time-based checks.
export const EXAMPLE_KEYS = new Set(["examples", "failed_examples", "passed_examples"]);

// Sync with the catalogs in src/messages. Each name is in its own language, and is never translated.
export const LOCALES: Record<string, string> = { en: "English", es: "Español" };

/** A pair of thresholds, between which a share passes. */
type Ticks = [number, number];

// Sync with CHECK_TYPES in dataset.py, and with the check descriptions.
/**
 * How to chart a dataset-level check, and what the chart needs: a type whose chart plots thresholds cannot be
 * declared without them.
 */
export type DatasetCheck = {
  /** Whether the check reports a distribution without passing or failing. */
  reportOnly?: true;
} & (
  | { type: "code"; ticks?: Ticks; styles?: string[] }
  | { type: "percentile"; ticks: Ticks }
  | { type: "single_value_share"; ticks: Ticks }
  | { type: "numeric" | "top3" | "biggest_share" }
);

export const DATASET_CHECKS: Record<string, DatasetCheck | undefined> = {
  // code
  "distribution.main_procurement_category": { type: "code", ticks: [0, 0.95], styles: [] },
  "distribution.tender_status": { type: "code", ticks: [0.001, 0.99], styles: ["active", "complete"] },
  "distribution.tender_procurement_method": { type: "code", ticks: [0.001, 0.99], styles: ["open"] },
  "distribution.tender_award_criteria": { type: "code", reportOnly: true },
  "distribution.tender_submission_method": { type: "code", reportOnly: true },
  "distribution.awards_status": { type: "code", ticks: [0.001, 0.99], styles: ["active"] },
  "distribution.contracts_status": { type: "code", ticks: [0.001, 0.99], styles: ["active", "terminated"] },
  "distribution.milestone_status": { type: "code", ticks: [0.001, 0.99], styles: ["met"] },
  "distribution.milestone_type": { type: "code", reportOnly: true },
  "distribution.document_document_type": { type: "code", reportOnly: true },
  "distribution.value_currency": { type: "code", reportOnly: true },
  "distribution.related_process_relation": { type: "code", reportOnly: true },
  // percentile
  "distribution.tender_value": { type: "percentile", ticks: [0, 0.5] },
  "distribution.contracts_value": { type: "percentile", ticks: [0, 0.5] },
  "distribution.awards_value": { type: "percentile", ticks: [0, 0.5] },
  // numeric
  "misc.url_availability": { type: "numeric" },
  "unique.tender_id": { type: "numeric" },
  "consistent.related_process_title": { type: "numeric" },
  "reference.related_process_identifier": { type: "numeric" },
  // top3
  "distribution.tender_value_repetition": { type: "top3" },
  "distribution.awards_value_repetition": { type: "top3" },
  "distribution.contracts_value_repetition": { type: "top3" },
  // biggest_share
  "distribution.buyer_repetition": { type: "biggest_share" },
  // single_value_share
  "distribution.buyer": { type: "single_value_share", ticks: [0, 0.5] },
};

// Key order determines the order of the sections in the dataset-level view.
export const DATASET_CHECK_SECTIONS: Record<string, string[] | undefined> = {
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
