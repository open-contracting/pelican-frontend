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

<script setup>
import { BCol, BRow } from "bootstrap-vue-next";
import { onBeforeMount, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import DatasetLevelSection from "@/components/DatasetLevelSection.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";
import { DATASET_CHECK_SECTIONS } from "@/config.js";
import Dashboard from "./layouts/Dashboard.vue";

const store = useStore();
const { t } = useI18n();

const sections = Object.keys(DATASET_CHECK_SECTIONS);
const filterIndex = ref(0);

const filterNames = [
    t("datasetLevel.filterDropdown.all"),
    t("datasetLevel.filterDropdown.failedOnly"),
    t("datasetLevel.filterDropdown.passedOnly"),
    t("datasetLevel.filterDropdown.calculatedOnly"),
];

const filters = [
    () => true,
    (item) => item.result === false,
    (item) => item.result === true,
    (item) => item.result != null,
];

watch(filterIndex, (newFilterIndex) => {
    store.commit("setDatasetLevelFilterIndex", newFilterIndex);
});

onBeforeMount(() => {
    filterIndex.value = store.getters.datasetLevelFilterIndex;
});
</script>

<style lang="scss">

.collection_header {
    margin-bottom: 5px;
    position: relative;

    h4 {
        position: absolute;
        bottom: 0px;
        margin-bottom: 5px;
    }
}
</style>
