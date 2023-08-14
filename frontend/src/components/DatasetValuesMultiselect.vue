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
    <template
      slot="option"
      slot-scope="props"
    >
      <div class="option__desc">
        <span class="option__title">{{ props.option.value }}</span>
        <span class="option__small">&nbsp;({{ props.option.count }} items)</span>
      </div>
    </template>
    <template
      slot="tag"
      slot-scope="{ option, remove }"
    >
      <div class="multiselect__tag">
        <div>
          <span>{{ option.value }}</span>
          <span class="multiselect__tag__items__count">&nbsp;({{ option.count }} items)</span>
          <i
            aria-hidden="true"
            tabindex="1"
            class="multiselect__tag-icon"
            @click="remove(option)"
          />
        </div>
      </div>
    </template>
    <template
      slot="clear"
      slot-scope="props"
    >
      <div
        v-if="selected.length"
        class="multiselect__clear"
        @mousedown.prevent.stop="clearAll(props.search)"
      />
    </template>
    <span slot="noResult">{{ $t("datasetValuesMultiselect.noResult") }}</span>
  </multiselect>
</template>

<script>
const axios = require("axios");
import { CONFIG } from "@/config.js";

export default {
    props: ["datasetId", "jsonPath", "updateSelected"],
    data: function () {
        return {
            options: [],
            selected: [],
            isLoading: false,
            cancelToken: null
        };
    },
    watch: {
        selected(value) {
            this.updateSelected(value.map(el => el.value));
        }
    },
    mounted() {
        this.asyncFind("");
    },
    methods: {
        asyncFind(query) {
            if (this.cancelToken != null) {
                this.cancelToken.cancel();
                this.cancelToken = null;
            }
            this.isLoading = true;
            this.options = [];
            var url = `${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.datasetDistinctValues}/${this.datasetId}/${this.jsonPath}/`;
            if (query) {
                url += `${query}/`;
            }

            this.cancelToken = axios.CancelToken.source();
            var self = this;
            axios
                .get(url, { cancelToken: this.cancelToken.token })
                .then(response => {
                    this.options = response["data"];
                    this.isLoading = false;
                })
                .catch(function (error) {
                    self.isLoading = false;
                    throw new Error(error);
                });
        },
        clearAll() {
            this.selected = [];
        },
        limitText(count) {
            return this.$t("datasetValuesMultiselect.limitText", { n: count });
        }
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
