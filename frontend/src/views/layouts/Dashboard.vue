<template>
    <div class="row h-100">
        <main-menu></main-menu>

        <main role="main" class="main main_content col-11 col-sm-10 col-md-9 col-lg-9 col-xl-10">
            <slot />
        </main>
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