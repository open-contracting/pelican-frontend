<template>
    <modal name="datasetFilterModal" @before-open="beforeOpen">
        <date-pick
            v-model="releaseDateFrom"
            :startPeriod="this.firstDate != null ? {month: this.firstDate.getMonth(), year: this.firstDate.getFullYear()} : {month: 0, year: 2020}"
            :selectableYearRange="this.firstDate != null ? {from: this.firstDate.getFullYear(), to: this.lastDate.getFullYear()} : null"
            :inputAttributes="{readonly: true}"
            :isDateDisabled="dateIrrelevant"
        ></date-pick>
        <date-pick
            v-model="releaseDateTo"
            :startPeriod="this.firstDate != null ? {month: this.firstDate.getMonth(), year: this.firstDate.getFullYear()} : {month: 0, year: 2020}"
            :selectableYearRange="this.firstDate != null ? {from: this.firstDate.getFullYear(), to: this.lastDate.getFullYear()} : null"
            :inputAttributes="{readonly: true}"
            :isDateDisabled="dateIrrelevant"
        ></date-pick>
        <DatasetValuesMultiselect ref="buyerNameMultiselect" :datasetId="dataset != null ? dataset.id : null" jsonPath="buyer.name"/>
        <input v-model="buyerNameRegex" placeholder="edit me">
        <DatasetValuesMultiselect ref="procuringEntityNameMultiselect" :datasetId="dataset != null ? dataset.id : null" jsonPath="tender.procuringEntity.name"/>
        <input v-model="procuringEntityNameRegex" placeholder="edit me">
        <button @click="createDatasetFilter">submit</button>
        <p>{{ test }}</p>
    </modal>
</template>

<script>

const axios = require("axios");
const moment = require('moment');
import { CONFIG } from "@/config.js";
import DatasetValuesMultiselect from "@/components/DatasetValuesMultiselect.vue";

export default {
    data: function() {
        return {
            dataset: null,
            firstDate: null,
            lastDate: null,
            releaseDateFrom: null,
            releaseDateTo: null,
            buyerNameRegex: '',
            procuringEntityNameRegex: '',
            test: 'ok',
        };
    },
    components: { DatasetValuesMultiselect, },
    methods: {
        beforeOpen (event) {
            this.dataset = event.params.dataset;
            if (this.dataset.meta.period.length > 0) {
                this.firstDate = moment(this.dataset.meta.period[0].date_str, "MMM-YY").toDate();
                var date = moment(this.dataset.meta.period[this.dataset.meta.period.length - 1].date_str, "MMM-YY").toDate();
                this.lastDate = new Date(date.getFullYear(), date.getMonth() + 1, 0);
            } else {
                this.firstDate = null;
                this.lastDate = null;
            }
            this.releaseDateFrom = null;
            this.releaseDateTo = null;
            this.buyerNameRegex = '';
            this.procuringEntityNameRegex = '';
        },
        createDatasetFilter () {
            var data = {
                dataset_id_original: parseInt(this.dataset.id),
                filter_message: {},
            };

            if (this.releaseDateFrom != null) {
                data.filter_message.release_date_from = this.releaseDateFrom;
            }
            if (this.releaseDateTo != null) {
                data.filter_message.release_date_to = this.releaseDateTo;
            }
            if (this.$refs.buyerNameMultiselect.selected.length > 0) {
                data.filter_message.buyer = this.$refs.buyerNameMultiselect.selected;
            }
            if (this.buyerNameRegex.trim() != '') {
                data.filter_message.buyer_regex = this.buyerNameRegex.trim();
            }
            if (this.$refs.procuringEntityNameMultiselect.selected.length > 0) {
                data.filter_message.procuring_entity = this.$refs.procuringEntityNameMultiselect.selected;
            }
            if (this.procuringEntityNameRegex.trim() != '') {
                data.filter_message.procuring_entity_regex = this.procuringEntityNameRegex.trim();
            }
            axios
                .post(CONFIG.apiBaseUrl + CONFIG.apiEndpoints.createDatasetFilter, data)
                .then(response => {
                    if (response.status == 200) {
                        this.test = "okk";
                    } else {
                        this.test = "failed";
                    }
                    this.test = response.status;
                    this.$modal.hide('datasetFilterModal');
                })
                .catch(function(error) {
                    this.test = 'error';
                    throw new Error(error);
                });
        },
        dateIrrelevant (date) {
            return (date < this.firstDate) || (date > this.lastDate);
        }
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";


</style>
