<template>
    <dashboard>
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.dataset") }}</h2>
        <span v-if="loaded">
            <h4>{{ $t("datasetLevel.subheadline") }}</h4>
            <div class="row">
                <div v-for="(check, index) in datasetLevelStats" v-bind:key="index" class="col col-12 col-sm-12 col-md-6 col-lg-6 col-xl-4">
                    <DatasetLevelCheck :check="check"></DatasetLevelCheck>
                </div>
            </div>
        </span>
        <span v-else>
            <Loader></Loader>
        </span>
    </dashboard>
</template>

<script>
import Loader from "@/components/Loader.vue";
import DatasetLevelCheck from "@/components/DatasetLevelCheck.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";

export default {
    name: "dataset",
    components: { Loader, DatasetLevelCheck, Dashboard },
    computed: {
        loaded() {
            if (this.$store.getters.datasetLevelStats != null) {
                return true;
            }
            return false;
        },
        datasetLevelStats() {
            return this.$store.getters.datasetLevelStats;
        }
    }
};
</script>
