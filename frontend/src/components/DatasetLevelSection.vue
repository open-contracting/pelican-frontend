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
import { DATASET_CHECK_SECTIONS } from "@/config.js";
import DatasetLevelCheck from "./DatasetLevelCheck.vue";
import Loader from "./Loader.vue";

const props = defineProps(["section", "filter"]);

const store = useStore();

const loaded = computed(() => store.getters.datasetLevelStats != null);

const datasetLevelStats = computed(() => {
    if (!(props.section in DATASET_CHECK_SECTIONS)) {
        return [];
    }
    return DATASET_CHECK_SECTIONS[props.section]
        .map((item) => store.getters.datasetLevelCheckByName(item))
        .filter(props.filter);
});
</script>
