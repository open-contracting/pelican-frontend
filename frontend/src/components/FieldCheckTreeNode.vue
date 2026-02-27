<template>
  <FieldCheckTableRow
    :key="path"
    :check="check"
    :show-stats="filter(data._check)"
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
      <div
        class="name flex-fill"
        :title="path"
        v-html="highlightSearchLast(path)"
      />
    </div>
  </FieldCheckTableRow>

  <template v-if="hasChildren">
    <template v-for="n in children" :key="n._path">
      <tree-node
        :data="n"
        :depth="depth + 1"
        :hide="!expanded"
      />
    </template>
  </template>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useStore } from "vuex";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import FieldCheckTableRow from "./FieldCheckTableRow.vue";

defineOptions({ name: "TreeNode" });

const props = defineProps({
    data: Object,
    expand: Boolean,
    depth: { type: Number, default: 0 },
    hide: { type: Boolean, default: false },
});

const store = useStore();
const { highlightSearchLast, isPathSearched } = useFieldCheckSearch();

function getChildren(node) {
    const result = { ...node };
    delete result._check;
    return result;
}

function isSearched(node) {
    return (isPathSearched(node._check.path) && filter.value(node._check)) || isSearchedSubTree(node);
}

function isSearchedSubTree(node) {
    return Object.values(getChildren(node)).some((n) => isSearched(n));
}

const check = computed(() => props.data._check);
const path = computed(() => props.data._check.path);
const filter = computed(() => store.getters.fieldLevelFilter);
const children = computed(() => getChildren(props.data));
const hasChildren = computed(() => Object.keys(children.value).length > 0);
const isExpandable = computed(() => hasChildren.value && isSearchedSubTree(props.data));
const expanded = computed({
    get: () => store.getters.isFieldCheckExpanded(path.value),
    set: (value) => {
        if (value) {
            store.commit("addFieldCheckExpandedNode", path.value);
        } else {
            store.commit("removeFieldCheckExpandedNode", path.value);
        }
    },
});

onMounted(() => {
    if (props.expand) {
        expanded.value = true;
    }
});
</script>

<style scoped lang="scss">
@import "@/scss/main";

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
