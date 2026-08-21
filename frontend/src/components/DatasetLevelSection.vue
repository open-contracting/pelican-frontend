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

<script setup lang="ts">
import { computed } from "vue";
import { DATASET_CHECK_SECTIONS } from "@/config.js";
import { useDatasetStore } from "@/stores/dataset.js";
import type { DatasetLevelCheck as Check } from "@/types.js";
import DatasetLevelCheck from "./DatasetLevelCheck.vue";
import Loader from "./Loader.vue";

const props = defineProps<{
  section: string;
  filter: (check: Check) => boolean;
}>();

const datasetStore = useDatasetStore();

const loaded = computed(() => datasetStore.datasetLevelStats != null);

const datasetLevelStats = computed(() => {
  const names = DATASET_CHECK_SECTIONS[props.section];

  if (!names) {
    return [];
  }

  return names
    .map((item) => datasetStore.datasetLevelCheckByName(item))
    .filter((check) => check != null)
    .filter(props.filter);
});
</script>
