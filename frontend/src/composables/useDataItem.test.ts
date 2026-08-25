import { flushPromises } from "@vue/test-utils";
import { createPinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";
import api from "@/api.js";
import { useDataItem } from "@/composables/useDataItem.js";
import { mountComposable, testI18n } from "@/test/helpers.js";
import type { DataItem } from "@/types.js";

const { toast } = vi.hoisted(() => ({ toast: vi.fn() }));

vi.mock("bootstrap-vue-next", () => ({ useToast: () => ({ create: toast }) }));
vi.mock("@/api.js", () => ({ default: { get: vi.fn() } }));

const apiGet = vi.mocked(api.get);

// The JSON of an array of n numbers spans n + 2 lines: the brackets, and one line per number.
function itemOfLines(id: number, lines: number): DataItem {
  return { id, data: Array(lines - 2).fill(0) };
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

function composable() {
  return mountComposable(() => useDataItem(), [createPinia(), testI18n()]);
}

beforeEach(() => {
  toast.mockReset();
  apiGet.mockReset();
});

describe("previewDataItem", () => {
  it("previews an item below the size limit, remembering which control asked", async () => {
    const item = itemOfLines(1, 2999);
    apiGet.mockResolvedValueOnce(item);
    const { previewDataItem, previewData, loadingPreviewData, selectedKey } = composable();

    previewDataItem(1, "box-1");
    expect(loadingPreviewData.value).toBe(true);
    await flushPromises();

    expect(previewData.value).toEqual(item.data);
    expect(selectedKey.value).toBe("box-1");
    expect(loadingPreviewData.value).toBe(false);
    expect(toast).not.toHaveBeenCalled();
  });

  it("refuses an item at the size limit, explaining why", async () => {
    apiGet.mockResolvedValueOnce(itemOfLines(1, 3000));
    const { previewDataItem, previewData } = composable();

    previewDataItem(1);
    await flushPromises();

    expect(previewData.value).toBeUndefined();
    expect(toast).toHaveBeenCalledWith(
      expect.objectContaining({ variant: "danger", body: expect.stringContaining("cannot be previewed") }),
    );
  });

  it("reports an item that the backend no longer has", async () => {
    apiGet.mockRejectedValueOnce(new Error("404 Not Found"));
    const { previewDataItem, previewData, loadingPreviewData } = composable();

    previewDataItem(1);
    await flushPromises();

    expect(previewData.value).toBeUndefined();
    expect(loadingPreviewData.value).toBe(false);
    expect(toast).toHaveBeenCalledWith(
      expect.objectContaining({ variant: "danger", body: expect.stringContaining("was not found") }),
    );
  });

  it("shows the item of the reader's last click, however the responses are ordered", async () => {
    const first = deferred<DataItem>();
    const second = deferred<DataItem>();
    apiGet.mockImplementation((url: string) => (url.includes("/1/") ? first.promise : second.promise) as never);
    const { previewDataItem, previewData, loadingPreviewData } = composable();

    previewDataItem(1);
    previewDataItem(2);

    second.resolve(itemOfLines(2, 10));
    await flushPromises();
    expect(previewData.value).toEqual(itemOfLines(2, 10).data);
    expect(loadingPreviewData.value).toBe(false);

    first.resolve(itemOfLines(1, 10));
    await flushPromises();
    expect(previewData.value).toEqual(itemOfLines(2, 10).data);
  });
});

describe("copyToClipboard", () => {
  function stubClipboard() {
    // The stub awaits the parts, as browsers do: a rejected data promise must reject the write.
    class FakeClipboardItem {
      parts: Record<string, Promise<Blob>>;
      constructor(parts: Record<string, Promise<Blob>>) {
        this.parts = parts;
      }
    }
    const write = vi.fn(async (items: FakeClipboardItem[]) => {
      await Promise.all(items.flatMap((item) => Object.values(item.parts)));
    });
    vi.stubGlobal("ClipboardItem", FakeClipboardItem);
    Object.defineProperty(navigator, "clipboard", { value: { write }, configurable: true });
    return write;
  }

  it("copies an item below the size limit", async () => {
    const write = stubClipboard();
    apiGet.mockResolvedValueOnce(itemOfLines(1, 2999));
    const { copyToClipboard } = composable();

    await copyToClipboard(1);

    expect(write).toHaveBeenCalledTimes(1);
    expect(toast).toHaveBeenCalledWith(
      expect.objectContaining({ variant: "primary", body: expect.stringContaining("copied to clipboard") }),
    );
  });

  it("refuses an item at the size limit, explaining why", async () => {
    stubClipboard();
    apiGet.mockResolvedValueOnce(itemOfLines(1, 3000));
    const { copyToClipboard } = composable();

    await copyToClipboard(1);

    expect(toast).toHaveBeenCalledWith(
      expect.objectContaining({ variant: "danger", body: expect.stringContaining("cannot be copied") }),
    );
  });

  it("reports an item that the backend no longer has", async () => {
    stubClipboard();
    apiGet.mockRejectedValueOnce(new Error("404 Not Found"));
    const { copyToClipboard } = composable();

    await copyToClipboard(1);

    expect(toast).toHaveBeenCalledWith(
      expect.objectContaining({ variant: "danger", body: expect.stringContaining("was not found") }),
    );
  });
});
