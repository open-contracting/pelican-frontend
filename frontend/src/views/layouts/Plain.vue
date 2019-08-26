<template>
    <div class="row h-100">
        <main role="main" class="home main_content col-12">
            <slot />
        </main>
    </div>
</template>

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