<template>
    <div class="row h-100">
        <main-menu></main-menu>

        <main role="main" class="dataset_level_check_detail main_content col col-11 col-sm-10 col-md-5 col-lg-5 col-xl-5">
            <slot name="content" />
        </main>
        <div class="preview col col-11 col-sm-10 col-md-4 col-lg-4 col-xl-5">
            <div class="row">
                <div class="preview_envelope col col-11 col-sm-10 col-md-4 col-lg-4 col-xl-5">
                    <slot name="preview" />
                </div>
            </div>
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
.preview {
    background-color: white;
    position: relative;
}

.examples .divider {
    border-top: solid 1px $na_light_color;
    width: 100%;
    margin-top: 40px;
    margin-bottom: 20px;
}

.preview_envelope {
    position: fixed;
    top: 0px;
    right: 0px;
    bottom: 0px;
    overflow-y: scroll;
    padding: 30px;
}
</style>