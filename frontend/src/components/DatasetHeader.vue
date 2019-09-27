<template>
    <h1 v-if="dataset">
        <i>id</i>
        {{ dataset.id }} |
        <span class="name">{{ dataset.name }}</span>
        |
        <i>size</i>
        {{ dataset.size | formatNumber}}
        |
        <i>created</i>
        {{ dataset.meta.data_quality_tool_metadata.processing_start }}
    </h1>
</template>

<script>
export default {
    data: function() {
        return {
            showHidden: {}
        };
    },
    computed: {
        dataset() {
            if (this.$store.getters.dataset != null) {
                return this.$store.getters.dataset;
            }
            return [];
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.name {
    font-family: $font-family-bold;
    color: $headings_light_color;
}
</style>