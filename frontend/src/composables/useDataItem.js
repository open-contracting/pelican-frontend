import { useToast } from "bootstrap-vue-next";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";

export function useDataItem() {
    const store = useStore();
    const { t } = useI18n();
    const { create: showToast } = useToast();

    function download(itemId) {
        store
            .dispatch("loadDataItem", itemId)
            .then(() => {
                const result = store.getters.dataItemById(itemId);
                const fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(result.data, null, 2)]));
                const fileLink = document.createElement("a");

                fileLink.href = fileURL;
                fileLink.setAttribute("download", `data_item_${itemId}.json`);
                document.body.appendChild(fileLink);

                fileLink.click();

                showToast({ body: t("examples.download.success"), variant: "primary", pos: "middle-center" });
            })
            .catch(() => {
                showToast({ body: t("preview.nonExisting"), variant: "danger", pos: "middle-center" });
            });
    }

    function copyToClipboard(itemId) {
        let message;

        const blobPromise = store.dispatch("loadDataItem", itemId).then(
            () => {
                if (store.getters.dataItemJSONLines(itemId) < 3000) {
                    return new Blob([store.getters.dataItemJSON(itemId)]);
                }
                message = "examples.copyToClipboard.failure";
                throw new Error();
            },
            () => {
                message = "preview.nonExisting";
                throw new Error();
            },
        );

        navigator.clipboard
            .write([new ClipboardItem({ "text/plain": blobPromise })])
            .then(() => {
                showToast({ body: t("examples.copyToClipboard.success"), variant: "primary", pos: "middle-center" });
            })
            .catch((error) => {
                showToast({ body: message ? t(message) : error.message, variant: "danger", pos: "middle-center" });
            });
    }

    return { download, copyToClipboard };
}
