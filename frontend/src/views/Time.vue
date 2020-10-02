<template>
    <dashboard>
        <h2>{{ $t("sections.time") }}</h2>
        <div class="description" v-html=" $t('timeLevel.description')"></div>
        <h4>{{ $t("timeLevel.subheadline") }}</h4>
        <FilterDropdown
            v-on:newSelectedIndex="newSelectedIndex => filterIndex = newSelectedIndex"
            :filterNames="filterNames"
            :startIndex="filterIndex"
        />
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
                    <div v-if="(index + 1) % 3 == 0" class="w-100 d-none d-lg-block d-xl-none" v-bind:key="'lg' + index">
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
import FilterDropdown from "@/components/FilterDropdown.vue";

export default {
    name: "timeLevel",
    data: function() {
        return {
            filterIndex: 0,
            filterNames: [
                this.$t("timeLevel.filterDropdown.all"),
                this.$t("timeLevel.filterDropdown.failedOnly"),
                this.$t("timeLevel.filterDropdown.passedOnly"),
            ],
            filters: [
                () => true,
                item => item.coverage_result == false,
                item => item.coverage_result == true,
            ]
        }
    },
    components: { Dashboard, TimeVarianceLevelCheck, FilterDropdown },
    created() {
        this.filterIndex = this.$store.getters.timeLevelFilterIndex;
    },
    computed: {
        timeVarianceLevelStats() {
            return this.$store.getters.timeVarianceLevelStats.filter(this.filters[this.filterIndex]);
        }
    },
    methods: {
        detail: function(name) {
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
