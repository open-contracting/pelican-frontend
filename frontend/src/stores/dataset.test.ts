import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";
import api from "@/api.js";
import { useDatasetStore } from "@/stores/dataset.js";
import { useUiStore } from "@/stores/ui.js";
import type { DataItem, Dataset, ResourceLevelCheck } from "@/types.js";

vi.mock("@/api.js", () => ({ default: { get: vi.fn() } }));

const apiGet = vi.mocked(api.get);

function dataset(id: number): Dataset {
  return { id, name: `dataset_${id}` } as Dataset;
}

function counts(passed: number, total: number) {
  return { passed_count: passed, failed_count: total - passed, total_count: total, checks: {} };
}

function resourceCheck(name: string, overrides: Partial<ResourceLevelCheck> = {}): ResourceLevelCheck {
  return {
    name,
    total_count: 1,
    passed_count: 1,
    failed_count: 0,
    undefined_count: 0,
    individual_application_count: 1,
    individual_passed_count: 1,
    individual_failed_count: 0,
    examples_filled: false,
    passed_examples: [],
    failed_examples: [],
    undefined_examples: [],
    ...overrides,
  };
}

/** Answer each GET by its exact URL, so a test declares every request it expects. */
function mockRoutes(routes: Record<string, unknown>) {
  apiGet.mockImplementation(async (url: string) => {
    if (!(url in routes)) {
      throw new Error(`Unmocked URL ${url}`);
    }
    return routes[url];
  });
}

beforeEach(() => {
  setActivePinia(createPinia());
  apiGet.mockReset();
});

describe("loadDataset", () => {
  async function loadReports(fieldLevelReport: unknown) {
    mockRoutes({
      "/api/datasets/7": dataset(7),
      "/api/datasets/7/field_level_report/": fieldLevelReport,
      "/api/datasets/7/compiled_release_level_report/": { "coverage.ocid": resourceCheck("coverage.ocid") },
      "/api/datasets/7/dataset_level_report/": { "distribution.buyer": { result: true, value: 1, meta: {} } },
      "/api/datasets/7/time_based_report/": { phase_stable: { result: null, value: null, meta: {} } },
    });

    const store = useDatasetStore();
    await store.loadDataset(7);
    return store;
  }

  it("keys each report's checks by name or path", async () => {
    const store = await loadReports({
      ocid: { coverage: counts(1, 1), quality: counts(1, 1), examples_filled: false, processing_order: 1 },
    });

    expect(store.dataset).toEqual(dataset(7));
    expect(store.datasetId).toBe(7);
    expect(store.fieldLevelStats?.map((item) => item.path)).toEqual(["ocid"]);
    expect(store.resourceLevelStats?.map((item) => item.name)).toEqual(["coverage.ocid"]);
    expect(store.datasetLevelStats?.map((item) => item.name)).toEqual(["distribution.buyer"]);
    expect(store.timeVarianceLevelStats?.map((item) => item.name)).toEqual(["phase_stable"]);
  });

  it("derives a field check's ratios, as 0 when the check was never applied", async () => {
    const store = await loadReports({
      ocid: { coverage: counts(2, 4), quality: counts(0, 0), examples_filled: false, processing_order: 1 },
    });

    const [ocid] = store.fieldLevelStats ?? [];
    expect(ocid.coverageOkRatio).toBe(0.5);
    expect(ocid.coverageFailedRatio).toBe(0.5);
    expect(ocid.qualityOkRatio).toBe(0);
    expect(ocid.qualityFailedRatio).toBe(0);
  });

  it("restores the field check page's defaults", async () => {
    const ui = useUiStore();
    ui.fieldCheckSearch = "tender";
    ui.fieldCheckLayout = "tree";

    await loadReports({});

    expect(ui.fieldCheckSearch).toBeNull();
    expect(ui.fieldCheckLayout).toBe("table");
  });
});

describe("resourceLevelStatsBySection", () => {
  it("matches checks by name prefix, including a section that extends the prefix", () => {
    const store = useDatasetStore();
    store.resourceLevelStats = [
      resourceCheck("coverage.ocid"),
      resourceCheck("coverage_deep.id"),
      resourceCheck("consistent.number"),
    ];

    const names = store.resourceLevelStatsBySection("coverage").map((item) => item.name);
    expect(names).toEqual(["coverage.ocid", "coverage_deep.id"]);
  });

  it("returns an empty list before the report loads", () => {
    expect(useDatasetStore().resourceLevelStatsBySection("coverage")).toEqual([]);
  });
});

describe("loadResourceLevelCheckDetail", () => {
  it("merges the examples into the check, and fetches them only once", async () => {
    const example = {
      meta: { ocid: "ocds-213czf-1", item_id: 1 },
      result: { result: true, meta: null, pass_count: 1, application_count: 1, version: 1 },
    };
    const store = useDatasetStore();
    store.dataset = dataset(7);
    store.resourceLevelStats = [resourceCheck("coverage.ocid")];
    mockRoutes({
      "/api/datasets/7/compiled_release_level/coverage.ocid/": resourceCheck("coverage.ocid", {
        passed_examples: [example],
      }),
    });

    await store.loadResourceLevelCheckDetail("coverage.ocid");

    const check = store.resourceLevelCheckByName("coverage.ocid");
    expect(check?.examples_filled).toBe(true);
    expect(check?.passed_examples).toEqual([example]);
    expect(apiGet).toHaveBeenCalledTimes(1);

    await store.loadResourceLevelCheckDetail("coverage.ocid");
    expect(apiGet).toHaveBeenCalledTimes(1);
  });

  it("fetches nothing for an unknown check", async () => {
    const store = useDatasetStore();
    store.dataset = dataset(7);
    store.resourceLevelStats = [resourceCheck("coverage.ocid")];

    await store.loadResourceLevelCheckDetail("nonexistent");

    expect(apiGet).not.toHaveBeenCalled();
  });
});

describe("data items", () => {
  it("loads an item once, then serves it from memory", async () => {
    const store = useDatasetStore();
    mockRoutes({ "/api/data_items/5/": { id: 5, data: { a: 1 } } });

    await store.loadDataItem(5);
    await store.loadDataItem(5);

    expect(apiGet).toHaveBeenCalledTimes(1);
    expect(store.dataItemById(5)).toEqual({ id: 5, data: { a: 1 } });
  });

  it("pretty-prints an item's JSON and counts its lines", () => {
    const store = useDatasetStore();
    store.dataItems = [{ id: 5, data: { a: 1 } } as DataItem];

    expect(store.dataItemJSON(5)).toBe('{\n  "a": 1\n}');
    expect(store.dataItemJSONLines(5)).toBe(3);
  });

  it("returns null for an unknown item", () => {
    const store = useDatasetStore();

    expect(store.dataItemJSON(5)).toBeNull();
    expect(store.dataItemJSONLines(5)).toBeNull();
  });
});
