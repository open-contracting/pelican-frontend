<template>
    <span class="just_holder">
        <Loader v-if="isSubmitting && submitResult == null"></Loader>
        <b-alert v-if="isSubmitting && submitResult != null" variant="success" show>{{ $t("datasetFilter.statusOk") }}</b-alert>
        <form v-if="!isSubmitting" class="modal_box align-items-center">
            <div class="form-group row">
                <label class="col-3 col-form-label">{{ $t("datasetFilter.releaseDateFromTo") }}</label>
                <div class="col-9 modal_input">
                    <div class="row">
                        <div class="col">
                            <b-form-datepicker
                                :min="firstDate"
                                :max="lastDate"
                                :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
                                v-model="releaseDateFrom"
                                class="date_picker"
                            ></b-form-datepicker>
                        </div>
                        <div class="col">
                            <b-form-datepicker
                                :min="firstDate"
                                :max="lastDate"
                                :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
                                v-model="releaseDateTo"
                                class="date_picker"
                            ></b-form-datepicker>
                        </div>
                    </div>
                </div>
            </div>
            <div class="form-group row section_row">
                <label class="col-3 col-form-label">{{ $t("datasetFilter.buyerName") }}</label>
                <div class="col-9">
                    <DatasetValuesMultiselect :updateSelected="updateBuyerName" :datasetId="dataset != null ? dataset.id : null" jsonPath="buyer.name" />
                </div>
            </div>
            <div class="form-group row">
                <label class="col-3 col-form-label">{{ $t("datasetFilter.procuringEntityName") }}</label>
                <div class="col-9">
                    <DatasetValuesMultiselect
                        :updateSelected="updateProcuringEntityName"
                        :datasetId="dataset != null ? dataset.id : null"
                        jsonPath="tender.procuringEntity.name"
                    />
                </div>
            </div>
            <div class="form-group row section_row">
                <label class="col-3 col-form-label">{{ $t("datasetFilter.buyerNameRegex") }}</label>
                <div class="col-9">
                    <input class="regex_input" v-model="buyerNameRegex" />
                    <small class="form-text text-muted">{{ $t("datasetFilter.buyerNameRegexTooltip") }}</small>
                </div>
            </div>
            <div class="form-group row procuring_row">
                <label class="col-3 col-form-label">{{ $t("datasetFilter.procuringEntityNameRegex") }}</label>
                <div class="col-9">
                    <input class="regex_input" v-model="procuringEntityNameRegex" />
                    <small class="form-text text-muted">{{ $t("datasetFilter.procuringEntityNameRegexTooltip") }}</small>
                </div>
            </div>
            <div class="text-center">
                <button
                    type="button"
                    class="btn btn-primary submit_button"
                    @click="createDatasetFilter"
                    :disabled="items == 0 || (dataset != null && items == dataset.size) || gettingCountsToken != null"
                >
                    {{ $t("datasetFilter.submit") }}
                    <span v-if="gettingCountsToken == null">
                        <span
                            v-if="items!= null && items > 0  && (dataset != null && items != dataset.size)"
                        >({{ items | formatNumber }} from {{ dataset.size | formatNumber }} {{ $t("datasetFilter.items") }})</span>
                        <span v-if="(dataset != null && items == dataset.size)">({{ $t("datasetFilter.itemsAll") }})</span>
                    </span>
                    <b-spinner v-if="gettingCountsToken != null" variant="default" style="width: 1.2rem; height: 1.2rem;"></b-spinner>
                </button>
            </div>
        </form>
    </span>
</template>

<script>
const axios = require("axios");
const moment = require("moment");
import { CONFIG } from "@/config.js";
import Loader from "@/components/Loader.vue";
import DatasetValuesMultiselect from "@/components/DatasetValuesMultiselect.vue";

