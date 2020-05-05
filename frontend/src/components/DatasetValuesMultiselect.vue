<template>
    <multiselect
        v-model="selected"
        placeholder="Enter buyer names"
        open-direction="bottom"
        :options="options"
        :multiple="true"
        :searchable="true"
        :loading="isLoading"
        :internal-search="false"
        :clear-on-select="false"
        :close-on-select="false"
        :options-limit="300"
        :limit="3"
        :limit-text="limitText"
        :max-height="600"
        :show-no-results="false"
        :hide-selected="true"
        @search-change="asyncFind"
    >
        <template
            slot="tag"
            slot-scope="{ option, remove }"
        >
            <span class="custom__tag">
                <span>{{ option }}</span>
                <span class="custom__remove" @click="remove(option)">❌</span>
            </span>
        </template>
        <template slot="clear" slot-scope="props">
            <div class="multiselect__clear" v-if="selected.length" @mousedown.prevent.stop="clearAll(props.search)"></div>
        </template>
        <span slot="noResult">Oops! No elements found. Consider changing the search query.</span>
    </multiselect>
</template>

<script>

const axios = require("axios");
import { CONFIG } from "@/config.js";

export default {
    data: function() {
        return {
            options: [],
            selected: [],
            isLoading: false,
        };
    },
    props: ["datasetId", "jsonPath"],
    methods: {
        beforeOpen (event) {
            this.datasetId = event.params.datasetId;
        },
        asyncFind (query) {
            this.isLoading = true;
            var url = null;
            if (query != '') {
                url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.datasetDistinctValues +
                    '/' + this.datasetId + '/' + this.jsonPath + '/' + query;
            } else {
                url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.datasetDistinctValues +
                    '/' + this.datasetId + '/' + this.jsonPath
            }
            axios
                .get(url)
                .then(response => {
                    this.options = response["data"];
                    this.isLoading = false;
                })
                .catch(function(error) {
                    this.isLoading = false;
                    throw new Error(error);
                });
        },
        clearAll () {
            this.selected = [];
        },
        limitText (count) {
            return `and ${count} more`
        }
    },
    
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
