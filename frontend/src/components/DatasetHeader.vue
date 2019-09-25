<template>
    <h3>
        <span class="name">{{ dataset.name }}</span>
        <br />
        <i>id:</i>
        {{ dataset.id }}
        <i>created:</i>
        {{ dataset.meta.data_quality_tool_metadata.processing_start }}
    </h3>
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