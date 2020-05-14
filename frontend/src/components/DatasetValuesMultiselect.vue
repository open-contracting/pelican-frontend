<template>
    <multiselect
        v-model="selected"
        open-direction="bottom"
        label="value"
        track-by="value"
        :show-labels="false"
        :options="options"
        :multiple="true"
        :searchable="true"
        :loading="isLoading"
        :internal-search="false"
        :clear-on-select="false"
        :close-on-select="false"
        :options-limit="300"
        :limit="10"
        :limit-text="limitText"
        :max-height="300"
        :show-no-results="false"
        :hide-selected="true"
        @search-change="asyncFind"
    >
        <template slot="option" slot-scope="props">
            <div class="option__desc">
                <span class="option__title">{{ props.option.value }}</span>
                <span class="option__small">&nbsp;({{ props.option.count }} items)</span>
            </div>
        </template>
        <template slot="tag" slot-scope="{ option, remove }">
            <div class="multiselect__tag">
                <div>
                    <span>{{ option.value }}</span>
                    <span class="multiselect__tag__items__count">&nbsp;({{ option.count }} items)</span>
                    <i aria-hidden="true" tabindex="1" @click="remove(option)" class="multiselect__tag-icon"></i>
                </div>
            </div>
        </template>
        <template slot="clear" slot-scope="props">
            <div class="multiselect__clear" v-if="selected.length" @mousedown.prevent.stop="clearAll(props.search)"></div>
        </template>
        <span slot="noResult">{{ $t("datasetValuesMultiselect.noResult") }}</span>
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
            cancelToken: null
        };
    },
    props: ["datasetId", "jsonPath", "updateSelected"],
    methods: {
        beforeOpen(event) {
            this.datasetId = event.params.datasetId;
        },
        asyncFind(query) {
            if (this.cancelToken != null) {
                this.cancelToken.cancel();
                this.cancelToken = null;
            }
            this.isLoading = true;
            this.options = [];
            var url = null;
            if (query != "") {
                url =
                    CONFIG.apiBaseUrl +
                    CONFIG.apiEndpoints.datasetDistinctValues +
                    "/" +
                    this.datasetId +
                    "/" +
                    this.jsonPath +
                    "/" +
                    query;
            } else {
                url =
                    CONFIG.apiBaseUrl +
                    CONFIG.apiEndpoints.datasetDistinctValues +
                    "/" +
                    this.datasetId +
                    "/" +
                    this.jsonPath;
            }

            this.cancelToken = axios.CancelToken.source();
            var self = this;
            axios
                .get(url, { cancelToken: this.cancelToken.token })
                .then(response => {
                    this.options = response["data"];
                    this.isLoading = false;
                })
                .catch(function(error) {
                    self.isLoading = false;
                    throw new Error(error);
                });
        },
        clearAll() {
            this.selected = [];
        },
        limitText(count) {
            return count + this.$t("datasetValuesMultiselect.limitText");
        }
    },
    watch: {
        selected(value) {
            this.updateSelected(value.map(el => el.value));
        }
    },
    mounted() {
        this.asyncFind("");
    }
};
</script>

<style lang="scss">
@import "src/scss/main";

.multiselect__tag {
    background: $primary;
}

.multiselect__option--highlight {
    background: $primary;
    outline: none;
    color: white;
}

.multiselect__tag__items__count,
.option__small {
    font-style: italic;
}
</style>