<template>
    <dashboard>
        <h2>{{ $t("sections.time") }}</h2>
        <div class="description" v-html="$t('timeLevel.description')"></div>
        <b-row class="collection_header" align-h="between">
            <b-col class="text-left">
                <h4>{{ $t("timeLevel.subheadline") }}</h4>
            </b-col>
            <b-col class="text-right">
                <FilterDropdown
                    v-on:newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
                    :filterNames="filterNames"
                    :startIndex="filterIndex"
                />
            </b-col>
        </b-row>
        <div v-if="loaded" class="row row-cols-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3">
            <template v-for="(check, index) in timeVarianceLevelStats">
                <div class="col mb-4" v-bind:key="index">
                    <TimeVarianceLevelCheck :check="check"></TimeVarianceLevelCheck>
                </div>
            </template>
        </div>
        <Loader v-else />
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import TimeVarianceLevelCheck from "@/components/TimeVarianceLevelCheck";
import FilterDropdown from "@/components/FilterDropdown.vue";
import Loader from "@/components/Loader.vue";

export default {
    name: "timeLevel",
    data: function () {
        return {
            filterIndex: 0,
            filterNames: [
                this.$t("timeLevel.filterDropdown.all"),
                this.$t("timeLevel.filterDropdown.failedOnly"),
                this.$t("timeLevel.filterDropdown.passedOnly")
            ],
            filters: [
                () => true,
                item => item.coverage_result != true || item.check_result != true,
                item => item.coverage_result == true && item.check_result == true
            ]
        };
    },
    components: { Dashboard, TimeVarianceLevelCheck, FilterDropdown, Loader },
    created() {
        this.filterIndex = this.$store.getters.timeLevelFilterIndex;
    },
    computed: {
        loaded() {
            if (this.$store.getters.datasetLevelStats != null) {
                return true;
            }
            return false;
        },
        timeVarianceLevelStats() {
            return this.$store.getters.timeVarianceLevelStats.filter(this.filters[this.filterIndex]);
        }
    },
    methods: {
        detail: function (name) {
            this.$router.push({
                name: "timeVarianceCheckDetail",
                params: {
                    check: name,
                    datasetId: this.$store.getters.datasetId
                }
            });
        }
    },
    watch: {
        filterIndex: function (newFilterIndex) {
            this.$store.commit("setTimeLevelFilterIndex", newFilterIndex);
        }
    }
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
