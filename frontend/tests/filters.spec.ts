import { describe, expect, it } from "vitest";
import {
  DATASET_LEVEL_FILTERS,
  FIELD_LEVEL_FILTERS,
  RESOURCE_LEVEL_FILTERS,
  TIME_VARIANCE_LEVEL_FILTERS,
} from "@/filters.js";
import type { DatasetLevelCheck, FieldLevelCheck, ResourceLevelCheck, TimeVarianceLevelCheck } from "@/types.js";

/** Apply each filter to the items, naming the ones it keeps. */
function kept<T extends { name: string }>(filters: ((item: T) => boolean)[], items: T[]) {
  return filters.map((filter) => items.filter(filter).map((item) => item.name));
}

describe("FIELD_LEVEL_FILTERS", () => {
  const check = (name: string, coverage: [number, number], quality: [number, number]) =>
    ({
      name,
      coverage: { passed_count: coverage[0], failed_count: coverage[1] },
      quality: { passed_count: quality[0], failed_count: quality[1] },
    }) as FieldLevelCheck & { name: string };

  it("selects all, then each kind of failure, then the checks that only passed", () => {
    const items = [
      check("clean", [5, 0], [5, 0]),
      check("coverageFailed", [5, 2], [5, 0]),
      check("qualityFailed", [5, 0], [5, 2]),
      check("bothFailed", [5, 1], [5, 1]),
      // A check that was never applied has nothing to pass, so "passed only" excludes it.
      check("inapplicable", [0, 0], [0, 0]),
    ];

    expect(kept(FIELD_LEVEL_FILTERS, items)).toEqual([
      ["clean", "coverageFailed", "qualityFailed", "bothFailed", "inapplicable"],
      ["coverageFailed", "bothFailed"],
      ["qualityFailed", "bothFailed"],
      ["clean"],
    ]);
  });
});

describe("DATASET_LEVEL_FILTERS", () => {
  it("distinguishes a check that could not run from one that failed", () => {
    const items = [
      { name: "passed", result: true },
      { name: "failed", result: false },
      { name: "notApplicable", result: null },
    ] as (DatasetLevelCheck & { name: string })[];

    expect(kept(DATASET_LEVEL_FILTERS, items)).toEqual([
      ["passed", "failed", "notApplicable"],
      ["failed"],
      ["passed"],
      ["passed", "failed"],
    ]);
  });
});

describe("RESOURCE_LEVEL_FILTERS", () => {
  it("excludes an inapplicable check from passed and calculated alike", () => {
    const items = [
      { name: "passed", passed_count: 5, failed_count: 0 },
      { name: "failed", passed_count: 3, failed_count: 2 },
      { name: "allFailed", passed_count: 0, failed_count: 4 },
      { name: "inapplicable", passed_count: 0, failed_count: 0 },
    ] as (ResourceLevelCheck & { name: string })[];

    expect(kept(RESOURCE_LEVEL_FILTERS, items)).toEqual([
      ["passed", "failed", "allFailed", "inapplicable"],
      ["failed", "allFailed"],
      ["passed"],
      ["passed", "failed", "allFailed"],
    ]);
  });
});

describe("TIME_VARIANCE_LEVEL_FILTERS", () => {
  it("counts a check as failed only when a result failed, not when it is absent", () => {
    const items = [
      { name: "bothPassed", coverage_result: true, check_result: true },
      { name: "checkFailed", coverage_result: true, check_result: false },
      { name: "coverageFailed", coverage_result: false, check_result: true },
      // No pairs were found, so the coverage failed and the check itself has no result.
      { name: "noPairs", coverage_result: false, check_result: null },
      // The check applied to no compiled release, so the card reports insufficient data.
      { name: "notApplicable", coverage_result: null, check_result: null },
    ] as (TimeVarianceLevelCheck & { name: string })[];

    expect(kept(TIME_VARIANCE_LEVEL_FILTERS, items)).toEqual([
      ["bothPassed", "checkFailed", "coverageFailed", "noPairs", "notApplicable"],
      ["checkFailed", "coverageFailed", "noPairs"],
      ["bothPassed"],
    ]);
  });
});
