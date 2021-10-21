<template>
    <dashboard>
        <h2>{{ $t("sections.dataset") }}</h2>
        <div class="description" v-html="$t('datasetLevel.description')"></div>
        <b-row class="collection_header" align-h="between">
            <b-col class="text-left">
                <h4>{{ $t("datasetLevel.subheadline") }}</h4>
            </b-col>
            <b-col class="text-right">
                <FilterDropdown
                    v-on:newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
                    :filterNames="filterNames"
                    :startIndex="filterIndex"
                />
            </b-col>
        </b-row>
        <template v-for="(section, index) in sections">
            <DatasetLevelSection
                :section="section"
                :filter="filters[filterIndex]"
                v-bind:key="index"
            ></DatasetLevelSection>
        </template>
    </dashboard>
</template>

<script>
// import Loader from "@/components/Loader.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";
import DatasetLevelSection from "@/components/DatasetLevelSection.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";

export default {
    name: "dataset",
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
    created() {
        this.filterIndex = this.$store.getters.datasetLevelFilterIndex;
    },
    watch: {
        filterIndex: function (newFilterIndex) {
            this.$store.commit("setDatasetLevelFilterIndex", newFilterIndex);
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
