<template>
    <div class="home ">
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.home") }}</h2>
        <DatasetPicker />
    </div>
</template>

<script>
import DatasetPicker from "@/components/DatasetPicker.vue";

export default {
    name: "home",
    components: {
        DatasetPicker
    }
};
</script>

