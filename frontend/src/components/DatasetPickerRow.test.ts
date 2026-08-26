import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";
import DatasetPickerRow from "@/components/DatasetPickerRow.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import { testI18n } from "@/test/helpers.js";
import type { DatasetNode } from "@/types.js";

function dataset(phase: string, state: string): DatasetNode {
  return {
    id: 7,
    name: "dataset_7",
    phase,
    state,
    meta: { compiled_releases: { total_unique_ocids: 5 }, kingfisher_metadata: { collection_id: 1 } },
    filtered_children: [],
  } as unknown as DatasetNode;
}

function mountRow(phase: string, state: string) {
  return mount(DatasetPickerRow, {
    props: { dataset: dataset(phase, state) },
    global: {
      plugins: [testI18n()],
      stubs: { FontAwesomeIcon: true, BLink: true, RouterLink: true },
    },
  });
}

describe("the status cell", () => {
  it("names a deleted dataset, whichever state it is in", () => {
    for (const state of ["OK", "IN_PROGRESS"]) {
      const wrapper = mountRow("DELETED", state);

      expect(wrapper.find(".phase_cell").text()).toBe("Deleted");
      expect(wrapper.findComponent(ProgressBar).exists()).toBe(false);
    }
  });

  it("names a checked dataset, without a progress bar", () => {
    const wrapper = mountRow("CHECKED", "OK");

    expect(wrapper.find(".phase_cell").text()).toBe("Checked");
    expect(wrapper.findComponent(ProgressBar).exists()).toBe(false);
  });

  it("charts how far an unfinished dataset has progressed", () => {
    const wrapper = mountRow("DATASET", "IN_PROGRESS");

    expect(wrapper.find(".phase_cell").text()).toBe("Collection");
    expect(wrapper.findComponent(ProgressBar).props("value")).toBe(50);
  });
});
