<template>
  <div class="row h-100">
    <main-menu />

    <main
      role="main"
      class="main main_content col col-12"
    >
      <div class="main_envelope">
        <DatasetHeader />
        <slot />
      </div>
    </main>
  </div>
</template>

<script>
import MainMenu from "@/views/layouts/MainMenu.vue";
import DatasetHeader from "@/components/DatasetHeader.vue";

export default {
    name: "Dashboard",
    components: { MainMenu, DatasetHeader },
    data: function () {
        return {};
    },
    computed: {
        dataset() {
            if (this.$store.getters.dataset != null) {
                return this.$store.getters.dataset;
            }
            return [];
        },
    },
};
</script>

<style lang="scss">
@import "src/scss/main";

@media (max-width: 1199.98px) {
    .main_envelope {
        padding-left: 80px;
    }
}

@media (min-width: 1199.98px) {
    .main_envelope {
        padding-left: 215px;
    }
}
</style>
