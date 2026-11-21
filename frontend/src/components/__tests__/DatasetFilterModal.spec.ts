import { shallowMount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import api from "@/api.js";
import DatasetFilterModal from "@/components/DatasetFilterModal.vue";
import { testI18n } from "@/test/helpers.js";
import type { Dataset } from "@/types.js";

const { go } = vi.hoisted(() => ({ go: vi.fn() }));

vi.mock("vue-router", () => ({ useRouter: () => ({ go }) }));
vi.mock("@/api.js", () => ({ default: { post: vi.fn(), postJSON: vi.fn() } }));

const apiPost = vi.mocked(api.post);
const apiPostJSON = vi.mocked(api.postJSON);

const dataset = {
  id: 7,
  name: "dataset_7",
  meta: {
    collection_metadata: { published_from: "2020-01-01T00:00:00Z", published_to: "2020-12-31T00:00:00Z" },
    compiled_releases: { total_unique_ocids: 42 },
  },
} as unknown as Dataset;

function mountModal() {
  return shallowMount(DatasetFilterModal, {
    props: { dataset },
    global: { plugins: [testI18n()] },
  });
}

beforeEach(() => {
  vi.useFakeTimers();
  go.mockClear();
  apiPost.mockReset();
  apiPostJSON.mockReset();
  apiPostJSON.mockResolvedValue({ ok: true, data: { items: 3 } });
});

afterEach(() => {
  vi.useRealTimers();
});

describe("counting the matches", () => {
  it("counts on opening, and again after the reader pauses typing", async () => {
    const wrapper = mountModal();
    await vi.advanceTimersByTimeAsync(0);

    expect(apiPostJSON).toHaveBeenCalledTimes(1);

    await wrapper.findAll("input.regex_input")[0].setValue(" acme ");
    await vi.advanceTimersByTimeAsync(399);
    expect(apiPostJSON).toHaveBeenCalledTimes(1);

    await vi.advanceTimersByTimeAsync(1);
    expect(apiPostJSON).toHaveBeenCalledTimes(2);
    expect(apiPostJSON).toHaveBeenLastCalledWith(
      "/api/dataset-filter-items/",
      // The default dates match the collection's bounds, so only the trimmed pattern narrows it.
      { dataset_id_original: 7, filter_message: { buyer_regex: "acme" } },
      expect.any(AbortSignal),
    );
  });

  it("disables the submission of a filter that matches nothing", async () => {
    apiPostJSON.mockResolvedValue({ ok: true, data: { items: 0 } });
    const wrapper = mountModal();
    await vi.advanceTimersByTimeAsync(0);

    expect(wrapper.find(".submit_button").attributes("disabled")).toBeDefined();
  });

  it("disables the submission of a filter that matches the whole dataset", async () => {
    apiPostJSON.mockResolvedValue({ ok: true, data: { items: 42 } });
    const wrapper = mountModal();
    await vi.advanceTimersByTimeAsync(0);

    expect(wrapper.find(".submit_button").attributes("disabled")).toBeDefined();
  });
});

describe("submitting the filter", () => {
  it("posts the filter, then closes and reloads for the new dataset", async () => {
    apiPost.mockResolvedValue({ ok: true } as Response);
    const wrapper = mountModal();
    await vi.advanceTimersByTimeAsync(0);

    await wrapper.findAll("input.regex_input")[1].setValue("ministry");
    await vi.advanceTimersByTimeAsync(400);
    await wrapper.find(".submit_button").trigger("click");
    await vi.advanceTimersByTimeAsync(0);

    expect(apiPost).toHaveBeenCalledExactlyOnceWith("/api/datasets/7/filter/", {
      procuring_entity_regex: "ministry",
    });
    expect(wrapper.find("b-alert-stub[variant='success']").exists()).toBe(true);
    expect(wrapper.emitted("close")).toBeUndefined();

    // The success message stays readable for a moment before the reload.
    await vi.advanceTimersByTimeAsync(2000);
    expect(wrapper.emitted("close")).toHaveLength(1);
    expect(go).toHaveBeenCalledWith(0);
  });

  it("restores the form when the submission fails, to try again", async () => {
    apiPost.mockResolvedValue({ ok: false, status: 500, statusText: "Server Error" } as Response);
    const wrapper = mountModal();
    await vi.advanceTimersByTimeAsync(0);

    await wrapper.find(".submit_button").trigger("click");
    await vi.advanceTimersByTimeAsync(0);

    expect(wrapper.find("b-alert-stub[variant='danger']").exists()).toBe(true);
    expect(wrapper.find("form").exists()).toBe(true);
    expect(wrapper.emitted("close")).toBeUndefined();
    expect(go).not.toHaveBeenCalled();
  });
});
