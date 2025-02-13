<template>
  <dashboard>
    <h2>{{ $t("sections.time") }}</h2>
    <div
      class="description"
      v-html="$t('timeLevel.description')"
    />
    <b-row
      class="collection_header"
      align-h="between"
    >
      <b-col class="text-left">
        <h4>{{ $t("timeLevel.subheadline") }}</h4>
      </b-col>
      <b-col class="text-right">
        <FilterDropdown
          :filter-names="filterNames"
          :start-index="filterIndex"
          @newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
        />
      </b-col>
    </b-row>
    <div
      v-if="loaded"
      class="row row-cols-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3"
    >
      <template v-for="(check, index) in timeVarianceLevelStats">
        <div
          :key="index"
          class="col mb-4"
        >
          <TimeVarianceLevelCheck :check="check" />
        </div>
      </template>
    </div>
    <Loader v-else />
  </dashboard>
</template>

<script>
import FilterDropdown from "@/components/FilterDropdown.vue";
import Loader from "@/components/Loader.vue";
import TimeVarianceLevelCheck from "@/components/TimeVarianceLevelCheck.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";

export default {
    name: "TimeLevel",
    components: { Dashboard, TimeVarianceLevelCheck, FilterDropdown, Loader },
    data: function () {
        return {
            filterIndex: 0,
            filterNames: [
                this.$t("timeLevel.filterDropdown.all"),
                this.$t("timeLevel.filterDropdown.failedOnly"),
                this.$t("timeLevel.filterDropdown.passedOnly"),
            ],
            filters: [
                () => true,
                (item) => item.coverage_result !== true || item.check_result !== true,
                (item) => item.coverage_result === true && item.check_result === true,
            ],
        };
    },
    computed: {
        loaded() {
            return this.$store.getters.datasetLevelStats != null;
        },
        timeVarianceLevelStats() {
            return this.$store.getters.timeVarianceLevelStats.filter(this.filters[this.filterIndex]);
        },
    },
    watch: {
        filterIndex: function (newFilterIndex) {
            this.$store.commit("setTimeLevelFilterIndex", newFilterIndex);
        },
    },
    created() {
        this.filterIndex = this.$store.getters.timeLevelFilterIndex;
    },
    methods: {
        detail: function (name) {
            this.$router.push({
                name: "timeVarianceCheckDetail",
                params: {
                    check: name,
                    datasetId: this.$store.getters.datasetId,
                },
            });
        },
    },
};
</script>

<style lang="scss">
@import "src/scss/main";

.collection_header {
    margin-bottom: 5px;

    h4 {
        position: absolute;
        bottom: 0px;
        margin-bottom: 5px;
    }
}
</style>
