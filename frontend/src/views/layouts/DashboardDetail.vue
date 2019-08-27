<template>
    <div class="row h-100">
        <main-menu></main-menu>

        <main role="main" class="dataset_level_check_detail main_content col col-11 col-sm-10 col-md-5 col-lg-5 col-xl-5">
            <slot name="content" />
        </main>
        <div class="preview col col-11 col-sm-10 col-md-4 col-lg-4 col-xl-5">
            <slot name="preview" />
        </div>
    </div>
</template>

<script>
import MainMenu from "@/views/layouts/MainMenu.vue";

export default {
    name: "dashboard",
    data: function() {
        return {};
    },
    components: { MainMenu }
};
</script>

<style lang="scss">
@import "src/scss/main";
</style>