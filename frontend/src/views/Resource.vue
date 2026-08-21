<template>
  <dashboard>
    <h2>{{ $t("sections.resource") }}</h2>
    <div
      class="description"
      v-html="$t('resourceLevel.description')"
    />
    <span v-if="loaded">
      <BRow class="collection_header">
        <BCol class="text-start">
          <h4>{{ $t("resourceLevel.subheadline") }}</h4>
        </BCol>
        <BCol class="text-end">
          <FilterDropdown
            :filter-names="filterNames"
            :start-index="filterIndex"
            @newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
          />
        </BCol>
      </BRow>
      <div class="check_list_box">
        <table class="data_table">
          <thead>
            <tr>
              <th
                class="col-9 col-lg-5"
                scope="col"
              >{{ $t("resourceLevel.check") }}</th>
              <th
                class="col-1 text-end"
                scope="col"
              >{{ $t("resourceLevel.ok") }}</th>
              <th
                class="col-1 text-end"
                scope="col"
              >{{ $t("resourceLevel.failed") }}</th>
              <th
                class="col-1 text-end"
                scope="col"
              >{{ $t("resourceLevel.na") }}</th>
              <th
                class="col-4 d-none d-lg-table-cell"
                scope="col"
              />
            </tr>
          </thead>

          <tbody>
            <template
              v-for="(name, index) in RESOURCE_CHECK_SECTIONS"
              :key="index"
            >
              <ResourceLevelList
                :section="name"
                :filter="filters[filterIndex]"
              />
            </template>
          </tbody>
        </table>
      </div>
    </span>
    <span v-else>
      <Loader />
    </span>
  </dashboard>
</template>

<script setup lang="ts">
import { BCol, BRow } from "bootstrap-vue-next";
import { computed, onBeforeMount, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import FilterDropdown from "@/components/FilterDropdown.vue";
import Loader from "@/components/Loader.vue";
import ResourceLevelList from "@/components/ResourceLevelList.vue";
import { RESOURCE_CHECK_SECTIONS } from "@/config.js";
import { useDatasetStore } from "@/stores/dataset.js";
import { useUiStore } from "@/stores/ui.js";
import type { ResourceLevelCheck } from "@/types.js";
import Dashboard from "./layouts/Dashboard.vue";

const datasetStore = useDatasetStore();
const ui = useUiStore();
const { t } = useI18n();

const filterIndex = ref(0);

const filterNames = [
  t("resourceLevel.filterDropdown.all"),
  t("resourceLevel.filterDropdown.failedOnly"),
  t("resourceLevel.filterDropdown.passedOnly"),
  t("resourceLevel.filterDropdown.calculatedOnly"),
];

const filters: ((item: ResourceLevelCheck) => boolean)[] = [
  () => true,
  (item) => item.failed_count > 0,
  (item) => item.failed_count === 0 && item.passed_count > 0,
  (item) => item.passed_count > 0 || item.failed_count > 0,
];

const loaded = computed(() => datasetStore.resourceLevelStats != null);

watch(filterIndex, (newFilterIndex) => {
  ui.resourceLevelFilterIndex = newFilterIndex;
});

onBeforeMount(() => {
  filterIndex.value = ui.resourceLevelFilterIndex;
});
</script>
