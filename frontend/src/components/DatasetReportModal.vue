<template>
    <span class="just_holder">
        <Loader v-if="isSubmitting"></Loader>
        <span v-if="submitResult != null">
            <span v-if="submitResult == true">
                <b-alert class="submit-result" variant="success" show>
                    <span>
                        {{ $t("datasetReport.statusOk") }}
                    </span>
                    <span>
                        <a class="variant-success" v-on:click.stop.prevent="retry" href="#">
                            <font-awesome-icon :icon="['fas', 'redo-alt']" />
                        </a>
                    </span>
                </b-alert>
                <span class="info_prefix">{{ $t("datasetReport.link") }}:&nbsp;</span>
                <a :href="documentLink" target="_blank">{{ documentLink }}</a>
            </span>
            <span v-if="submitResult == false">
                <b-alert class="submit-result" variant="danger" show>
                    <span>{{ $t("datasetReport.statusFailed") }}</span>
                    <span>
                        <a class="variant-danger" v-on:click.stop.prevent="retry" href="#">
                            <font-awesome-icon :icon="['fas', 'redo-alt']" />
                        </a>
                    </span>
                </b-alert>
                <span v-if="errorMessage != null">
                    <span class="info_prefix">{{ $t("datasetReport.errorReason") }}:&nbsp;</span>{{ errorMessage }}
                </span>
            </span>
        </span>
        <form v-if="!isSubmitting && submitResult == null" class="modal_box align-items-center">
            <div class="form-group row section_row">
                <label class="col-3 col-form-label">{{ $t("datasetReport.documentId") }}</label>
                <div class="col-9">
                    <input class="base_input" v-model="documentId" />
                    <small class="form-text text-muted">{{ $t("datasetReport.documentIdTooltip") }}</small>
                </div>
            </div>
            <div class="form-group row section_row">
                <label class="col-3 col-form-label">{{ $t("datasetReport.folderId") }}</label>
                <div class="col-9">
                    <input class="base_input" v-model="folderId" />
                    <small class="form-text text-muted">{{ $t("datasetReport.folderIdTooltip") }}</small>
                </div>
            </div>
            <div class="text-center">
                <button
                    type="button"
                    class="btn btn-primary submit_button"
                    @click="createDatasetReport"
                    :disabled="dataset == null || !documentId || !folderId"
                >
                    {{ $t("datasetReport.submit") }}
                </button>
            </div>
        </form>
    </span>
</template>

<script>
const axios = require("axios");
import { CONFIG } from "@/config.js";
import Loader from "@/components/Loader.vue";

export default {
    props: ["dataset"],
    data: function() {
        return {
            isSubmitting: false,
            documentId: "",
            folderId: "",
            submitResult: null,
            documentLink: null,
            errorMessage: null
        };
    },
    components: { Loader },
    methods: {
        createDatasetReport() {
            if (this.dataset == null) { return; }
            this.errorMessage = null;
            this.isSubmitting = true;
            var documentIdMatch = this.documentId.match(/\/d\/([^/]+)/);
            var folderIdMatch = this.folderId.match(/\/folders\/([^/]+)/);

            axios
                .post(
                    CONFIG.apiBaseUrl + CONFIG.apiEndpoints.createDatasetReport,
                    {
                        "dataset_id": parseInt(this.dataset.id),
                        "document_id": documentIdMatch != null ? documentIdMatch[1] : this.documentId,
                        "folder_id": folderIdMatch != null ? folderIdMatch[1] : this.folderId
                    }
                )
                .then((response) => {
                    if (response.status == 200) {
                        this.submitResult = true;
                        this.documentLink = "https://docs.google.com/document/d/" + response.data;
                    } else {
                        this.submitResult = false;
                        this.errorMessage = response.statusText;
                    }
                })
                .catch((error) => {
                    this.submitResult = false;
                    this.errorMessage = error.response.statusText;
                })
                .finally(() => {
                    this.isSubmitting = false;
                });
        },
        reset() {
            this.isSubmitting = false;
            this.documentId = "";
            this.folderId = "";
            this.submitResult = null;
        },
        retry() {
            this.submitResult = null;
            this.createDatasetReport();
        }
    }
};
</script>

<style lang="scss">
@import "src/scss/main";

.submit-result {
    display: flex;
    justify-content: space-between;
}

.variant-success {
    color: #606602;
}

.variant-danger {
    color: #6C010E;
}

.modal_box {
    padding: 30px;
}

.modal_headline {
    padding-bottom: 30px;
}

.base_input {
    width: 100%;
    height: 100%;
    padding-right: 0px;
    font-size: 13px;
    font-family: $font-family-mono;
}

.modal_input {
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
}

.submit_button {
    font-size: 18px;
    font-weight: 700;
    color: $text-color;
    font-family: $font-family-sans-serif;
    background-color: transparent;
    border: 1px solid $na_color;
    margin-top: 20px;
}

.submit_button:hover {
    background-color: $na_color;
    color: white;
    border: 1px solid $na_color;
}

.procuring_row {
    padding-top: 15px;
}

.section_row {
    padding-top: 30px;
}

.date_picker label {
    text-align: left !important;
}

.multiselect__tag-icon:after {
    content: "×";
    color: white;
    font-size: 16px;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
    background: $gray-800;
}

.info_prefix {
    color: $headings-light-color;
}

</style>
