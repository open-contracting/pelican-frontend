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
        v-for="n in tree"
        :key="n._check.path"
        :data="n"
      />
    </tbody>
  </table>
</template>

<script setup>
import { computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import { useUiStore } from "@/stores/ui.js";
import FieldCheckTreeNode from "./FieldCheckTreeNode.vue";

const props = defineProps(["filter"]);
const store = useStore();
const ui = useUiStore();

const { search, sorted } = useFieldCheckSearch();

const stats = computed(() => store.getters.fieldLevelStats);
const tree = computed(() => {
  const root = {};

  // Insertion order determines the order in which the nodes render.
  for (const n of sorted(stats.value, "processingOrder")) {
    let node = root;
    for (const p of n.path.split(".")) {
      if (!(p in node)) {
        node[p] = {};
      }
      node = node[p];
    }

    node._check = n;
  }

  return root;
});

watch(search, () => {
  store.dispatch("setExpandedNodesForSearch");
});

watch(
  () => props.filter,
  () => {
    ui.fieldLevelFilter = props.filter;
  },
);

onMounted(() => {
  if (search.value) {
    store.dispatch("setExpandedNodesForSearch");
  }
});
</script>

