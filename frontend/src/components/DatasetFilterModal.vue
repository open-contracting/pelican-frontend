<template>
  <span class="just_holder">
    <Loader v-if="isSubmitting && submitResult == null" />
    <b-alert
      v-if="isSubmitting && submitResult != null"
      variant="success"
      show
    >{{
      $t("datasetFilter.statusOk")
    }}</b-alert>
    <form
      v-if="!isSubmitting"
      class="modal_box align-items-center"
    >
      <div class="form-group row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.releaseDateFromTo") }}</label>
        <div class="col-8 modal_input">
          <div class="row">
            <div class="col">
              <b-form-datepicker
                v-model="releaseDateFrom"
                :min="firstDate"
                :max="lastDate"
                :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
                class="date_picker"
              />
            </div>
            <div class="col">
              <b-form-datepicker
                v-model="releaseDateTo"
                :min="firstDate"
                :max="lastDate"
                :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
                class="date_picker"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="form-group row section_row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.buyerName") }}</label>
        <div class="col-8">
          <DatasetValuesMultiselect
            :update-selected="updateBuyerName"
            :dataset-id="dataset != null ? dataset.id : null"
            json-path="buyer.name"
          />
        </div>
      </div>
      <div class="form-group row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.procuringEntityName") }}</label>
        <div class="col-8">
          <DatasetValuesMultiselect
            :update-selected="updateProcuringEntityName"
            :dataset-id="dataset != null ? dataset.id : null"
            json-path="tender.procuringEntity.name"
          />
        </div>
      </div>
      <div class="form-group row section_row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.buyerNameRegex") }}</label>
        <div class="col-8">
          <input
            v-model="buyerNameRegex"
            class="regex_input"
          >
          <small class="form-text text-muted">{{ $t("datasetFilter.buyerNameRegexTooltip") }}</small>
        </div>
      </div>
      <div class="form-group row procuring_row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.procuringEntityNameRegex") }}</label>
        <div class="col-8">
          <input
            v-model="procuringEntityNameRegex"
            class="regex_input"
          >
          <small class="form-text text-muted">{{
            $t("datasetFilter.procuringEntityNameRegexTooltip")
          }}</small>
        </div>
      </div>
      <div class="text-center">
        <button
          type="button"
          class="btn btn-primary submit_button"
          :disabled="items == 0 || (dataset != null && items == dataset.meta.compiled_releases?.total_unique_ocids) || gettingCountsToken != null"
          @click="createDatasetFilter"
        >
          {{ $t("datasetFilter.submit") }}
          <span v-if="gettingCountsToken == null">
            <span
              v-if="items != null && items > 0 && dataset != null && items != dataset.meta.compiled_releases?.total_unique_ocids"
            >({{ items | formatNumber }} from {{ dataset.meta.compiled_releases?.total_unique_ocids | formatNumber }}
              {{ $t("datasetFilter.items") }})</span>
            <span
              v-if="dataset != null && items == dataset.meta.compiled_releases?.total_unique_ocids"
            >({{ $t("datasetFilter.itemsAll") }})</span>
          </span>
          <b-spinner
            v-if="gettingCountsToken != null"
            variant="default"
            style="width: 1.2rem; height: 1.2rem"
          />
        </button>
      </div>
    </form>
  </span>
</template>

<script>
const axios = require("axios");
import DatasetValuesMultiselect from "@/components/DatasetValuesMultiselect.vue";
import Loader from "@/components/Loader.vue";
import { CONFIG } from "@/config.js";

