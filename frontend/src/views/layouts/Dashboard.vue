<template>
  <div class="row h-100">
    <main-menu />

    <main
      role="main"
      class="main main_content col col-12"
    >
      <div class="main_envelope">
        <SiteHeader>
          <DatasetHeader />
        </SiteHeader>
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import DatasetHeader from "@/components/DatasetHeader.vue";
import MainMenu from "./MainMenu.vue";
import SiteHeader from "./SiteHeader.vue";
</script>
