<template>
  <BAlert
    v-if="status != null"
    variant="danger"
    dismissible
    :model-value="true"
    @closed="errorStore.clear()"
  >
    {{ status == 403 ? $t("forbiddenError") : $t("requestError") }}
  </BAlert>
</template>

<script setup lang="ts">
import { BAlert } from "bootstrap-vue-next";
import { computed } from "vue";
import { useErrorStore } from "@/stores/error.js";

const errorStore = useErrorStore();

const status = computed(() => errorStore.status);
</script>
