<template>
    <dashboard>
        <h2>{{ $t("sections.time") }}</h2>
        <h4>{{ $t("timeLevel.subheadline") }}</h4>
        <div class="row">
            <div v-for="(check, index) in timeVarianceLevelStats" v-bind:key="index" class="col col-12 col-sm-12 col-md-6 col-lg-6 col-xl-4">
                <TimeVarianceLevelCheck :check="check"></TimeVarianceLevelCheck>
            </div>
        </div>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import TimeVarianceLevelCheck from "@/components/TimeVarianceLevelCheck";

export default {
    name: "timeLevel",
    components: { Dashboard, TimeVarianceLevelCheck },
    computed: {
        timeVarianceLevelStats() {
            return this.$store.getters.timeVarianceLevelStats;
        }
    },
    methods: {
        detail: function(name) {
            this.$router.push({
                name: "timeVarianceCheckDetail",
                params: { check: name }
            });
        }
    }
};
</script>
