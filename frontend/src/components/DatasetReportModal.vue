<template>
    <span class="just_holder">
        <Loader v-if="isSubmitting"></Loader>
        <span v-if="submitResult != null">
            <span v-if="submitResult == true">
                <b-alert class="submit-result" variant="success" show>
                    <span>
                        {{ $t("datasetReport.statusOk") }}
                    </span>
                    <a class="variant-success" v-on:click.stop.prevent="reset" href="#">
                        <font-awesome-icon :icon="['fas', 'times']" />
                    </a>    
                </b-alert>
                <span>
                    {{ $t("datasetReport.link") }}
                    <a :href="documentLink">{{ documentLink }}</a>  
                </span>
            </span>
            <b-alert class="submit-result" v-if="submitResult == false" variant="danger" show>
                <span>{{ $t("datasetReport.statusFailed") }}</span>
                <a class="variant-danger" v-on:click.stop.prevent="reset" href="#">
                    <font-awesome-icon :icon="['fas', 'times']" />
                </a>
            </b-alert>
        </span>
        <form v-if="!isSubmitting && submitResult == null" class="modal_box align-items-center">
            <div class="form-group row section_row">
                <label class="col-3 col-form-label">{{ $t("datasetReport.documentId") }}</label>
                <div class="col-9">
                    <input class="document_id_input" v-model="documentId" />
                    <small class="form-text text-muted">{{ $t("datasetFilter.documentIdTooltip") }}</small>
                </div>
            </div>
            <div class="text-center">
                <button
                    type="button"
                    class="btn btn-primary submit_button"
                    @click="createDatasetReport"
                    :disabled="dataset == null || !documentId"
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
            submitResult: null,
            documentLink: null
        };
    },
    components: { Loader },
    methods: {
        createDatasetReport() {
            if (this.dataset == null) { return; }
            this.isSubmitting = true;
            axios
                .post(
                    CONFIG.apiBaseUrl + CONFIG.apiEndpoints.createDatasetReport,
                    {
                        "dataset_id": parseInt(this.dataset.id),
                        "document_id": this.documentId
                    }
                )
                .then((response) => {
                    if (response.status == 200) {
                        this.submitResult = true;
                        this.documentLink = "https://docs.google.com/document/d/" + response["data"];
                    } else {
                        this.submitResult = false;
                    }
                    this.isSubmitting = false;
                })
                .catch(() => {
                    this.submitResult = false;
                    this.isSubmitting = false;
                });
        },
        reset() {
            this.isSubmitting = false;
            this.documentId = "";
            this.submitResult = null;
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

.document_id_input {
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
</style>
