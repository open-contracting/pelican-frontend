<template>
    <div class="resource">
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.resource") }}</h2>
        <h4>ALL RESOURCE LEVEL CHECKS</h4>
        <div class="result_box">
            <ResourceLevelList />
        </div>
    </div>
</template>

<script>
import ResourceLevelList from "@/components/ResourceLevelList.vue";

export default {
    name: "resource",
    components: {
        ResourceLevelList
    }
};
</script>
