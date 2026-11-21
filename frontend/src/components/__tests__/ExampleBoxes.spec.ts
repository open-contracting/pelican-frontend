import { shallowMount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import { testI18n } from "@/test/helpers.js";
import type { ExampleSection } from "@/types.js";

const { download, copyToClipboard } = vi.hoisted(() => ({ download: vi.fn(), copyToClipboard: vi.fn() }));

vi.mock("@/composables/useDataItem.js", () => ({ useDataItem: () => ({ download, copyToClipboard }) }));

function section(count: number): ExampleSection {
  return {
    header: "coverage.ocid",
    group: "coverage",
    examples: Array.from({ length: count }, (_, index) => ({ ocid: `ocds-${index}`, item_id: 100 + index })),
  };
}

function mountBoxes(sections: ExampleSection[]) {
  return shallowMount(ExampleBoxes, {
    props: { exampleSections: sections },
    global: { plugins: [testI18n()], stubs: { FontAwesomeIcon: true } },
  });
}

beforeEach(() => {
  download.mockClear();
  copyToClipboard.mockClear();
});

describe("ExampleBoxes", () => {
  it("shows the first five examples, and the rest on demand", async () => {
    const wrapper = mountBoxes([section(7)]);

    expect(wrapper.findAll(".check_name")).toHaveLength(5);

    await wrapper.find(".moreLess").trigger("click");
    expect(wrapper.findAll(".check_name")).toHaveLength(7);

    await wrapper.find(".moreLess").trigger("click");
    expect(wrapper.findAll(".check_name")).toHaveLength(5);
  });

  it("shows every example of a short section, with nothing to expand", () => {
    const wrapper = mountBoxes([section(3)]);

    expect(wrapper.findAll(".check_name")).toHaveLength(3);
    expect(wrapper.find(".moreLess").exists()).toBe(false);
  });

  it("emits a preview of the clicked example, and marks it as selected", async () => {
    const wrapper = mountBoxes([section(2)]);

    const buttons = wrapper.findAll("button[title='Preview']");
    await buttons[1].trigger("click");

    expect(wrapper.emitted("preview")).toEqual([[101, "coverage"]]);
    // The selected example's preview button gives way to a static icon.
    expect(wrapper.findAll("button[title='Preview']")).toHaveLength(1);
  });

  it("downloads and copies the clicked example", async () => {
    const wrapper = mountBoxes([section(2)]);

    await wrapper.findAll("button[title='Download']")[1].trigger("click");
    await wrapper.findAll("button[title='Copy to clipboard']")[0].trigger("click");

    expect(download).toHaveBeenCalledExactlyOnceWith(101);
    expect(copyToClipboard).toHaveBeenCalledExactlyOnceWith(100);
  });
});
