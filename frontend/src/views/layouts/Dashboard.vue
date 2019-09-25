<template>
    <div class="row h-100">
        <main-menu></main-menu>

        <main role="main" class="main main_content col-11 col-sm-10 col-md-9 col-lg-9 col-xl-10">
            <DatasetHeader></DatasetHeader>
            <slot />
        </main>
    </div>
</template>

<script>
import MainMenu from "@/views/layouts/MainMenu.vue";
import DatasetHeader from "@/components/DatasetHeader.vue";

export default {
    name: "dashboard",
    data: function() {
        return {};
    },
    components: { MainMenu, DatasetHeader },
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

<style lang="scss">
@import "src/scss/main";
</style>