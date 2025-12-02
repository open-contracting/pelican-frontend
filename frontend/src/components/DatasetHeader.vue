<template>
  <h1 v-if="dataset">
    <span class="name">{{ dataset.name }}</span>
    ({{ $t("dataset.id") }} {{ dataset.id }})
    | {{ $t("dataset.size") }} {{ $filters.formatNumber(dataset.meta.compiled_releases?.total_unique_ocids) }}
    | {{ $t("created") }} {{ dataset.meta.data_quality_tool_metadata.processing_start }}
  </h1>
</template>

<script>
export default {
    data: () => ({
        showHidden: {},
    }),
    computed: {
        dataset() {
            if (this.$store.getters.dataset?.meta !== undefined) {
                return this.$store.getters.dataset;
            }
            return undefined;
        },
    },
};
</script>

<style scoped lang="scss">
@import "@/scss/main";

h1 {
    font-size: 13px;
    font-family: $font-family-thin;
    margin-bottom: 40px;
    text-align: right;
    color: $headings_light_color;
}

.name {
    font-family: $font-family-sans-serif;
}
</style>