export default {
    components: { DatasetValuesMultiselect, Loader },
    props: ["dataset"],
    data: () => ({
        isSubmitting: false,
        gettingCountsToken: null,
        filteredItemsTimeout: null,
        filteredItemsTimeoutLimit: 400,
        releaseDateFrom: null,
        releaseDateTo: null,
        buyerName: [],
        procuringEntityName: [],
        buyerNameRegex: "",
        procuringEntityNameRegex: "",
        submitResult: null,
        items: null,
    }),
    computed: {
        firstDate: function () {
            var publishedFrom = this.dataset.meta.collection_metadata.published_from;
            if (publishedFrom) {
                return publishedFrom.substring(0, 10);
            } else {
                return "1970-01-01";
            }
        },
        lastDate: function () {
            var publishedTo = this.dataset.meta.collection_metadata.published_to;
            if (publishedTo) {
                return publishedTo.substring(0, 10);
            } else {
                return new Date().toISOString().split("T")[0];
            }
        },
    },
    mounted() {
        this.$watch(
            (vm) => [
                vm.releaseDateFrom,
                vm.releaseDateTo,
                vm.buyerName,
                vm.procuringEntityName,
                vm.buyerNameRegex,
                vm.procuringEntityNameRegex,
            ],
            () => {
                if (this.filteredItemsTimeout) {
                    clearTimeout(this.filteredItemsTimeout);
                }

                this.filteredItemsTimeout = setTimeout(
                    () => this.datasetFilterItems(),
                    this.filteredItemsTimeoutLimit,
                );
            },
            {
                immediate: true,
                deep: true,
            },
        );

        this.releaseDateFrom = this.firstDate;
        this.releaseDateTo = this.lastDate;
        this.datasetFilterItems();
    },
    methods: {
        createDatasetFilter() {
            this.isSubmitting = true;
            axios
                .post(
                    `${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.createDatasetFilter.replace(/{id}/g, this.dataset.id)}`,
                    this.datasetFilterMessage(),
                )
                .then((response) => {
                    if (response.status == 200) {
                        this.submitResult = this.$t("datasetFilter.submitResultOk");
                    } else {
                        this.submitResult = this.$t("datasetFilter.submitResultFailed");
                    }

                    setTimeout(() => {
                        this.$bvModal.hide();
                        this.$router.go();
                    }, 2000);
                })
                .catch((error) => {
                    // TODO
                    throw new Error(error);
                });
        },
        datasetFilterItems() {
            if (this.dataset == null) {
                return;
            }

            // https://axios-http.com/docs/cancellation
            if (this.gettingCountsToken != null) {
                this.gettingCountsToken.cancel();
            }

            this.gettingCountsToken = axios.CancelToken.source();

            axios
                .post(
                    `${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.datasetFilterItems}`,
                    {
                        dataset_id_original: Number.parseInt(this.dataset.id),
                        filter_message: this.datasetFilterMessage(),
                    },
                    {
                        cancelToken: this.gettingCountsToken.token,
                    },
                )
                .then((response) => {
                    if (response.status == 200) {
                        this.items = response["data"]["items"];
                    } else {
                        this.items = null;
                    }

                    this.gettingCountsToken = null;
                })
                .catch((error) => {
                    if (!axios.isCancel(error)) {
                        throw new Error(error);
                    }
                });
        },
        datasetFilterMessage() {
            if (this.dataset == null) {
                return null;
            }

            var data = {};

            if (this.releaseDateFrom > this.firstDate) {
                data.release_date_from = this.releaseDateFrom;
            }
            if (this.releaseDateTo < this.lastDate) {
                data.release_date_to = this.releaseDateTo;
            }
            if (this.buyerName.length > 0) {
                data.buyer = this.buyerName;
            }
            if (this.buyerNameRegex.trim() != "") {
                data.buyer_regex = this.buyerNameRegex.trim();
            }
            if (this.procuringEntityName.length > 0) {
                data.procuring_entity = this.procuringEntityName;
            }
            if (this.procuringEntityNameRegex.trim() != "") {
                data.procuring_entity_regex = this.procuringEntityNameRegex.trim();
            }

            return data;
        },
        updateBuyerName(value) {
            this.buyerName = value;
        },
        updateProcuringEntityName(value) {
            this.procuringEntityName = value;
        },
    },
};
</script>

<style lang="scss">
@import "src/scss/main";

.modal_box {
    padding: 30px;
}

.modal_headline {
    padding-bottom: 30px;
}

.regex_input {
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
