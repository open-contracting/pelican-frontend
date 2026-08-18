<template>
  <span>
    <span :id="tooltipId">
      <FontAwesomeIcon icon="info-circle" />
    </span>
    <BTooltip
      :target="tooltipId"
    >
      <span
        class="tooltip_text"
        v-html="text"
      />
    </BTooltip>
  </span>
</template>

<script setup>
import { BTooltip } from "bootstrap-vue-next";
import { useId } from "vue";

defineProps(["text"]);

const tooltipId = useId();
</script>

<style scoped lang="scss">
.loader {
    font-size: 19px;
    font-weight: 700;
    padding: 40px;
}

.spinner {
    margin-bottom: 40px;
    font-size: 40px;
}
</style>
