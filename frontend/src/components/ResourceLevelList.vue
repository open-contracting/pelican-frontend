<template>
    <span v-if="resourceLevelStats.length > 0">
        <div class="tr row clickable" v-on:click="showChecks = !showChecks">
            <div class="td col-4 col-lg-5 category" scope="col">
                <div class="switcher text-center" v-if="!showChecks">
                    <font-awesome-icon icon="chevron-right" />
                </div>
                <div class="switcher text-center" v-if="showChecks">
                    <font-awesome-icon icon="chevron-down" />
                </div>
                {{ $t("resourceLevel." + section + ".categoryName") }}
            </div>
            <div
                class="td col-8 col-lg-7 text-right text-lg-left info_message"
                scope="col"
            >{{ resourceLevelStats.length }} checks in total with avg score {{ avgScore }}%</div>
        </div>
        <span class="checks" v-if="showChecks">
            <ResourceLevelRow v-for="(value, name, index) in resourceLevelStats" :check="value" :name="value.name" v-bind:key="name" v-bind:index="index"></ResourceLevelRow>
        </span>
    </span>
</template>

<script>
import ResourceLevelRow from "@/components/ResourceLevelRow";

export default {
    data: function() {
        return {
            showChecks: false
        };
    },
    props: ["section"],
    components: { ResourceLevelRow },
    computed: {
        resourceLevelStats() {
            var result = this.$store.getters.resourceLevelStatsBySection(
                this.section
            );

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

            return result.sort(function(a, b) {
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

            return result;
        },
        avgScore() {
            var sum = 0;
            for (var item in this.resourceLevelStats) {
                var check = this.resourceLevelStats[item];
                sum =
                    sum +
                    check.passed_count /
                        ((check.passed_count +
                            check.failed_count +
                            check.undefined_count) /
                            100);
            }

            return Math.round(sum / this.resourceLevelStats.length);
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