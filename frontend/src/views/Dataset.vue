<template>
    <main role="main" class="dataset main_content col-11 col-sm-10 col-md-9 col-lg-9 col-xl-10 offset-1 offset-sm-2 offset-md-3 offset-lg-3 offset-xl-2">
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.dataset") }}</h2>
        <span v-if="loaded">
            <h4>{{ $t("datasetLevel.subheadline") }}</h4>
            <div class="row">
                <div v-for="(check, index) in datasetLevelStats" v-bind:key="index" class="col col-12 col-sm-12 col-md-6 col-lg-4 col-xl-4">
                    <DatasetLevelCheck :check="check"></DatasetLevelCheck>
                </div>
            </div>
        </span>
        <span v-else>
            <Loader></Loader>
        </span>
    </main>
</template>

<script>
import Loader from "@/components/Loader.vue";
import DatasetLevelCheck from "@/components/DatasetLevelCheck.vue";
export default {
    name: "dataset",
    components: { Loader, DatasetLevelCheck },
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
