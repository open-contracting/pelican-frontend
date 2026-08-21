<template>
  <div class="progress_bar">
    <template v-for="(b, i) in allBars" :key="i">
      <div
        v-if="b.value"
        :class="['inner', b.class]"
        :style="{ width: b.value + '%' }"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  value?: number;
  ok?: number;
  failed?: number;
}>();

const allBars = computed(() => {
  const result: { value: number; class?: string }[] = [];

  if (props.value) {
    result.push({ value: props.value });
  }
  if (props.ok) {
    result.push({ value: props.ok, class: "ok" });
  }
  if (props.failed) {
    result.push({ value: props.failed, class: "failed" });
  }

  return result;
});
</script>

<style scoped lang="scss">

.progress_bar {
    width: 100%;
    height: 4px;
    background-color: $na_light_color;
    display: inline-block;
    position: relative;
    overflow: hidden;
    border-radius: 2px;

    .inner {
        background-color: $primary;
        height: 4px;
        display: inline-block;
        // A .inner has no content, so the default vertical-align: baseline would position it below
        // the 4px height, in the overflow, which is hidden. Top alignment is independent of content.
        vertical-align: top;

        &.ok {
            background-color: $ok_bright_color;
        }

        &.failed {
            background-color: $failed_color;
        }
    }
}
</style>
