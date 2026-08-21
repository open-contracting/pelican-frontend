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

<script setup lang="ts">
import DatasetHeader from "@/components/DatasetHeader.vue";
import MainMenu from "./MainMenu.vue";
</script>

<style scoped lang="scss">
.preview {
    background-color: white;
    position: relative;
    font-size: 12px;
}

.preview_envelope {
    position: fixed;
    top: 0px;
    right: 0px;
    bottom: 0px;
    overflow-y: scroll;
    padding: 30px;
}

@include media-breakpoint-down(xl) {
    .preview_envelope {
        padding-left: 50px;
    }
}
</style>
