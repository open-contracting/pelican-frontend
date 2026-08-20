<template>
  <dashboard>
    <h2>{{ $t("sections.time") }}</h2>
    <div
      class="description"
      v-html="$t('timeLevel.description')"
    />
    <BRow
      class="collection_header"
      align-h="between"
    >
      <BCol class="text-start">
        <h4>{{ $t("timeLevel.subheadline") }}</h4>
      </BCol>
      <BCol class="text-end">
        <FilterDropdown
          :filter-names="filterNames"
          :start-index="filterIndex"
          @newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
        />
      </BCol>
    </BRow>
    <div
      v-if="loaded"
      class="row row-cols-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3"
    >
      <template v-for="(check, index) in timeVarianceLevelStats" :key="index">
        <div
          class="col mb-4"
        >
          <TimeVarianceLevelCheck :check="check" />
        </div>
      </template>
    </div>
    <Loader v-else />
  </dashboard>
</template>

<script setup>
import { BCol, BRow } from "bootstrap-vue-next";
import { computed, onBeforeMount, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import FilterDropdown from "@/components/FilterDropdown.vue";
import Loader from "@/components/Loader.vue";
import TimeVarianceLevelCheck from "@/components/TimeVarianceLevelCheck.vue";
import { useUiStore } from "@/stores/ui.js";
import Dashboard from "./layouts/Dashboard.vue";

const store = useStore();
const ui = useUiStore();
const { t } = useI18n();

const filterIndex = ref(0);

const filterNames = [
  t("timeLevel.filterDropdown.all"),
  t("timeLevel.filterDropdown.failedOnly"),
  t("timeLevel.filterDropdown.passedOnly"),
];

const filters = [
  () => true,
  (item) => item.coverage_result !== true || item.check_result !== true,
  (item) => item.coverage_result === true && item.check_result === true,
];

const loaded = computed(() => store.getters.datasetLevelStats != null);

const timeVarianceLevelStats = computed(() => {
  return store.getters.timeVarianceLevelStats.filter(filters[filterIndex.value]);
});

watch(filterIndex, (newFilterIndex) => {
  ui.timeLevelFilterIndex = newFilterIndex;
});

onBeforeMount(() => {
  filterIndex.value = ui.timeLevelFilterIndex;
});
</script>
