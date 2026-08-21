import type { ColorVariant } from "bootstrap-vue-next";
import { useToast } from "bootstrap-vue-next";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useDatasetStore } from "@/stores/dataset.js";
import type { JSONData } from "@/types.js";

// Above this, some browsers can crash while rendering the JSON data.
const maxJSONLines = 3000;

class DataItemNotFound extends Error {}
class DataItemTooLarge extends Error {}

export function useDataItem() {
  const datasetStore = useDatasetStore();
  const { t } = useI18n();
  const { create: showToast } = useToast();

  const previewDataItemId = ref<number | null>(null);
  const loadingPreviewData = ref(false);
  const selectedKey = ref<string | null>(null);

  const previewData = computed(() =>
    previewDataItemId.value == null
      ? undefined
      : (datasetStore.dataItemById(previewDataItemId.value)?.data as JSONData | undefined),
  );

  let fileLink: HTMLAnchorElement | undefined;
  let previousFileURL: string | undefined;
  let previewRequest = 0;

  function toast(body: string, variant: ColorVariant) {
    showToast({ body, variant, pos: "middle-center" });
  }

  // `key` identifies the control that requested the preview, for the caller to highlight it.
  function previewDataItem(itemId: number, key: string | null = null) {
    // A later click supersedes this one, whose response is then ignored.
    const request = ++previewRequest;
    loadingPreviewData.value = true;
    datasetStore
      .loadDataItem(itemId)
      .then(() => {
        if (request !== previewRequest) {
          return;
        }
        if ((datasetStore.dataItemJSONLines(itemId) ?? 0) < maxJSONLines) {
          previewDataItemId.value = itemId;
          selectedKey.value = key;
        } else {
          toast(t("preview.cannotDisplay"), "danger");
          previewDataItemId.value = null;
          selectedKey.value = null;
        }
      })
      .catch(() => {
        if (request !== previewRequest) {
          return;
        }
        toast(t("preview.nonExisting"), "danger");
        previewDataItemId.value = null;
        selectedKey.value = null;
      })
      .finally(() => {
        if (request !== previewRequest) {
          return;
        }
        loadingPreviewData.value = false;
      });
  }

  function download(itemId: number) {
    datasetStore
      .loadDataItem(itemId)
      .then(() => {
        const result = datasetStore.dataItemById(itemId);

        if (result == null) {
          throw new DataItemNotFound();
        }

        const fileURL = window.URL.createObjectURL(
          new Blob([JSON.stringify(result.data, null, 2)], { type: "application/json" }),
        );

        // Safari needs the link in the document to follow it. Reuse it, rather than leaving one per file.
        if (!fileLink) {
          fileLink = document.createElement("a");
          document.body.appendChild(fileLink);
        }

        fileLink.href = fileURL;
        fileLink.setAttribute("download", `data_item_${itemId}.json`);

        fileLink.click();

        // Revoke the previous URL, whose download has started, rather than this one, which might not have.
        if (previousFileURL) {
          window.URL.revokeObjectURL(previousFileURL);
        }
        previousFileURL = fileURL;

        toast(t("examples.download.success"), "primary");
      })
      .catch(() => {
        toast(t("preview.nonExisting"), "danger");
      });
  }

  async function copyToClipboard(itemId: number) {
    // WebKit rejects write() with a DOMException rather than the error below, so keep our own reference to it.
    let reason: Error | undefined;
    // write() must be called during the click, so pass the data as a promise instead of awaiting it here.
    const blob = datasetStore.loadDataItem(itemId).then(
      () => {
        const json = datasetStore.dataItemJSON(itemId);

        if (json == null) {
          reason = new DataItemNotFound();
          throw reason;
        }
        if ((datasetStore.dataItemJSONLines(itemId) ?? 0) >= maxJSONLines) {
          reason = new DataItemTooLarge();
          throw reason;
        }
        // Chromium rejects a blob whose type differs from the item's, and a blob has none unless given one.
        return new Blob([json], { type: "text/plain" });
      },
      () => {
        reason = new DataItemNotFound();
        throw reason;
      },
    );

    try {
      await navigator.clipboard.write([new ClipboardItem({ "text/plain": blob })]);
      toast(t("examples.copyToClipboard.success"), "primary");
    } catch (error) {
      const cause = reason ?? error;

      if (cause instanceof DataItemTooLarge) {
        toast(t("examples.copyToClipboard.failure"), "danger");
      } else if (cause instanceof DataItemNotFound) {
        toast(t("preview.nonExisting"), "danger");
      } else {
        toast(cause instanceof Error ? cause.message : String(cause), "danger");
      }
    }
  }

  return { previewDataItem, previewData, loadingPreviewData, selectedKey, download, copyToClipboard };
}
