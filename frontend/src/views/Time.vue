<template>
    <dashboard>
        <h2>{{ $t("sections.time") }}</h2>
        <h4>{{ $t("timeLevel.subheadline") }}</h4>
        <div class="row">
            <div class="card-deck col-12">
                <template v-for="(check, index) in timeVarianceLevelStats">
                    <TimeVarianceLevelCheck v-bind:key="index" :check="check"></TimeVarianceLevelCheck>

                    <div class="w-100 d-none d-sm-block d-md-none" v-bind:key="'sm' + index">
                        <!-- wrap every 2-->
                    </div>

                    <div v-if="(index + 1) % 2 == 0" class="w-100 d-none d-md-block d-lg-none" v-bind:key="'md' + index">
                        <!-- wrap every 2-->
                    </div>
                    <div v-if="(index + 1) % 2 == 0" class="w-100 d-none d-lg-block d-xl-none" v-bind:key="'lg' + index">
                        <!-- wrap every 2-->
                    </div>

                    <div v-if="(index + 1) % 3 == 0" class="w-100 d-none d-xl-block" v-bind:key="'xl' + index">
                        <!-- wrap every 2-->
                    </div>
                </template>
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
