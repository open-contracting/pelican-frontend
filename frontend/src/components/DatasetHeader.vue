<template>
  <h1 v-if="dataset">
    <span class="name">{{ dataset.name }}</span>
    ({{ $t("dataset.id") }} {{ dataset.id }})
    | {{ $t("dataset.size") }} {{ formatNumber(dataset.meta.compiled_releases?.total_unique_ocids) }}
    | {{ $t("created") }} {{ dataset.meta.data_quality_tool_metadata?.processing_start }}
  </h1>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useFormatters } from "@/composables/useFormatters";
import { useDatasetStore } from "@/stores/dataset.js";

const datasetStore = useDatasetStore();
const { formatNumber } = useFormatters();

const dataset = computed(() => {
  if (datasetStore.dataset?.meta !== undefined) {
    return datasetStore.dataset;
  }
  return undefined;
});
</script>

<style scoped lang="scss">

h1 {
    font-size: 13px;
    font-family: $font-family-thin;
    margin-bottom: 40px;
    text-align: right;
    color: $headings_light_color;
}

.name {
    font-family: $font-family-sans-serif;
}
</style>
