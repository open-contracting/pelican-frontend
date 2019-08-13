<template>
    <main role="main" class="home main_content col-11 col-sm-10 col-md-9 col-lg-9 col-xl-10 offset-1 offset-sm-2 offset-md-3 offset-lg-3 offset-xl-2">
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.home") }}</h2>
        <DatasetPicker />
    </main>
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

