import type { components, operations } from "@/schema.js";

type Schemas = components["schemas"];

export type DataItem = Schemas["DataItem"];
export type Dataset = Schemas["Dataset"];
export type DatasetLevelReport = Schemas["DatasetLevelReport"];
export type DistinctValue = Schemas["DistinctValue"];
type ExampleMeta = Schemas["ExampleMeta"];
export type FieldLevelCheckDetail = Schemas["FieldLevelCheckDetail"];
export type FieldLevelCounts = Schemas["FieldLevelCounts"];
export type FieldLevelExample = Schemas["FieldLevelExample"];
export type FieldLevelReport = Schemas["FieldLevelReport"];
export type FilterDataset = Schemas["FilterDataset"];
/** The number of data items that a filter matches. */
export type FilterItemsCount =
  operations["dataset_filter_items_create"]["responses"][200]["content"]["application/json"];
export type GenerateReport = Schemas["GenerateReport"];
export type GenerateReportResponse = Schemas["GenerateReportResponse"];
export type ResourceLevelCheck = Schemas["ResourceLevelCheck"];
export type ResourceLevelCheckDetail = Schemas["ResourceLevelCheckDetail"];
export type ResourceLevelReport = Schemas["ResourceLevelReport"];
export type Settings = Schemas["Settings"];
export type TimeVarianceLevelReport = Schemas["TimeVarianceLevelReport"];

/** A dataset in the picker's tree: the datasets filtered from it, and the name of the dataset it follows. */
export type DatasetNode = Dataset & {
  filtered_children: DatasetNode[];
  ancestor_name?: string;
};

// The dataset-level and time-based reports key each check by name, and the store moves the key into the check.

export type DatasetLevelCheck = Omit<Schemas["DatasetLevelCheck"], "meta"> & {
  name: string;
  meta: DatasetLevelMeta;
};

export type TimeVarianceLevelCheck = Schemas["TimeVarianceLevelCheck"] & {
  name: string;
};

// The field-level report keys each check by field path, and the store derives the ratios the tables display.
export type FieldLevelCheck = Schemas["FieldLevelCheck"] & {
  path: string;
  coverageOkRatio: number;
  coverageFailedRatio: number;
  qualityOkRatio: number;
  qualityFailedRatio: number;
};

// A dataset-level check's meta is documented as free-form, because its properties vary by check. The frontend
// reads one shape per check type, and renders the rest verbatim. DATASET_CHECKS maps a check to its type.

/** The properties common to every check. */
export interface DatasetLevelMeta {
  /** The reason the check could not be performed. */
  reason?: string | null;
}

export interface CodeMeta extends DatasetLevelMeta {
  shares: Record<string, CodeShare>;
}

interface CodeShare {
  share: number;
  count: number;
  examples: ExampleMeta[];
}

export interface PercentileMeta extends DatasetLevelMeta {
  shares: Record<string, number>;
  counts: Record<string, number>;
  examples: Record<string, ExampleMeta[]>;
}

export interface NumericMeta extends DatasetLevelMeta {
  total_passed: number;
  total_processed: number;
  passed_examples: ExampleMeta[];
  failed_examples: ExampleMeta[];
}

export interface Top3Meta extends DatasetLevelMeta {
  most_frequent: MostFrequentValue[];
}

interface MostFrequentValue {
  value_str: string;
  share: number;
  count: number;
  examples: ExampleMeta[];
}

export interface BiggestShareMeta extends DatasetLevelMeta {
  ocid_share: number;
  ocid_count: number;
  total_ocid_count: number;
  /** The check's own properties, rendered as a definition list. */
  specifics?: Record<string, unknown>;
  examples: ExampleMeta[];
}

export interface SingleValueShareMeta extends DatasetLevelMeta {
  counts: Record<string, { total_unique_count: number }>;
  total_unique_count: number;
  examples: ExampleMeta[];
}

/** A node in the field-level check tree: the check at this path, if any, and a child node per following segment. */
export interface FieldCheckTreeNode {
  check?: FieldLevelCheck;
  children: Map<string, FieldCheckTreeNode>;
}

/** A JSON value, as VueJsonPretty renders it. */
export type JSONData = string | number | boolean | unknown[] | Record<string, unknown> | null;

/** A table's sort order: the column, and its direction. */
export interface Sorting {
  by: string;
  asc: boolean;
}

/** A group of examples, as ExampleBoxes renders it. */
export interface ExampleSection {
  header: string;
  examples: ExampleMeta[];
  id?: string;
  prefix?: string;
  group?: "coverage" | "quality";
}
