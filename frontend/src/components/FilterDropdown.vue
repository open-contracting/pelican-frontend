<template>
  <b-dropdown
    id="filter_dropdown"
    right
    split
    split-button-type="button"
    :html="'<span id=\'show_prefix\'>Show: </span>' + filterNames[selectedIndex]"
    variant="primary"
  >
    <b-dropdown-item-button
      v-for="(name, index) in filterNames"
      :key="index"
      variant="bg-transparent border-transparent"
      @click="clickItem(index)"
    >
      {{ name }}
    </b-dropdown-item-button>
  </b-dropdown>
</template>

<script>
export default {
    props: {
        filterNames: Array,
        startIndex: {
            type: Number,
            default: 0
        }
    },
    data: function () {
        return {
            selectedIndex: 0
        };
    },
    mounted: function () {
        this.selectedIndex = this.startIndex;
        this.clickItem(this.startIndex);
    },
    methods: {
        clickItem: function (index) {
            this.selectedIndex = index;
            this.$emit("newSelectedIndex", index);
        }
    }
};
</script>

<style lang="scss">
@import "src/scss/variables";

#filter_dropdown {
    margin: 0.5rem;
    margin-left: 15px;
    margin-right: 0px;

    .dropdown-menu {
        padding: 0px;
        border-radius: 4px;
    }

    .btn-primary {
        border: none;
        background-color: transparent;
        color: $headings-color;
    }

    .btn-primary:first-of-type {
        pointer-events: none;
        padding-left: 0px;
        padding-right: 7px;
        padding-top: 7px;
        padding-bottom: 5px;
    }

    .dropdown-toggle {
        padding-top: 9px;
        padding-bottom: 3px;
    }

    .dropdown-toggle,
    .dropdown-item {
        border-radius: 4px;
        border: 1px solid transparent;
    }

    .dropdown-toggle:hover,
    .dropdown-toggle:active,
    .dropdown-toggle[aria-expanded="true"],
    .dropdown-item:hover {
        color: $primary;
        background-color: transparent;
        border-color: $primary;
    }

    .dropdown-toggle:focus,
    .dropdown-item:focus {
        box-shadow: none;
        outline: none;
    }
}

#show_prefix {
    color: $headings-light-color;
    font-family: $font-family-thin;
}
</style>
