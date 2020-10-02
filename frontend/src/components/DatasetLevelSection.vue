<template>
    <span v-if="loaded">
        <h4 v-if="datasetLevelStats.length > 0">{{ $t("datasetLevel.sections." + section) }}</h4>
        <div class="row">
            <div class="card-deck col-12">
                <template v-for="(check, index) in datasetLevelStats">
                    <DatasetLevelCheck :check="check" v-bind:key="index"></DatasetLevelCheck>

                    <div class="w-100 d-none d-sm-block d-md-none" v-bind:key="'sm' + index">
                        <!-- wrap every 1-->
                    </div>

                    <div v-if="(index + 1) % 2 == 0" class="w-100 d-none d-md-block d-lg-none" v-bind:key="'md' + index">
                        <!-- wrap every 2-->
                    </div>
                    <div v-if="(index + 1) % 2 == 0" class="w-100 d-none d-lg-block d-xl-none" v-bind:key="'lg' + index">
                        <!-- wrap every 2-->
                    </div>

                    <div v-if="(index + 1) % 3 == 0" class="w-100 d-none d-xl-block" v-bind:key="'xl' + index">
                        <!-- wrap every 3-->
                    </div>
                </template>
            </div>
        </div>
    </span>
    <span v-else>
        <Loader></Loader>
    </span>
</template>

<script>
import DatasetLevelCheck from "@/components/DatasetLevelCheck.vue";

export default {
    data: function() {
        return {
            sections: {
                status_distribution: [
                    "distribution.tender_status",
                    "distribution.awards_status",
                    "distribution.contracts_status",
                    "distribution.milestone_status"
                ],
                value_distribution: [
                    "distribution.tender_value",
                    "distribution.awards_value",
                    "distribution.contracts_value"
                ],
                other_distribution: [
                    "distribution.value_currency",
                    "distribution.main_procurement_category",
                    "distribution.tender_procurement_method",
                    "distribution.tender_submission_method",
                    "distribution.tender_award_criteria",
                    "distribution.buyer",
                    "distribution.document_document_type",
                    "distribution.milestone_type",
                    "distribution.related_process_relation"
                ],
                repetition: [
                    "distribution.tender_value_repetition",
                    "distribution.awards_value_repetition",
                    "distribution.contracts_value_repetition",
                    "distribution.buyer_repetition"
                ],
                other: [
                    "misc.url_availability",
                    "consistent.related_process_title",
                    "reference.related_process_identifier",
                    "unique.tender_id"
                ]
            }
        };
    },
    props: ["section", "filter"],
    components: { DatasetLevelCheck },
    computed: {
        loaded() {
            if (this.$store.getters.datasetLevelStats != null) {
                return true;
            }
            return false;
        },
        datasetLevelStats() {
            if (!(this.section in this.sections)) {
                return [];
            } else {
                return this.sections[this.section]
                    .map(item =>
                        this.$store.getters.datasetLevelCheckByName(item)
                    )
                    .filter(this.filter);
            }
        }
    }
};
</script>