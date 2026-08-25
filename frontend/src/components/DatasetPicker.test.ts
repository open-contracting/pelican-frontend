import { flushPromises, shallowMount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";
import api from "@/api.js";
import DatasetPicker from "@/components/DatasetPicker.vue";
import DatasetPickerRow from "@/components/DatasetPickerRow.vue";
import { useUiStore } from "@/stores/ui.js";
import { testI18n } from "@/test/helpers.js";
import type { Dataset, Sorting } from "@/types.js";

vi.mock("@/api.js", () => ({ default: { get: vi.fn() } }));

const apiGet = vi.mocked(api.get);

interface DatasetOptions {
  created?: string | null;
  ocids?: number;
  collectionId?: number;
  phase?: string;
  state?: string;
  parentId?: number;
  ancestorId?: number;
}

function dataset(id: number, name: string, options: DatasetOptions = {}): Dataset {
  const { created = null, ocids, collectionId, phase = "CHECKED", state = "OK", parentId, ancestorId } = options;
  return {
    id,
    name,
    created,
    modified: null,
    phase,
    state,
    parent_id: parentId ?? null,
    parent_name: null,
    ancestor_id: ancestorId ?? null,
    filter_message: null,
    meta: {
      compiled_releases: ocids === undefined ? {} : { total_unique_ocids: ocids },
      kingfisher_metadata: collectionId === undefined ? {} : { collection_id: collectionId },
    },
  } as Dataset;
}

let pinia: ReturnType<typeof createPinia>;

beforeEach(() => {
  pinia = createPinia();
  setActivePinia(pinia);
  apiGet.mockReset();
});

async function rowNames(datasets: Dataset[], sorting: Sorting | null = null) {
  useUiStore().datasetSorting = sorting;
  apiGet.mockResolvedValueOnce(datasets);

  const wrapper = shallowMount(DatasetPicker, { global: { plugins: [pinia, testI18n()] } });
  await flushPromises();

  return wrapper.findAllComponents(DatasetPickerRow).map((row) => (row.props("dataset") as Dataset).name);
}

describe("sorting", () => {
  it("sorts by creation date, newest first, by default, with undated datasets last", async () => {
    const names = await rowNames([
      dataset(1, "older", { created: "2024-01-02T00:00:00Z" }),
      dataset(2, "undated"),
      dataset(3, "newer", { created: "2024-03-01T00:00:00Z" }),
    ]);

    expect(names).toEqual(["newer", "older", "undated"]);
  });

  it("sorts by size, with a dataset of 0 OCIDs tied with those of unknown size", async () => {
    const names = await rowNames(
      [
        dataset(1, "large", { ocids: 5 }),
        dataset(2, "empty", { ocids: 0 }),
        dataset(3, "unknown"),
        dataset(4, "small", { ocids: 2 }),
      ],
      { by: "size", asc: true },
    );

    expect(names).toEqual(["empty", "unknown", "small", "large"]);
  });

  it("sorts by Kingfisher collection ID", async () => {
    const names = await rowNames(
      [dataset(1, "second", { collectionId: 20 }), dataset(2, "first", { collectionId: 10 }), dataset(3, "unknown")],
      { by: "collection_id", asc: true },
    );

    expect(names).toEqual(["unknown", "first", "second"]);
  });

  it("sorts by phase, breaking ties by state and then ID", async () => {
    const names = await rowNames(
      [
        dataset(9, "checked-late", { phase: "CHECKED", state: "OK" }),
        dataset(4, "checked-early", { phase: "CHECKED", state: "OK" }),
        dataset(2, "checked-running", { phase: "CHECKED", state: "IN_PROGRESS" }),
        dataset(3, "importing", { phase: "CONTRACTING_PROCESS", state: "OK" }),
      ],
      { by: "phase", asc: true },
    );

    expect(names).toEqual(["importing", "checked-running", "checked-early", "checked-late"]);
  });

  it("sorts by name in either direction", async () => {
    const datasets = [dataset(1, "b"), dataset(2, "a"), dataset(3, "c")];

    expect(await rowNames(datasets, { by: "name", asc: true })).toEqual(["a", "b", "c"]);
    expect(await rowNames(datasets, { by: "name", asc: false })).toEqual(["c", "b", "a"]);
  });
});

describe("the datasets tree", () => {
  it("lists a filtered dataset under its parent, not as its own row", async () => {
    useUiStore().datasetSorting = { by: "name", asc: true };
    apiGet.mockResolvedValueOnce([dataset(1, "parent"), dataset(2, "filtered", { parentId: 1 })]);

    const wrapper = shallowMount(DatasetPicker, { global: { plugins: [pinia, testI18n()] } });
    await flushPromises();

    const rows = wrapper.findAllComponents(DatasetPickerRow);
    expect(rows).toHaveLength(1);
    const parent = rows[0].props("dataset");
    expect(parent.name).toBe("parent");
    expect(parent.filtered_children.map((child: Dataset) => child.name)).toEqual(["filtered"]);
  });

  it("names the dataset that a time-based comparison follows", async () => {
    useUiStore().datasetSorting = { by: "name", asc: true };
    apiGet.mockResolvedValueOnce([dataset(3, "previous"), dataset(4, "current", { ancestorId: 3 })]);

    const wrapper = shallowMount(DatasetPicker, { global: { plugins: [pinia, testI18n()] } });
    await flushPromises();

    const current = wrapper.findAllComponents(DatasetPickerRow)[0].props("dataset");
    expect(current.name).toBe("current");
    expect(current.ancestor_name).toBe("previous");
  });
});

describe("searching", () => {
  it("shows the datasets whose names contain the search, case-insensitively", async () => {
    useUiStore().datasetSearch = "MEXICO";

    const names = await rowNames([dataset(1, "mexico_2024"), dataset(2, "chile_2024")], { by: "name", asc: true });

    expect(names).toEqual(["mexico_2024"]);
  });
});
