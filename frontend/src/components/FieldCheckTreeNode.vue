<template>
  <FieldCheckTableRow
    :key="path"
    v-slot="{ to }"
    :check="check"
    :show-stats="check != null && filter(check)"
    :class="{ hidden: hide || !isSearched(data) }"
  >
    <div class="d-flex flex-row align-items-center">
      <div :class="'indent-' + depth" />
      <div
        v-if="isExpandable"
        class="switcher text-center"
        @click.stop="expanded = !expanded"
      >
        <template v-if="isExpandable">
          <FontAwesomeIcon
            v-if="!expanded"
            icon="chevron-right"
          />
          <FontAwesomeIcon
            v-else
            icon="chevron-down"
          />
        </template>
      </div>
      <div
        v-else
        class="switcher"
      />
      <RouterLink
        class="check_link name flex-fill"
        :to="to"
        :title="path"
      ><MarkedText :segments="highlightSearchLast(path)" /></RouterLink>
    </div>
  </FieldCheckTableRow>

  <template v-for="[segment, n] in data.children" :key="segment">
    <tree-node
      :data="n"
      :depth="depth + 1"
      :hide="!expanded"
    />
  </template>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import { useUiStore } from "@/stores/ui.js";
import type { FieldCheckTreeNode as Node } from "@/types.js";
import FieldCheckTableRow from "./FieldCheckTableRow.vue";
import MarkedText from "./MarkedText.vue";

defineOptions({ name: "TreeNode" });

const props = withDefaults(
  defineProps<{
    data: Node;
    depth?: number;
    hide?: boolean;
  }>(),
  { depth: 0, hide: false },
);

const ui = useUiStore();
const { highlightSearchLast, isPathSearched } = useFieldCheckSearch();

function isSearched(node: Node): boolean {
  return (
    (node.check != null && isPathSearched(node.check.path) && filter.value(node.check)) || isSearchedSubTree(node)
  );
}

function isSearchedSubTree(node: Node) {
  return [...node.children.values()].some((n) => isSearched(n));
}

const check = computed(() => props.data.check);
const path = computed(() => props.data.check?.path ?? "");
const filter = computed(() => ui.fieldLevelFilter);
const isExpandable = computed(() => props.data.children.size > 0 && isSearchedSubTree(props.data));
const expanded = computed({
  get: () => ui.isFieldCheckExpanded(path.value),
  set: (value) => {
    if (value) {
      ui.expandFieldCheck(path.value);
    } else {
      ui.collapseFieldCheck(path.value);
    }
  },
});
</script>

<style scoped lang="scss">

$indent-width-px: 35px;

@function indent-with($depth) {
    @return ($depth * $indent-width-px);
}

.switcher {
    display: inline-block;
    font-size: 80%;
    width: 30px;
    color: $primary;
    position: relative;
}

.name {
    display: inline-block;
}

.node_data {
    td {
        border-top: none;
    }
}

div[class^="indent-"] {
    display: inline-block;
}

@for $depth from 0 to 10 {
    .indent-#{$depth} {
        width: indent-with($depth);
    }
}

.hidden {
    display: none !important;
}
</style>
