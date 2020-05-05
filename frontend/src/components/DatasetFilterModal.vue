<template>
    <modal name="datasetFilterModal" @before-open="beforeOpen">
        <multiselect
            v-model="values"
            :options="buyerNames"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Pick some"
            :preselect-first="true"
        >
            <template
                slot="selection"
                slot-scope="{ values, search, isOpen }"
            >
                <span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">
                    {{ values.length }} options selected
                </span>
            </template>
        </multiselect>
        <p>{{ values }}</p>
    </modal>
</template>

<script>

const axios = require("axios");
import { CONFIG } from "@/config.js";

export default {
    data: function() {
        return {
            values: [],
            datasetId: null,
            buyerNames: [],
            procuringEntityNames: [],
        };
    },
    methods: {
        beforeOpen (event) {
            this.datasetId = event.params.datasetId;
        }
    },
    watch: {
        datasetId: function (newValue) {
            if (newValue == null) return;
            
            // fetching buyer names
            axios
                .get(
                    CONFIG.apiBaseUrl + CONFIG.apiEndpoints.datasetDistinctValues +
                    '/' + newValue + '/' + 'buyer.name'
                )
                .then(response => {
                    this.buyerNames = response["data"];
                })
                .catch(function(error) {
                    throw new Error(error);
                });

            // fetching procuring entity names
            axios
                .get(
                    CONFIG.apiBaseUrl + CONFIG.apiEndpoints.datasetDistinctValues +
                    '/' + newValue + '/' + 'tender.procuringEntity.name'
                )
                .then(response => {
                    this.procuringEntityNames = response["data"];
                })
                .catch(function(error) {
                    throw new Error(error);
                });
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

// .box {
//     border-radius: 10px;
//     padding: 35px;
//     box-shadow: 0 2px 18px 6px rgba(0, 0, 0, 0.06);
//     border: 0;
// }

</style>
