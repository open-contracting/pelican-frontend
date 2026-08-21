<template>
  <table class="data_table">
    <thead>
      <tr>
        <th>
          <div class="d-flex align-items-center">
            <div>{{ $t("field.table.head.object") }}</div>
          </div>
        </th>
        <th>
          <div class="d-flex justify-content-center align-items-center">
            <span>{{ $t("field.table.head.coverage") }}</span>
          </div>
        </th>
        <th>
          <div class="d-flex justify-content-center align-items-center">
            <span>{{ $t("field.table.head.quality") }}</span>
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
import type { FieldLevelCheck, FieldCheckTreeNode as Node } from "@/types.js";
import FieldCheckTreeNode from "./FieldCheckTreeNode.vue";

const props = defineProps<{
  filter: (check: FieldLevelCheck) => boolean;
}>();
const datasetStore = useDatasetStore();
const ui = useUiStore();

const { search, sorted } = useFieldCheckSearch();

const stats = computed(() => datasetStore.fieldLevelStats);
const tree = computed(() => {
  const root: Node = { children: new Map() };

  // Insertion order determines the order in which the nodes render.
  for (const n of sorted(stats.value, "processingOrder")) {
    let node = root;
    for (const p of n.path.split(".")) {
      let child = node.children.get(p);
      if (!child) {
        child = { children: new Map() };
        node.children.set(p, child);
      }
      node = child;
    }

    node.check = n;
  }

  return root;
});

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

