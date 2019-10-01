<template>
    <dashboard>
        <h2>{{ $t("sections.dataset") }}</h2>
        <div class="description" v-html=" $t('datasetLevel.description')"></div>
        <span v-if="loaded">
            <h4>{{ $t("datasetLevel.subheadline") }}</h4>
            <div class="row">
                <div class="card-deck col-12">
                    <template v-for="(check, index) in datasetLevelStats">
                        <DatasetLevelCheck :check="check" v-bind:key="index"></DatasetLevelCheck>

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
            var data = this.$store.getters.datasetLevelStats;

            var order = [
                "distribution.tender_status",
                "distribution.awards_status",
                "distribution.contracts_status",
                "distribution.milestone_status",
                "distribution.tender_value",
                "distribution.awards_value",
                "distribution.contracts_value",
                "distribution.tender_value_repetition",
                "distribution.awards_value_repetition",
                "distribution.contracts_value_repetition",
                "distribution.value_currency",
                "distribution.main_procurement_category",
                "distribution.tender_procurement_method",
                "distribution.tender_submission_method",
                "distribution.tender_award_criteria",
                "misc.url_availability",
                "distribution.buyer",
                "distribution.buyer_repetition",
                "distribution.document_document_type",
                "distribution.milestone_type",
                "distribution.related_process_relation",
                "consistent.related_process_title",
                "reference.related_process_identifier"
            ];
            return data.sort(function(a, b) {
                var nameA = a["name"];
                var nameB = b["name"];
                if (order.indexOf(nameA) < 0 && order.indexOf(nameB) < 0) {
                    if (nameA < nameB) {
                        return -1;
                    }

                    return 1;
                } else if (order.indexOf(nameA) < 0) {
                    return 1;
                } else if (order.indexOf(nameB) < 0) {
                    return -1;
                }

                return order.indexOf(nameA) - order.indexOf(nameB);
            });
        }
    }
};
</script>
