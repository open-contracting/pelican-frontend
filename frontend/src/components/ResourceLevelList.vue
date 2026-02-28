<template>
  <span>
    <div
      class="tr row clickable"
      @click="showChecks = !showChecks"
    >
      <div
        class="td col-4 col-lg-5 category"
        scope="col"
      >
        <div class="switcher text-center">
          <span v-if="resourceLevelStats.length > 0">
            <FontAwesomeIcon
              v-if="!showChecks"
              icon="chevron-right"
            />
            <FontAwesomeIcon
              v-if="showChecks"
              icon="chevron-down"
            />
          </span>
        </div>
        {{ $t("resourceLevel." + section + ".categoryName") }}
      </div>
      <div
        class="td col-8 col-lg-7 text-end text-lg-start info_message"
        scope="col"
      >
        {{ $t("resourceLevel.averageScore.description", { applicable: applicableChecks, total: resourceLevelStats.length, average_score: formattedAvgScore }) }}
        <Tooltip :text="$t('resourceLevel.averageScore.tooltip')" />
      </div>
    </div>
    <span
      v-if="showChecks"
      class="checks"
    >
      <ResourceLevelRow
        v-for="(value, name, index) in resourceLevelStats"
        :key="name"
        :check="value"
        :name="value.name"
        :index="index"
      />
    </span>
  </span>
</template>

<script>
import { useFormatters } from "@/composables/useFormatters";
import ResourceLevelRow from "./ResourceLevelRow.vue";
import Tooltip from "./Tooltip.vue";

export default {
    components: {
        ResourceLevelRow,
        Tooltip,
    },
    props: ["section", "filter"],
    setup() {
        const { formatPercentage } = useFormatters();
        return { formatPercentage };
    },
    data: () => ({
        showChecks: false,
    }),
    computed: {
        resourceLevelStats() {
            const result = this.$store.getters.resourceLevelStatsBySection(this.section);

            const order = [
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
                "coherent.release_date",
                "coherent.milestones_dates",
                "coherent.amendments_dates",
                "coherent.documents_dates",
                "coherent.value_realistic",
                "coherent.period",
                "coherent.procurement_method_vs_number_of_tenderers",
            ];

            return result
                .sort((a, b) => {
                    const nameA = a.name;
                    const nameB = b.name;
                    if (order.indexOf(nameA) < 0 && order.indexOf(nameB) < 0) {
                        if (nameA < nameB) {
                            return -1;
                        }

                        return 1;
                    }
                    if (order.indexOf(nameA) < 0) {
                        return 1;
                    }
                    if (order.indexOf(nameB) < 0) {
                        return -1;
                    }

                    return order.indexOf(nameA) - order.indexOf(nameB);
                })
                .filter(this.filter);
        },
        applicableChecks() {
            let applicableCount = 0;
            for (const check of this.resourceLevelStats) {
                if (check.undefined_count < check.total_count) {
                    applicableCount += 1;
                }
            }
            return applicableCount;
        },
        formattedAvgScore() {
            let passedCount = 0;
            let failedCount = 0;
            for (const check of this.resourceLevelStats) {
                passedCount += check.passed_count;
                failedCount += check.failed_count;
            }

            if (passedCount + failedCount === 0) {
                return this.$t("resourceLevel.averageScore.undefined");
            }

            return this.formatPercentage(passedCount / (passedCount + failedCount));
        },
    },
    watch: {
        showChecks: function (newShowChecks) {
            if (newShowChecks) {
                this.$store.commit("addResourceCheckExpandedNode", this.section);
            } else {
                this.$store.commit("removeResourceCheckExpandedNode", this.section);
            }
        },
    },
    mounted() {
        this.showChecks = this.$store.getters.isResourceCheckExpanded(this.section);
    },
};
</script>

<style scoped lang="scss">
@import "@/scss/variables";

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
