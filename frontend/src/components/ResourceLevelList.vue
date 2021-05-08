<template>
    <span>
        <div class="tr row clickable" v-on:click="showChecks = !showChecks">
            <div class="td col-4 col-lg-5 category" scope="col">
                <div class="switcher text-center">
                    <span v-if="resourceLevelStats.length > 0">
                        <font-awesome-icon v-if="!showChecks" icon="chevron-right" />
                        <font-awesome-icon v-if="showChecks" icon="chevron-down" />
                    </span>
                </div>
                {{ $t("resourceLevel." + section + ".categoryName") }}
            </div>
            <div class="td col-8 col-lg-7 text-right text-lg-left info_message" scope="col">
                {{ resourceLevelStats.length }} {{ $t("resourceLevel.averageScore.description") }}:
                <span v-if="avgScore != null">
                    {{ avgScore | formatPercentage }}
                </span>
                <span v-else>
                    {{ $t("resourceLevel.averageScore.undefined") }}
                </span>
                <Tooltip :text="$t('resourceLevel.averageScore.tooltip')"></Tooltip>
            </div>
        </div>
        <span class="checks" v-if="showChecks">
            <ResourceLevelRow
                v-for="(value, name, index) in resourceLevelStats"
                :check="value"
                :name="value.name"
                v-bind:key="name"
                v-bind:index="index"
            ></ResourceLevelRow>
        </span>
    </span>
</template>

<script>
import ResourceLevelRow from "@/components/ResourceLevelRow";
import Tooltip from "@/components/Tooltip.vue";

export default {
    data: function () {
        return {
            showChecks: false
        };
    },
    props: ["section", "filter"],
    components: {
        ResourceLevelRow,
        Tooltip
    },
    computed: {
        resourceLevelStats() {
            var result = this.$store.getters.resourceLevelStatsBySection(this.section);

            var order = [
                "reference.buyer_in_parties",
                "reference.procuring_entity_in_parties",
                "reference.tenderer_in_parties",
                "reference.supplier_in_parties",
                "reference.payer_in_parties",
                "reference.payee_in_parties",
                "reference.contract_in_awards",
                "consistent.tender_value",
                "consistent.contracts_value",
                "consistent.contracts_implementation_transactions_value",
                "consistent.parties_roles",
                "consistent.period_duration_in_days",
                "consistent.number_of_tenderers",
                "consistent.buyer_in_parties_roles",
                "consistent.tenderer_in_parties_roles",
                "consistent.procuring_entity_in_parties_roles",
                "consistent.supplier_in_parties_roles",
                "consistent.payer_in_parties_roles",
                "consistent.payee_in_parties_roles",
                "consistent.buyer_name_in_parties",
                "consistent.tenderer_name_in_parties",
                "consistent.procuring_entity_name_in_parties",
                "consistent.supplier_name_in_parties",
                "consistent.payer_name_in_parties",
                "consistent.payee_name_in_parties",
                "coherent.tender_status",
                "coherent.awards_status",
                "coherent.contracts_status",
                "coherent.milestone_status",
                "coherent.dates",
                "coherent.milestones_dates",
                "coherent.amendments_dates",
                "coherent.documents_dates",
                "coherent.value_realistic",
                "coherent.period",
                "coherent.procurement_method_vs_number_of_tenderers"
            ];

            return result
                .sort(function (a, b) {
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
                })
                .filter(this.filter);
        },
        avgScore() {
            var passedCount = 0;
            var failedCount = 0;
            for (var i = 0; i < this.resourceLevelStats.length; i++) {
                passedCount += this.resourceLevelStats[i].passed_count;
                failedCount += this.resourceLevelStats[i].failed_count;
            }

            if (passedCount + failedCount == 0) {
                return null;
            }

            return (100.0 * passedCount) / (passedCount + failedCount);
        }
    },
    mounted() {
        this.showChecks = this.$store.getters.isResourceCheckExpanded(this.section);
    },
    watch: {
        showChecks: function (newShowChecks) {
            if (newShowChecks) {
                this.$store.commit("addResourceCheckExpandedNode", this.section);
            } else {
                this.$store.commit("removeResourceCheckExpandedNode", this.section);
            }
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.info_message {
    color: $na_color;
    font-weight: 300;
}

.switcher {
    display: inline-block;
    font-size: 80%;
    width: 30px;
    color: $primary;
}

.category {
    font-weight: 700;
}
</style>
