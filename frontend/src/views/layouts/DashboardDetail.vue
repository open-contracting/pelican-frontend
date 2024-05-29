<template>
  <div class="row h-100">
    <main-menu />

    <div class="col col-12">
      <div class="main_envelope">
        <div class="row">
          <main
            role="main"
            class="dataset_level_check_detail main_content col col-7 col-xl-6"
          >
            <DatasetHeader />
            <slot name="content" />
          </main>
          <div class="preview col col-5 col-xl-6">
            <div class="row">
              <div class="preview_envelope col col-5 col-xl-5">
                <slot name="preview" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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
.preview {
    background-color: white;
    position: relative;
    font-size: 12px;
}

.vjs-tree {
    font-family: $font-family-mono;
    font-size: 13px;
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

@media (max-width: 1199.98px) {
    .main_envelope {
        padding-left: 80px;
    }

    .preview_envelope {
        padding-left: 50px;
    }
}

@media (min-width: 1199.98px) {
    .main_envelope {
        padding-left: 215px;
    }
}
</style>
