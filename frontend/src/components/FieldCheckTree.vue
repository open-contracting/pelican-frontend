<template>
  <table class="data_table">
    <thead>
      <tr>
        <th>
          <div class="d-flex align-items-center">
            <div>{{ $t("field.path") }}</div>
          </div>
        </th>
        <th>
          <div class="d-flex justify-content-center align-items-center">
            <span>{{ $t("field.coverage") }}</span>
          </div>
        </th>
        <th>
          <div class="d-flex justify-content-center align-items-center">
            <span>{{ $t("field.quality") }}</span>
          </div>
        </th>
      </tr>
    </thead>

    <tbody>
      <FieldCheckTreeNode
        v-for="[segment, n] in tree.children"
        :key="segment"
        :data="n"
      />
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import { useDatasetStore } from "@/stores/dataset.js";
import { useUiStore } from "@/stores/ui.js";
import type { FieldLevelCheck } from "@/types.js";
import { fieldCheckTree } from "@/util.js";
import FieldCheckTreeNode from "./FieldCheckTreeNode.vue";

const props = defineProps<{
  filter: (check: FieldLevelCheck) => boolean;
}>();
const datasetStore = useDatasetStore();
const ui = useUiStore();

const { search, sorted } = useFieldCheckSearch();

const stats = computed(() => datasetStore.fieldLevelStats);
const tree = computed(() => fieldCheckTree(sorted(stats.value, "processingOrder")));

watch(search, () => {
  ui.setExpandedNodesForSearch(stats.value);
});

watch(
  () => props.filter,
  () => {
    ui.fieldLevelFilter = props.filter;
  },
);

onMounted(() => {
  if (search.value) {
    ui.setExpandedNodesForSearch(stats.value);
  }
});
</script>

