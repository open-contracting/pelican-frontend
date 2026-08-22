<template>
  <div class="row h-100">
    <main
      role="main"
      class="home main_content col-12"
    >
      <SiteHeader />
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import SiteHeader from "./SiteHeader.vue";
</script>
