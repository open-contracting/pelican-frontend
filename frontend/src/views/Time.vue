<template>
    <dashboard>
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.time") }}</h2>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";

export default {
    name: "time",
    components: { Dashboard }
};
</script>
