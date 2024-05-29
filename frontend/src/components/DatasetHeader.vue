<template>
  <h1 v-if="dataset">
    <span class="name">{{ dataset.name }}</span>
    ({{ $t("dataset.id") }} {{ dataset.id }})
    | {{ $t("dataset.size") }} {{ dataset.meta.compiled_releases?.total_unique_ocids | formatNumber }}
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
            if (this.$store.getters.dataset != null && this.$store.getters.dataset.meta != undefined) {
                return this.$store.getters.dataset;
            }
            return undefined;
        },
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

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
