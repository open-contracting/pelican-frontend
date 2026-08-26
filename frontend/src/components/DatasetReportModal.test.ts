import { flushPromises, shallowMount } from "@vue/test-utils";
import { BFormInput, BFormRadio } from "bootstrap-vue-next";
import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";
import api from "@/api.js";
import DatasetReportModal from "@/components/DatasetReportModal.vue";
import GoogleDocsLink from "@/components/GoogleDocsLink.vue";
import RetryOrCloseButtons from "@/components/RetryOrCloseButtons.vue";
import { useSettingsStore } from "@/stores/settings.js";
import { testI18n } from "@/test/helpers.js";
import type { Dataset } from "@/types.js";

vi.mock("@/api.js", () => ({ default: { patch: vi.fn(), postJSON: vi.fn() } }));

const apiPostJSON = vi.mocked(api.postJSON);

const dataset = { id: 7, name: "dataset_7" } as Dataset;

function mountModal() {
  const pinia = createPinia();
  setActivePinia(pinia);
  useSettingsStore().settings = {
    template: { en: "TEMPLATE_EN", es: "TEMPLATE_ES" },
    folder: "FOLDER",
    user: "exporter@example.com",
    username: "reader",
    language: "en",
  };

  return shallowMount(DatasetReportModal, {
    props: { dataset },
    // The radios render inside BRow/BCol slots, which stubs would swallow.
    global: { plugins: [pinia, testI18n()], stubs: { BRow: false, BCol: false } },
  });
}

async function submit(wrapper: ReturnType<typeof mountModal>) {
  await wrapper.find(".submit_button").trigger("click");
  await flushPromises();
}

beforeEach(() => {
  apiPostJSON.mockReset();
});

describe("submitting an export", () => {
  it("posts the account's defaults, and links the created report", async () => {
    apiPostJSON.mockResolvedValue({ ok: true, data: { status: "ok", data: { file_id: "FILE" }, failed_tags: [] } });
    const wrapper = mountModal();

    await submit(wrapper);

    expect(apiPostJSON).toHaveBeenCalledExactlyOnceWith("/api/generate-report", {
      dataset_id: 7,
      document_id: "TEMPLATE_EN",
      folder_id: "FOLDER",
      language: "en",
    });
    expect(wrapper.find("b-alert-stub[variant='success']").exists()).toBe(true);
    expect(wrapper.findComponent(GoogleDocsLink).props("documentId")).toBe("FILE");
  });

  it("switches the default template with the report's language, but keeps a custom one", async () => {
    apiPostJSON.mockResolvedValue({ ok: true, data: { status: "ok", data: { file_id: "FILE" }, failed_tags: [] } });
    const wrapper = mountModal();

    wrapper.findAllComponents(BFormRadio)[1].vm.$emit("update:modelValue", "es");
    await submit(wrapper);
    expect(apiPostJSON.mock.calls[0][1]).toMatchObject({ document_id: "TEMPLATE_ES", language: "es" });

    const retryWrapper = mountModal();
    retryWrapper.findAllComponents(BFormInput)[0].vm.$emit("update:modelValue", "CUSTOM");
    retryWrapper.findAllComponents(BFormRadio)[1].vm.$emit("update:modelValue", "es");
    await submit(retryWrapper);
    expect(apiPostJSON.mock.calls[1][1]).toMatchObject({ document_id: "CUSTOM", language: "es" });
  });

  it("reports a server error, and retries on demand", async () => {
    apiPostJSON.mockResolvedValue({ ok: false, status: 500, statusText: "Server Error" });
    const wrapper = mountModal();

    await submit(wrapper);
    expect(wrapper.find("b-alert-stub[variant='danger']").exists()).toBe(true);

    wrapper.findComponent(RetryOrCloseButtons).vm.$emit("retry");
    await flushPromises();
    expect(apiPostJSON).toHaveBeenCalledTimes(2);
  });

  it("lists the tags that an exported report could not compute", async () => {
    apiPostJSON.mockResolvedValue({
      ok: true,
      data: { status: "ok", data: { file_id: "FILE" }, failed_tags: ["{% tag1 %}", "{% tag2 %}"] },
    });
    const wrapper = mountModal();

    await submit(wrapper);

    expect(wrapper.find("b-alert-stub[variant='warning']").exists()).toBe(true);
    expect(wrapper.findAll("li").map((item) => item.text())).toEqual(["{% tag1 %}", "{% tag2 %}"]);
  });
});

describe("the file ID formatter", () => {
  it("extracts the ID from a document or folder URL, and keeps a bare ID", () => {
    const wrapper = mountModal();
    const formatter = wrapper.findAllComponents(BFormInput)[0].props("formatter") as (value: string) => string;

    expect(formatter("https://docs.google.com/document/d/DOC_ID/edit")).toBe("DOC_ID");
    expect(formatter("https://drive.google.com/drive/folders/FOLDER_ID")).toBe("FOLDER_ID");
    expect(formatter("BARE_ID")).toBe("BARE_ID");
  });

  it("drops a copied link's query string and fragment", () => {
    const wrapper = mountModal();
    const formatter = wrapper.findAllComponents(BFormInput)[0].props("formatter") as (value: string) => string;

    expect(formatter("https://drive.google.com/drive/folders/FOLDER_ID?usp=sharing")).toBe("FOLDER_ID");
    expect(formatter("https://docs.google.com/document/d/DOC_ID?usp=drive_link")).toBe("DOC_ID");
    expect(formatter("https://docs.google.com/document/d/DOC_ID#heading=h.abc")).toBe("DOC_ID");
    expect(formatter("https://docs.google.com/document/d/DOC_ID/edit#heading=h.abc")).toBe("DOC_ID");
  });
});
