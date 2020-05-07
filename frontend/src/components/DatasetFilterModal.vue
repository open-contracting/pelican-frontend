<template>
    <modal
        name="datasetFilterModal"
        width="50%"
        height="50%"
        :pivotY="0.38"
        :minWidth="800"
        :minHeight="600"
        :adaptive="true"
        :scrollable="true"
        
        @before-open="beforeOpen"
    >
        <form class="modal_box align-items-center">
            <h5>Dataset filter</h5>
            <div class="form-group row">
                <label class="col-sm-5 col-form-label">{{ $t("datasetFilter.releaseDateFrom") }}</label>
                <div class="col-sm-4 modal_input">
                    <date-pick
                        class="test"
                        v-model="releaseDateFrom"
                        :startPeriod="this.firstDate != null ? {month: this.firstDate.getMonth(), year: this.firstDate.getFullYear()} : {month: 0, year: 2020}"
                        :selectableYearRange="this.firstDate != null ? {from: this.firstDate.getFullYear(), to: this.lastDate.getFullYear()} : null"
                        :inputAttributes="{readonly: true}"
                        :isDateDisabled="dateIrrelevant"
                    ></date-pick>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-sm-5 col-form-label">{{ $t("datasetFilter.releaseDateTo") }}</label>
                <div class="col-sm-4">
                    <date-pick
                        v-model="releaseDateTo"
                        :startPeriod="this.firstDate != null ? {month: this.firstDate.getMonth(), year: this.firstDate.getFullYear()} : {month: 0, year: 2020}"
                        :selectableYearRange="this.firstDate != null ? {from: this.firstDate.getFullYear(), to: this.lastDate.getFullYear()} : null"
                        :inputAttributes="{readonly: true}"
                        :isDateDisabled="dateIrrelevant"
                    ></date-pick>
                </div>
            </div>
            <!-- <div class="form-group row">
            </div> -->
            <div class="form-group row">
                <label class="col-sm-5 col-form-label">{{ $t("datasetFilter.buyerName") }}</label>
                <div class="col-sm-4">
                    <DatasetValuesMultiselect :updateSelected="updateBuyerName" :datasetId="dataset != null ? dataset.id : null" jsonPath="buyer.name"/>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-sm-5 col-form-label">{{ $t("datasetFilter.procuringEntityName") }}</label>
                <div class="col-sm-4">
                    <DatasetValuesMultiselect :updateSelected="updateProcuringEntityName" :datasetId="dataset != null ? dataset.id : null" jsonPath="tender.procuringEntity.name"/>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-sm-5 col-form-label">{{ $t("datasetFilter.buyerNameRegex") }}</label>
                <div class="col-sm-4">
                    <input class="regex_input" v-model="buyerNameRegex">
                </div>
            </div>
            <div class="form-group row">
                <label class="col-sm-5 col-form-label">{{ $t("datasetFilter.procuringEntityNameRegex") }}</label>
                <div class="col-sm-4">
                    <input class="regex_input" v-model="procuringEntityNameRegex">
                </div>
            </div>
            <div class="text-center">
                <span v-if="submitResult" class="text-center">
                    {{ submitResult }}
                </span>
                <Loader v-else-if="isSubmitting">
                </Loader>
                <button
                    v-else
                    type="button"
                    class="btn btn-default submit_button"
                    @click="createDatasetFilter"
                >
                    {{ $t("datasetFilter.submit") }}
                </button>
            </div>
        </form>      
        <p>{{ items }}</p>
        <!-- <div class="modal_box"> -->
            <!-- <button class="align-self-right">
                <font-awesome-icon :icon="['fas', 'times']"/>
            </button>> -->
            
        <!-- </div> -->
    </modal>
</template>

<script>

const axios = require("axios");
const moment = require('moment');
import { CONFIG } from "@/config.js";
import Loader from "@/components/Loader.vue";
import DatasetValuesMultiselect from "@/components/DatasetValuesMultiselect.vue";

