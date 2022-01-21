<template>
    <dashboard>
        <h2>{{ $t("sections.dataset") }}</h2>
        <div class="description" v-html="$t('datasetLevel.description')" />
        <b-row class="collection_header" align-h="between">
            <b-col class="text-left">
                <h4>{{ $t("datasetLevel.subheadline") }}</h4>
            </b-col>
            <b-col class="text-right">
                <FilterDropdown
                    :filter-names="filterNames"
                    :start-index="filterIndex"
                    @newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
                />
            </b-col>
        </b-row>
        <template v-for="(section, index) in sections">
            <DatasetLevelSection :key="index" :section="section" :filter="filters[filterIndex]" />
        </template>
    </dashboard>
</template>

<script>
// import Loader from "@/components/Loader.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";
import DatasetLevelSection from "@/components/DatasetLevelSection.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";

export default {
    name: "Dataset",
    components: { Dashboard, DatasetLevelSection, FilterDropdown },
    data: function () {
        return {
            sections: ["status_distribution", "value_distribution", "other_distribution", "repetition", "other"],
            filterIndex: 0,
            filterNames: [
                this.$t("datasetLevel.filterDropdown.all"),
                this.$t("datasetLevel.filterDropdown.failedOnly"),
                this.$t("datasetLevel.filterDropdown.passedOnly"),
                this.$t("datasetLevel.filterDropdown.calculatedOnly")
            ],
            filters: [
                () => true,
                item => item.result == false,
                item => item.result == true,
                item => item.result != null
            ]
        };
    },
    watch: {
        filterIndex: function (newFilterIndex) {
            this.$store.commit("setDatasetLevelFilterIndex", newFilterIndex);
        }
    },
    created() {
        this.filterIndex = this.$store.getters.datasetLevelFilterIndex;
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
