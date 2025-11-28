<template>
  <fragment>
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
            <font-awesome-icon
              v-if="!expanded"
              icon="chevron-right"
            />
            <font-awesome-icon
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
      <template v-for="n in children">
        <tree-node
          :key="n._path"
          :data="n"
          :depth="depth + 1"
          :hide="!expanded"
        />
      </template>
    </template>
  </fragment>
</template>

<script>
import FieldCheckTableRow from "@/components/FieldCheckTableRow.vue";
import fieldCheckMixins from "@/plugins/fieldCheckMixins.js";
import { Fragment } from "vue-fragment";

export default {
    name: "TreeNode",
    components: { FieldCheckTableRow, Fragment },
    mixins: [fieldCheckMixins],
    props: {
        data: Object,
        expand: Boolean,
        depth: { type: Number, default: 0 },
        hide: { type: Boolean, default: false },
    },
    data: () => ({}),
    computed: {
        children: function () {
            return this.getChildren(this.data);
        },
        isExpandable: function () {
            return this.hasChildren && this.isSearchedSubTree(this.data);
        },
        hasChildren: function () {
            return Object.keys(this.children).length > 0;
        },
        expanded: {
            get: function () {
                return this.$store.getters.isFieldCheckExpanded(this.path);
            },
            set: function (value) {
                if (value) {
                    this.$store.commit("addFieldCheckExpandedNode", this.path);
                } else {
                    this.$store.commit("removeFieldCheckExpandedNode", this.path);
                }
            },
        },
        path: function () {
            return this.data._check.path;
        },
        check: function () {
            return this.data._check;
        },
        filter: function () {
            return this.$store.getters.fieldLevelFilter;
        },
    },
    mounted: function () {
        if (this.expand) {
            this.expanded = true;
        }
    },
    methods: {
        isSearched: function (node) {
            return (this.isPathSearched(node._check.path) && this.filter(node._check)) || this.isSearchedSubTree(node);
        },
        isSearchedSubTree: function (node) {
            return Object.values(this.getChildren(node)).some((n) => this.isSearched(n));
        },
        getChildren: (node) => {
            const result = Object.assign({}, node);
            delete result._check;
            return result;
        },
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

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
