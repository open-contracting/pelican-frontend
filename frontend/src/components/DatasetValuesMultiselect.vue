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
        <span class="option__small">({{ props.option.count }} items)</span>
      </div>
    </template>
    <template #tag="{ option, remove }">
      <div class="multiselect__tag">
        <div>
          <span>{{ option.value }}</span>
          <span class="multiselect__tag__items__count">({{ option.count }} items)</span>
          <i
            tabindex="1"
            class="multiselect__tag-icon"
            @click="remove(option)"
          />
        </div>
      </div>
    </template>
    <template #clear>
      <div
        v-if="selected.length"
        class="multiselect__clear"
        @mousedown.prevent.stop="clearAll()"
      />
    </template>
    <template #noResult>{{ $t("datasetValuesMultiselect.noResult") }}</template>
  </multiselect>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";
import { CONFIG } from "@/config.js";
import type { DistinctValue } from "@/types.js";

const props = defineProps<{
  datasetId: number;
  jsonPath: string;
}>();
const emit = defineEmits<{ selected: [values: string[]] }>();

const { t } = useI18n();

const options = ref<DistinctValue[]>([]);
const selected = ref<DistinctValue[]>([]);
const isLoading = ref(false);
let controller: AbortController | null = null;

watch(selected, (value) => {
  emit(
    "selected",
    value.map((el) => el.value),
  );
});

function asyncFind(query: string) {
  controller?.abort();
  isLoading.value = true;
  options.value = [];
  let url = `${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.datasetDistinctValues}${props.datasetId}/${props.jsonPath}/`;
  if (query) {
    url += `${query}/`;
  }

  controller = new AbortController();
  fetch(url, { signal: controller.signal })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
      }
      return response.json();
    })
    .then((data: DistinctValue[]) => {
      options.value = data;
      isLoading.value = false;
    })
    .catch((error: unknown) => {
      // A newer request has replaced this one, and owns the loading state.
      if (error instanceof Error && error.name === "AbortError") {
        return;
      }
      isLoading.value = false;
      throw error;
    });
}

function clearAll() {
  selected.value = [];
}

function limitText(count: number) {
  return t("datasetValuesMultiselect.limitText", { n: count });
}

onMounted(() => {
  asyncFind("");
});
</script>

<style lang="scss">

.multiselect__tag-icon:after {
    content: "×";
    color: white;
    font-size: 16px;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
    background: $gray-800;
}

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
