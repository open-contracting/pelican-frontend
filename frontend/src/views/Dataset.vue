<template>
  <dashboard>
    <h2>{{ $t("sections.dataset") }}</h2>
    <div
      class="description"
      v-html="$t('datasetLevel.description')"
    />
    <BRow
      class="collection_header"
      align-h="between"
    >
      <BCol class="text-start">
        <h4>{{ $t("datasetLevel.subheadline") }}</h4>
      </BCol>
      <BCol class="text-end">
        <FilterDropdown
          :filter-names="filterNames"
          :start-index="filterIndex"
          @newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
        />
      </BCol>
    </BRow>
    <template v-for="(section, index) in sections" :key="index">
      <DatasetLevelSection
        :section="section"
        :filter="filters[filterIndex]"
      />
    </template>
  </dashboard>
</template>

<script setup lang="ts">
import { BCol, BRow } from "bootstrap-vue-next";
import { onBeforeMount, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import DatasetLevelSection from "@/components/DatasetLevelSection.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";
import { DATASET_CHECK_SECTIONS } from "@/config.js";
import { useUiStore } from "@/stores/ui.js";
import type { DatasetLevelCheck } from "@/types.js";
import Dashboard from "./layouts/Dashboard.vue";

const ui = useUiStore();
const { t } = useI18n();

const sections = Object.keys(DATASET_CHECK_SECTIONS);
const filterIndex = ref(0);

const filterNames = [
  t("filterDropdown.all"),
  t("filterDropdown.failedOnly"),
  t("filterDropdown.passedOnly"),
  t("filterDropdown.calculatedOnly"),
];

const filters: ((item: DatasetLevelCheck) => boolean)[] = [
  () => true,
  (item) => item.result === false,
  (item) => item.result === true,
  (item) => item.result != null,
];

watch(filterIndex, (newFilterIndex) => {
  ui.datasetLevelFilterIndex = newFilterIndex;
});

onBeforeMount(() => {
  filterIndex.value = ui.datasetLevelFilterIndex;
});
</script>
