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
    <template #option="props">
      <div class="option__desc">
        <span class="option__title">{{ props.option.value }}</span>
        <span class="option__small">&nbsp;({{ props.option.count }} items)</span>
      </div>
    </template>
    <template #tag="{ option, remove }">
      <div class="multiselect__tag">
        <div>
          <span>{{ option.value }}</span>
          <span class="multiselect__tag__items__count">&nbsp;({{ option.count }} items)</span>
          <i
            tabindex="1"
            class="multiselect__tag-icon"
            @click="remove(option)"
          />
        </div>
      </div>
    </template>
    <template #clear="props">
      <div
        v-if="selected.length"
        class="multiselect__clear"
        @mousedown.prevent.stop="clearAll(props.search)"
      />
    </template>
    <template #noResult>{{ $t("datasetValuesMultiselect.noResult") }}</template>
  </multiselect>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";
import { CONFIG } from "@/config.js";

const props = defineProps(["datasetId", "jsonPath", "updateSelected"]);

const { t } = useI18n();

const options = ref([]);
const selected = ref([]);
const isLoading = ref(false);
let cancelToken = null;

watch(selected, (value) => {
    props.updateSelected(value.map((el) => el.value));
});

function asyncFind(query) {
    if (cancelToken != null) {
        cancelToken.cancel();
        cancelToken = null;
    }
    isLoading.value = true;
    options.value = [];
    let url = `${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.datasetDistinctValues}${props.datasetId}/${props.jsonPath}/`;
    if (query) {
        url += `${query}/`;
    }

    cancelToken = axios.CancelToken.source();
    axios
        .get(url, { cancelToken: cancelToken.token })
        .then((response) => {
            options.value = response.data;
            isLoading.value = false;
        })
        .catch((error) => {
            isLoading.value = false;
            throw new Error(error);
        });
}

function clearAll() {
    selected.value = [];
}

function limitText(count) {
    return t("datasetValuesMultiselect.limitText", { n: count });
}

onMounted(() => {
    asyncFind("");
});
</script>

<style lang="scss">
@import "@/scss/main";

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
