import type { DatasetLevelCheck, FieldLevelCheck, ResourceLevelCheck, TimeVarianceLevelCheck } from "@/types.js";

// Each list is in the order of the filter dropdown's names, whose first entry is always "All".

export const FIELD_LEVEL_FILTERS: ((item: FieldLevelCheck) => boolean)[] = [
  () => true,
  (item) => item.coverage.failed_count > 0,
  (item) => item.quality.failed_count > 0,
  (item) => item.coverage.failed_count === 0 && item.quality.failed_count === 0 && item.coverage.passed_count > 0,
];

export const DATASET_LEVEL_FILTERS: ((item: DatasetLevelCheck) => boolean)[] = [
  () => true,
  (item) => item.result === false,
  (item) => item.result === true,
  (item) => item.result != null,
];

export const RESOURCE_LEVEL_FILTERS: ((item: ResourceLevelCheck) => boolean)[] = [
  () => true,
  (item) => item.failed_count > 0,
  (item) => item.failed_count === 0 && item.passed_count > 0,
  (item) => item.passed_count > 0 || item.failed_count > 0,
];

export const TIME_VARIANCE_LEVEL_FILTERS: ((item: TimeVarianceLevelCheck) => boolean)[] = [
  () => true,
  // A check that applied to nothing has no result, and is no more failed than it is passed.
  (item) => item.coverage_result === false || item.check_result === false,
  (item) => item.coverage_result === true && item.check_result === true,
];
