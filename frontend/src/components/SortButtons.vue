<template>
    <div class="d-flex align-items-center">
        <div><slot>{{ label }}</slot></div>
        <div class="sort_buttons">
            <div :class="['asc', {active: active && asc}]" @click.stop="onAsc()"></div>
            <div :class="['desc', {active: active && !asc}]" @click.stop="onDesc()"></div>
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
        };
    },
    props: {
        label: String,
        asc: Boolean,
        active: Boolean,
        onAsc: Function,
        onDesc: Function
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.sort_buttons {
    margin-left: 10px;

    & > div {
        width: 0; 
        height: 0;
        border-color: $headings_light_color;
        cursor: pointer;
    }

    .asc {           
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;                    
        border-bottom: 8px solid $headings_light_color;
        margin-bottom: 4px;

        &:hover, &.active {
            border-bottom-color: $headings_color;
        }
    }

    .desc {
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;                    
        border-top: 8px solid $headings_light_color;

        &:hover, &.active {
            border-top-color: $headings_color;
        }
    }
}
</style>