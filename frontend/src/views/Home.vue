<template>
  <plain>
    <h2>{{ $t("sections.home") }}</h2>
    <div class="result_box">
      <DatasetPicker />
    </div>
  </plain>
</template>

<script setup>
import DatasetPicker from "@/components/DatasetPicker.vue";
import Plain from "./layouts/Plain.vue";
</script>
