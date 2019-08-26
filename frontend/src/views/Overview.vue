<template>
    <dashboard>
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.overview") }}</h2>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";

export default {
    name: "overview",
    components: { Dashboard }
};
</script>
