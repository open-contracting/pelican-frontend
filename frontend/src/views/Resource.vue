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
              >{{ $t("passed") }}</th>
              <th
                class="col-1 text-end"
                scope="col"
              >{{ $t("failed") }}</th>
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
                :filter="RESOURCE_LEVEL_FILTERS[filterIndex]"
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
import { RESOURCE_LEVEL_FILTERS } from "@/filters.js";
import { useDatasetStore } from "@/stores/dataset.js";
import { useUiStore } from "@/stores/ui.js";
import type { ResourceLevelCheck } from "@/types.js";
import Dashboard from "./layouts/Dashboard.vue";

const datasetStore = useDatasetStore();
const ui = useUiStore();
const { t } = useI18n();

const filterIndex = ref(0);

const filterNames = computed(() => [
  t("filterDropdown.all"),
  t("filterDropdown.failedOnly"),
  t("filterDropdown.passedOnly"),
  t("filterDropdown.calculatedOnly"),
]);

const loaded = computed(() => datasetStore.resourceLevelStats != null);

watch(filterIndex, (newFilterIndex) => {
  ui.resourceLevelFilterIndex = newFilterIndex;
});

onBeforeMount(() => {
  filterIndex.value = ui.resourceLevelFilterIndex;
});
</script>
