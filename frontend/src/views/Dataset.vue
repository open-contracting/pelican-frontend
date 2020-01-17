<template>
    <dashboard>
        <h2>{{ $t("sections.dataset") }}</h2>
        <div class="description" v-html=" $t('datasetLevel.description')"></div>
        <template v-for="(section, index) in sections">
            <DatasetLevelSection :section="section" v-bind:key="index"></DatasetLevelSection>
        </template>
    </dashboard>
</template>

<script>
// import Loader from "@/components/Loader.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";
import DatasetLevelSection from "@/components/DatasetLevelSection.vue"

export default {
    name: "dataset",
    components: { Dashboard, DatasetLevelSection },
    data: function() {
        return {
            sections: ["status_distribution", "value_distribution", "other_distribution", "repetition", "other"]
        };
    }
};
</script>
