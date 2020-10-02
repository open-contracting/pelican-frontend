<template>
    <span v-if="loaded">
        <h4 v-if="datasetLevelStats.length > 0">{{ $t("datasetLevel.sections." + section) }}</h4>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3">
            <!-- <div class="card-deck col-12"> -->
                <template v-for="(check, index) in datasetLevelStats">
                    <div class="col mb-4" v-bind:key="section + index">
                        <DatasetLevelCheck :check="check" v-bind:key="section + index"></DatasetLevelCheck>
                    </div>
                </template>
            <!-- </div> -->
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