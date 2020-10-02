<template>
    <dashboard>
        <h2>{{ $t("sections.resource") }}</h2>
        <div class="description" v-html=" $t('resourceLevel.description')"></div>
        <span v-if="loaded">
            <b-row class="action_bar">
                <b-col class="text-left">
                    <h4>{{ $t("resourceLevel.subheadline") }}</h4>
                </b-col>
                <b-col class="text-right">
                    <FilterDropdown
                        v-on:newSelectedIndex="newSelectedIndex => filterIndex = newSelectedIndex"
                        :filterNames="filterNames"
                        :startIndex="filterIndex"
                    />
                </b-col>
            </b-row>
            <div class="resource_result_box">
                <div class="thr row">
                    <div class="th col-9 col-lg-5" scope="col">{{ $t("resourceLevel.check") }}</div>
                    <div class="th col-1 text-right" scope="col">{{ $t("resourceLevel.ok") }}</div>
                    <div class="th col-1 text-right" scope="col">{{ $t("resourceLevel.failed") }}</div>
                    <div class="th col-1 text-right" scope="col">{{ $t("resourceLevel.na") }}</div>
                    <div class="th col-4 d-none d-lg-block" scope="col">&nbsp;</div>
                </div>
                <span v-for="(name, index) in sections" v-bind:key="index">
                    <ResourceLevelList :section="name" :filter="filters[filterIndex]" />
                </span>
            </div>
        </span>
        <span v-else>
            <Loader></Loader>
        </span>
    </dashboard>
</template>

<script>
import ResourceLevelList from "@/components/ResourceLevelList.vue";
import Loader from "@/components/Loader.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";

export default {
    name: "resource",
    data: function() {
        return {
            sections: ["reference", "consistent", "coherent"],
            filterIndex: 0,
            filterNames: [
                this.$t("resourceLevel.filterDropdown.all"),
                this.$t("resourceLevel.filterDropdown.failedOnly"),
                this.$t("resourceLevel.filterDropdown.passedOnly"),
                this.$t("resourceLevel.filterDropdown.calculatedOnly"),
            ],
            filters: [
                () => true,
                item => item.failed_count > 0,
                item => item.failed_count == 0 && item.passed_count > 0,
                item => item.passed_count > 0 || item.failed_count > 0,
            ]
        };
    },
    components: {
        ResourceLevelList,
        Loader,
        FilterDropdown,
        Dashboard
    },
    created() {
        this.filterIndex = this.$store.getters.resourceLevelFilterIndex;
    },
    computed: {
        loaded() {
            if (this.$store.getters.resourceLevelStats != null) {
                return true;
            }
            return false;
        }
    },
    watch: {
        filterIndex: function (newFilterIndex) {
            this.$store.commit("setResourceLevelFilterIndex", newFilterIndex);
        }
    }
};
</script>

<style lang="scss">

.action_bar {
    margin-bottom: 5px;

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