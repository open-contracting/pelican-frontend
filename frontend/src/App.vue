<template>
  <BApp>
    <div
      id="app"
      class="container-fluid"
    >
      <ErrorAlert />
      <router-view />
    </div>
  </BApp>
</template>

<script setup lang="ts">
import { BApp } from "bootstrap-vue-next";
import ErrorAlert from "@/components/ErrorAlert.vue";
</script>
