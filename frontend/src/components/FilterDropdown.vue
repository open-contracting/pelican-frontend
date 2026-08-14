<template>
  <span class="filter_dropdown_group">
    <span id="show_prefix">Show:</span>
    <BDropdown
      id="filter_dropdown"
      class="filter_dropdown"
      placement="bottom-end"
      variant="primary"
    >
      <template #button-content>
        {{ filterNames[selectedIndex] }}
      </template>
      <BDropdownItemButton
        v-for="(name, index) in filterNames"
        :key="index"
        @click="clickItem(index)"
      >
        {{ name }}
      </BDropdownItemButton>
    </BDropdown>
  </span>
</template>

<script setup>
import { BDropdown, BDropdownItemButton } from "bootstrap-vue-next";
import { onMounted, ref } from "vue";

const props = defineProps({
    filterNames: Array,
    startIndex: { type: Number, default: 0 },
});

const emit = defineEmits(["newSelectedIndex"]);

const selectedIndex = ref(0);

function clickItem(index) {
    selectedIndex.value = index;
    emit("newSelectedIndex", index);
}

onMounted(() => {
    clickItem(props.startIndex);
});
</script>

<style lang="scss">
@import "@/scss/variables";

.filter_dropdown_group {
    display: inline-flex;
    align-items: center;
    margin-top: 8px;
    margin-bottom: 8px;
}

.filter_dropdown {
    // Bootstrap renders a block-level wrapper, unlike the .btn-group of a split dropdown.
    display: inline-flex;
}

#filter_dropdown {
    background-color: transparent;
    color: $headings-color;
    padding-left: 7px;
    padding-right: 7px;
    padding-top: 7px;
    padding-bottom: 5px;
    border-radius: 4px;
    border: 1px solid transparent;

    &:hover,
    &:active,
    &[aria-expanded="true"] {
        color: $primary;
        background-color: transparent;
        border-color: $primary;
    }
}

#filter_dropdown-menu {
    padding: 0px;
    border-radius: 4px;

    .dropdown-item {
        border-radius: 4px;
        border: 1px solid transparent;

        &:hover {
            color: $primary;
            background-color: transparent;
            border-color: $primary;
        }
    }
}

#show_prefix {
    color: $headings-light-color;
    font-family: $font-family-thin;
    margin-right: 4px;
}
</style>
