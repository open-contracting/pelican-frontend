<template>
  <div class="table">
    <div class="thr row">
      <div class="th col col-4">
        <div class="d-flex align-items-center">
          <div>{{ $t("field.table.head.object") }}</div>
        </div>
      </div>
      <div
        class="th col col-4 justify-content-center d-flex"
        @click="sortByCoverage()"
      >
        <div class="d-flex align-items-center">
          <span>{{ $t("field.table.head.coverage") }}</span>
        </div>
      </div>
      <div
        class="th col col-4 justify-content-center d-flex"
        @click="sortByQuality()"
      >
        <div class="d-flex align-items-center">
          <span>{{ $t("field.table.head.quality") }}</span>
        </div>
      </div>
    </div>

    <FieldCheckTreeNode
      v-for="n in tree"
      :key="n._check.path"
      :data="n"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import FieldCheckTreeNode from "./FieldCheckTreeNode.vue";

const props = defineProps(["filter"]);
const store = useStore();

const { search, sortByProcessingOrder, sortByCoverage, sortByQuality } = useFieldCheckSearch();

const stats = computed(() => store.getters.fieldLevelStats);
const tree = computed(() => {
    const root = {};

    sortByProcessingOrder(stats.value);

    for (const n of stats.value) {
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
        store.commit("setFieldLevelFilter", props.filter);
    },
);

onMounted(() => {
    if (search.value) {
        store.dispatch("setExpandedNodesForSearch");
    }
});
</script>

<style scoped lang="scss">
@import "@/scss/main";

.table {
    thead {
        th {
            color: $headings_light_color;
            font-family: $headings-font-family;
        }
    }
}
</style>
