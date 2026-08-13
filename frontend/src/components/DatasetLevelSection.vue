<template>
  <span v-if="loaded">
    <h4 v-if="datasetLevelStats.length > 0">{{ $t("datasetLevel.sections." + section) }}</h4>
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3">
      <template v-for="(check, index) in datasetLevelStats" :key="section + index">
        <div
          class="col mb-4"
        >
          <DatasetLevelCheck
            :check="check"
          />
        </div>
      </template>
    </div>
  </span>
  <span v-else>
    <Loader />
  </span>
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import DatasetLevelCheck from "./DatasetLevelCheck.vue";
import Loader from "./Loader.vue";

const props = defineProps(["section", "filter"]);

const store = useStore();

const sections = {
    status_distribution: [
        "distribution.tender_status",
        "distribution.awards_status",
        "distribution.contracts_status",
        "distribution.milestone_status",
    ],
    value_distribution: ["distribution.tender_value", "distribution.awards_value", "distribution.contracts_value"],
    other_distribution: [
        "distribution.value_currency",
        "distribution.main_procurement_category",
        "distribution.tender_procurement_method",
        "distribution.tender_submission_method",
        "distribution.tender_award_criteria",
        "distribution.buyer",
        "distribution.document_document_type",
        "distribution.milestone_type",
        "distribution.related_process_relation",
    ],
    repetition: [
        "distribution.tender_value_repetition",
        "distribution.awards_value_repetition",
        "distribution.contracts_value_repetition",
        "distribution.buyer_repetition",
    ],
    other: [
        "misc.url_availability",
        "consistent.related_process_title",
        "reference.related_process_identifier",
        "unique.tender_id",
    ],
};

const loaded = computed(() => store.getters.datasetLevelStats != null);

const datasetLevelStats = computed(() => {
    if (!(props.section in sections)) {
        return [];
    }
    return sections[props.section].map((item) => store.getters.datasetLevelCheckByName(item)).filter(props.filter);
});
</script>
