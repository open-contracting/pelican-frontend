<template>
  <BRow class="buttons">
    <BCol>
      <button
        :class="`variant-${variant} btn-${variant}`"
        href="#"
        @click.stop.prevent="$emit('retry')"
      >
        <FontAwesomeIcon
          :icon="['fas', 'redo-alt']"
          class="icon"
        />
        {{ $t("tryAgain") }}
      </button>
    </BCol>
    <BCol class="right-align">
      <button
        :class="`variant-${variant} btn-${variant}`"
        href="#"
        @click.stop.prevent="$emit('close')"
      >
        <FontAwesomeIcon
          :icon="['fas', 'window-close']"
          class="icon"
        />
        {{ $t("close") }}
      </button>
    </BCol>
  </BRow>
</template>

<script setup lang="ts">
import { BCol, BRow } from "bootstrap-vue-next";

defineProps<{
  variant: "success" | "warning" | "danger";
}>();
defineEmits<{ retry: []; close: [] }>();
</script>

<style scoped lang="scss">
@import "@/scss/variables";

.buttons {
    margin-top: 1em;
}

.right-align {
    text-align: right;
    align-items: flex-end;
}

.icon {
    margin-right: 0.5em;
}

.variant-success {
    color: #606602;
}

.variant-danger,
.variant-warning {
    color: #6c010e;
}

.btn-danger,
.btn-warning,
.btn-success {
    border-radius: 5px;
    border: 1px solid $na_color;
    padding: 1em;
}
</style>
