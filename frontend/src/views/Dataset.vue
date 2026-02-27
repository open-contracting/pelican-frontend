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

<script>
import { BCol, BRow } from "bootstrap-vue-next";
import DatasetLevelSection from "@/components/DatasetLevelSection.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";
import Dashboard from "./layouts/Dashboard.vue";

export default {
    name: "Dataset",
    components: { BCol, BRow, Dashboard, DatasetLevelSection, FilterDropdown },
    data: function () {
        return {
            sections: ["status_distribution", "value_distribution", "other_distribution", "repetition", "other"],
            filterIndex: 0,
            filterNames: [
                this.$t("datasetLevel.filterDropdown.all"),
                this.$t("datasetLevel.filterDropdown.failedOnly"),
                this.$t("datasetLevel.filterDropdown.passedOnly"),
                this.$t("datasetLevel.filterDropdown.calculatedOnly"),
            ],
            filters: [
                () => true,
                (item) => item.result === false,
                (item) => item.result === true,
                (item) => item.result != null,
            ],
        };
    },
    watch: {
        filterIndex: function (newFilterIndex) {
            this.$store.commit("setDatasetLevelFilterIndex", newFilterIndex);
        },
    },
    created() {
        this.filterIndex = this.$store.getters.datasetLevelFilterIndex;
    },
};
</script>

<style lang="scss">
@import "@/scss/main";

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