export default {
    props: ["dataset"],
    data: function() {
        return {
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
            items: null
        };
    },
    computed: {
        firstDate: function() {
            if (this.dataset.meta.period.length > 0) {
                return moment(
                    this.dataset.meta.period[0].date_str,
                    "MMM-YY"
                ).toDate();
            } else {
                return null;
            }
        },
        lastDate: function() {
            if (this.dataset.meta.period.length > 0) {
                var date = moment(
                    this.dataset.meta.period[
                        this.dataset.meta.period.length - 1
                    ].date_str,
                    "MMM-YY"
                ).toDate();
                return new Date(date.getFullYear(), date.getMonth() + 1, 0);
            } else {
                return null;
            }
        }
    },
    mounted() {
        this.$watch(
            vm => [
                vm.releaseDateFrom,
                vm.releaseDateTo,
                vm.buyerName,
                vm.procuringEntityName,
                vm.buyerNameRegex,
                vm.procuringEntityNameRegex
            ],
            () => {
                if (this.filteredItemsTimeout) {
                    clearTimeout(this.filteredItemsTimeout);
                }

                this.filteredItemsTimeout = setTimeout(
                    () => this.datasetFilterItems(),
                    this.filteredItemsTimeoutLimit
                );
            },
            {
                immediate: true,
                deep: true
            }
        );

        this.releaseDateFrom = this.firstDate;
        this.releaseDateTo = this.lastDate;
        this.datasetFilterItems();
    },
    components: { DatasetValuesMultiselect, Loader },
    methods: {
        createDatasetFilter() {
            this.isSubmitting = true;
            axios
                .post(
                    CONFIG.apiBaseUrl + CONFIG.apiEndpoints.createDatasetFilter,
                    this.datasetFilterMessage()
                )
                .then(response => {
                    if (response.status == 200) {
                        this.submitResult = this.$t(
                            "datasetFilter.submitResultOk"
                        );
                    } else {
                        this.submitResult = this.$t(
                            "datasetFilter.submitResultOk"
                        );
                    }

                    setTimeout(() => {
                        this.$bvModal.hide();
                        this.$router.go();
                    }, 2000);
                })
                .catch(function(error) {
                    // TODO
                    throw new Error(error);
                });
        },
        datasetFilterItems() {
            var message = this.datasetFilterMessage();
            if (message == null) {
                return;
            }

            if (this.gettingCountsToken != null) {
                this.gettingCountsToken.cancel(
                    "Operation canceled by the user."
                );
            }

            this.gettingCountsToken = axios.CancelToken.source();
            axios
                .post(
                    CONFIG.apiBaseUrl + CONFIG.apiEndpoints.datasetFilterItems,
                    message,
                    {
                        cancelToken: this.gettingCountsToken.token
                    }
                )
                .then(response => {
                    if (response.status == 200) {
                        this.items = response["data"]["items"];
                    } else {
                        this.items = null;
                    }

                    this.gettingCountsToken = null;
                })
                .catch(function(error) {
                    // TODO
                    throw new Error(error);
                });
        },
        dateIrrelevant(date) {
            return date < this.firstDate || date > this.lastDate;
        },
        datasetFilterMessage() {
            if (this.dataset == null) {
                return null;
            }

            var data = {
                dataset_id_original: parseInt(this.dataset.id),
                filter_message: {}
            };

            if (this.releaseDateFrom != "") {
                data.filter_message.release_date_from = this.releaseDateFrom;
            }
            if (this.releaseDateTo != "") {
                data.filter_message.release_date_to = this.releaseDateTo;
            }
            if (this.buyerName.length > 0) {
                data.filter_message.buyer = this.buyerName;
            }
            if (this.buyerNameRegex.trim() != "") {
                data.filter_message.buyer_regex = this.buyerNameRegex.trim();
            }
            if (this.procuringEntityName.length > 0) {
                data.filter_message.procuring_entity = this.procuringEntityName;
            }
            if (this.procuringEntityNameRegex.trim() != "") {
                data.filter_message.procuring_entity_regex = this.procuringEntityNameRegex.trim();
            }

            return data;
        },
        updateBuyerName(value) {
            this.buyerName = value;
        },
        updateProcuringEntityName(value) {
            this.procuringEntityName = value;
        }
    }
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
