import { useToast } from "bootstrap-vue-next";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";

class DataItemNotFound extends Error {}
class DataItemTooLarge extends Error {}

export function useDataItem() {
    const store = useStore();
    const { t } = useI18n();
    const { create: showToast } = useToast();

    function toast(body, variant) {
        showToast({ body, variant, pos: "middle-center" });
    }

    function download(itemId) {
        store
            .dispatch("loadDataItem", itemId)
            .then(() => {
                const result = store.getters.dataItemById(itemId);
                const fileURL = window.URL.createObjectURL(
                    new Blob([JSON.stringify(result.data, null, 2)], { type: "application/json" }),
                );
                const fileLink = document.createElement("a");

                fileLink.href = fileURL;
                fileLink.setAttribute("download", `data_item_${itemId}.json`);
                document.body.appendChild(fileLink);

                fileLink.click();

                toast(t("examples.download.success"), "primary");
            })
            .catch(() => {
                toast(t("preview.nonExisting"), "danger");
            });
    }

    async function copyToClipboard(itemId) {
        // WebKit rejects write() with a DOMException rather than the error below, so keep our own reference to it.
        let reason;
        // write() must be called during the click, so pass the data as a promise instead of awaiting it here.
        const blob = store.dispatch("loadDataItem", itemId).then(
            () => {
                if (store.getters.dataItemJSONLines(itemId) >= 3000) {
                    reason = new DataItemTooLarge();
                    throw reason;
                }
                // Chromium rejects a blob whose type differs from the item's, and a blob has none unless given one.
                return new Blob([store.getters.dataItemJSON(itemId)], { type: "text/plain" });
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
                toast(cause.message, "danger");
            }
        }
    }

    return { download, copyToClipboard };
}
