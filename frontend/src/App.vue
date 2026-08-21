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

<script setup>
import { BApp } from "bootstrap-vue-next";
import ErrorAlert from "@/components/ErrorAlert.vue";
</script>
