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

<script setup>
import DatasetHeader from "@/components/DatasetHeader.vue";
import MainMenu from "./MainMenu.vue";
</script>
