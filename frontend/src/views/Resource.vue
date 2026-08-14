<template>
  <dashboard>
    <h2>{{ $t("sections.resource") }}</h2>
    <div
      class="description"
      v-html="$t('resourceLevel.description')"
    />
    <span v-if="loaded">
      <BRow class="action_bar">
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
      <div class="resource_result_box">
        <div class="thr row">
          <div
            class="th col-9 col-lg-5"
            scope="col"
          >{{ $t("resourceLevel.check") }}</div>
          <div
            class="th col-1 text-end"
            scope="col"
          >{{ $t("resourceLevel.ok") }}</div>
          <div
            class="th col-1 text-end"
            scope="col"
          >{{ $t("resourceLevel.failed") }}</div>
          <div
            class="th col-1 text-end"
            scope="col"
          >{{ $t("resourceLevel.na") }}</div>
          <div
            class="th col-4 d-none d-lg-block"
            scope="col"
          >&nbsp;</div>
        </div>
        <span
          v-for="(name, index) in RESOURCE_CHECK_SECTIONS"
          :key="index"
        >
          <ResourceLevelList
            :section="name"
            :filter="filters[filterIndex]"
          />
        </span>
      </div>
    </span>
    <span v-else>
      <Loader />
    </span>
  </dashboard>
</template>

<script setup>
import { BCol, BRow } from "bootstrap-vue-next";
import { computed, onBeforeMount, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import FilterDropdown from "@/components/FilterDropdown.vue";
import Loader from "@/components/Loader.vue";
import ResourceLevelList from "@/components/ResourceLevelList.vue";
import { RESOURCE_CHECK_SECTIONS } from "@/config.js";
import Dashboard from "./layouts/Dashboard.vue";

const store = useStore();
const { t } = useI18n();

const filterIndex = ref(0);

const filterNames = [
    t("resourceLevel.filterDropdown.all"),
    t("resourceLevel.filterDropdown.failedOnly"),
    t("resourceLevel.filterDropdown.passedOnly"),
    t("resourceLevel.filterDropdown.calculatedOnly"),
];

const filters = [
    () => true,
    (item) => item.failed_count > 0,
    (item) => item.failed_count === 0 && item.passed_count > 0,
    (item) => item.passed_count > 0 || item.failed_count > 0,
];

const loaded = computed(() => store.getters.resourceLevelStats != null);

watch(filterIndex, (newFilterIndex) => {
    store.commit("setResourceLevelFilterIndex", newFilterIndex);
});

onBeforeMount(() => {
    filterIndex.value = store.getters.resourceLevelFilterIndex;
});
</script>

<style lang="scss">
.action_bar {
    margin-bottom: 5px;
    position: relative;

    h4 {
        position: absolute;
        bottom: 0px;
        margin-bottom: 5px;
    }
}

.resource_result_box {
    background-color: white;
    border-radius: 10px;
    padding: 40px;
    box-shadow: 0 2px 18px 6px rgba(0, 0, 0, 0.06);
    border: 0;
}
</style>