export default {
    data: function() {
        return {
            isSubmitting: false,
            filteredItemsTimeout: null,
            filteredItemsTimeoutLimit: 400,
            dataset: null,
            firstDate: null,
            lastDate: null,
            releaseDateFrom: null,
            releaseDateTo: null,
            buyerName: [],
            procuringEntityName: [],
            buyerNameRegex: '',
            procuringEntityNameRegex: '',
            submitResult: null,
            items: null,
        };
    },
    mounted () {        
        this.$watch(vm => [vm.releaseDateFrom, vm.releaseDateTo, vm.buyerName, vm.procuringEntityName, vm.buyerNameRegex, vm.procuringEntityNameRegex], () => {
            if (this.filteredItemsTimeout) {
                clearTimeout(this.filteredItemsTimeout);
            }
            
            this.filteredItemsTimeout = setTimeout(() => this.datasetFilterItems(), this.filteredItemsTimeoutLimit);
        }, {
            immediate: true, // run immediately
            deep: true // detects changes inside objects. not needed here, but maybe in other cases
        }); 
    },
    components: { DatasetValuesMultiselect, Loader, },
    methods: {
        beforeOpen (event) {
            this.isSubmitting = false;
            this.submitResult = null;
            this.dataset = event.params.dataset;
            if (this.dataset.meta.period.length > 0) {
                this.firstDate = moment(this.dataset.meta.period[0].date_str, "MMM-YY").toDate();
                var date = moment(this.dataset.meta.period[this.dataset.meta.period.length - 1].date_str, "MMM-YY").toDate();
                this.lastDate = new Date(date.getFullYear(), date.getMonth() + 1, 0);
            } else {
                this.firstDate = null;
                this.lastDate = null;
            }
            this.releaseDateFrom = '';
            this.releaseDateTo = '';
            this.buyerNameRegex = '';
            this.procuringEntityNameRegex = '';
        },
        createDatasetFilter () {
            this.isSubmitting = true;
            axios
                .post(CONFIG.apiBaseUrl + CONFIG.apiEndpoints.createDatasetFilter, this.datasetFilterMessage())
                .then(response => {
                    if (response.status == 200) {
                        this.submitResult = this.$t("datasetFilter.submitResultOk");
                    } else {
                        this.submitResult = this.$t("datasetFilter.submitResultOk");
                    }

                    setTimeout(() => {this.$modal.hide('datasetFilterModal'); this.$router.go();}, 2000);
                })
                .catch(function(error) {
                    // TODO
                    throw new Error(error);
                });
        },
        datasetFilterItems () {
            axios
                .post(CONFIG.apiBaseUrl + CONFIG.apiEndpoints.datasetFilterItems, this.datasetFilterMessage())
                .then(response => {
                    if (response.status == 200) {
                        this.items = response['data']['items'];
                    } else {
                        this.items = null;
                    }
                })
                .catch(function(error) {
                    // TODO
                    throw new Error(error);
                });
        },
        dateIrrelevant (date) {
            return (date < this.firstDate) || (date > this.lastDate);
        },
        datasetFilterMessage () {
            if (this.dataset == null) {
                return null;
            }

            var data = {
                dataset_id_original: parseInt(this.dataset.id),
                filter_message: {},
            };

            if (this.releaseDateFrom != '') {
                data.filter_message.release_date_from = this.releaseDateFrom;
            }
            if (this.releaseDateTo != '') {
                data.filter_message.release_date_to = this.releaseDateTo;
            }
            if (this.buyerName.length > 0) {
                data.filter_message.buyer = this.buyerName;
            }
            if (this.buyerNameRegex.trim() != '') {
                data.filter_message.buyer_regex = this.buyerNameRegex.trim();
            }
            if (this.procuringEntityName.length > 0) {
                data.filter_message.procuring_entity = this.procuringEntityName;
            }
            if (this.procuringEntityNameRegex.trim() != '') {
                data.filter_message.procuring_entity_regex = this.procuringEntityNameRegex.trim();
            }

            return data;
        },
        updateBuyerName (value) {
            this.buyerName = value;
        },
        updateProcuringEntityName (value) {
            this.procuringEntityName = value;
        },
    },
    beforeDestroy () {
        clearTimeout(this.filteredItemsTimeout);
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.modal_box {
    padding: 30px;
}

.regex_input {
    width: 100%;
    height: 100%;
    padding-right: 0px;
    font-size: 13px;
    font-family: $font-family-mono;
    // color: #495057;
	// background-color: #fff;
	// background-clip: padding-box;
	// border: 1px solid #ced4da;
	// border-radius: 0.25rem;
	// -webkit-transition: border-color 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out;
	// transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out;
}

.modal_input {
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
    // text-align: left;
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


</style>
