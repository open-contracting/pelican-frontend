<template>
    <b-dropdown
        right
        split
        split-button-type="button"
        :html="'<span id=\'show_prefix\'>Show: </span>' + filterNames[selectedIndex]"
        variant="primary"
        id="filter_dropdown"
    >
        <b-dropdown-item-button
            variant="bg-transparent border-transparent"
            v-for="(name, index) in filterNames"
            v-bind:key="index"
            v-on:click="clickItem(index)"
        >
        {{ name }}
        </b-dropdown-item-button>
    </b-dropdown>
</template>

<script>

export default {
    data: function() {
        return {
            selectedIndex: 0
        }
    },
    props: {
        filterNames: Array,
        startIndex: {
            type: Number,
            default: 0
        }
    },
    mounted: function() {
        this.selectedIndex = this.startIndex;
        this.clickItem(this.startIndex);
    },
    methods: {
        clickItem: function(index) {
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
    
    .btn-primary {
        border: none;
        background-color: transparent;
        color: $headings-color;
    }

    .btn-primary:first-of-type {
        pointer-events: none;
        padding-left: 0px;
        padding-right: 5px;
        padding-top: 7px;
        padding-bottom: 5px;
    }

    .dropdown-toggle {
        padding-top: 9px;
        padding-bottom: 3px;

        &:hover, &:active, &:focus {
            color: white;
            background-color: $primary;
        }
    }

    .dropdown-toggle[aria-expanded="true"] {
        color: white;
        background-color: $primary;
    }

    .dropdown-item {
        &:hover, &:active, &:focus {
            color: white;
            background-color: $primary;
            border: none;
        }
    }
}

#show_prefix {
    color: $headings-light-color;
    font-family: $font-family-thin;
}

</style>