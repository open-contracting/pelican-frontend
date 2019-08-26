<template>
    <div class="row h-100">
        <main-menu></main-menu>

        <main role="main" class="resource col-11 col-sm-10 col-md-9 col-lg-9 col-xl-10 offset-1 offset-sm-2 offset-md-3 offset-lg-3 offset-xl-2">
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

.main_nav {
    margin-top: 50px;
    display: inline-block;
    position: relative;
    left: -10px;
}

.main_nav > li {
    display: block;
    width: 100%;
    margin-top: 10px;
    font-size: 0.8em;
}

.main_nav a {
    color: $menu_gray;
    font-weight: 500;
    letter-spacing: 0.05rem;
}

.main_nav a :hover {
    text-decoration: none;
}

.main_nav .menu_icon_small {
    font-size: 1.2rem;
    padding-right: 10px;
    position: relative;
    top: 2px;
}
</style>