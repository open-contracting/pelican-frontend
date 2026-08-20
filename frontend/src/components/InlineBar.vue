<template>
  <div
    ref="bar"
    class="inline_bar numeric"
    :class="state"
  >
    <div
      class="bar"
      :style="{ width: barWidth + 'px' }"
    >
      <span v-if="barWidth > 30">{{ formatPercentage(ratio) }}</span>
    </div>
    <div
      v-if="barWidth <= 30"
      class="count"
    >
      <span
        v-if="barWidth <= 30"
        class="small_label"
      >{{ formatPercentage(ratio) }}</span>
      <span
        v-if="showCount"
        class="count_holder"
      >
        <span class="count_holder">({{ formatNumber(count) }})</span>
      </span>
    </div>
    <div
      v-if="barWidth > 30 && showCount"
      class="count"
    >
      <span class="count_holder">({{ formatNumber(count) }})</span>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, useTemplateRef } from "vue";
import { useFormatters } from "@/composables/useFormatters.js";

const props = defineProps({
  numerator: { type: Number, required: true },
  denominator: { type: Number, required: true },
  count: Number,
  state: String,
  showCount: Boolean,
});

const { formatPercentage, formatNumber } = useFormatters();

const bar = useTemplateRef("bar");
const barWidth = ref(1);

const ratio = computed(() => {
  if (!props.denominator) return 0;
  return props.numerator / props.denominator;
});

onMounted(() => {
  if (ratio.value > 0) {
    if (props.showCount) {
      barWidth.value = (bar.value.clientWidth - 100) * ratio.value;
    } else {
      barWidth.value = bar.value.clientWidth * ratio.value;
    }
  }
});
</script>

<style scoped lang="scss">
@import "@/scss/variables";
.inline_bar {
    width: 100%;
    text-align: left;
    display: inline-block;
    position: relative;
}

// The bar has no content at 30px or narrower, so the default vertical-align: baseline would
// position it lower than the .count. Top alignment is independent of content.
.bar,
.count {
    display: inline-block;
    vertical-align: top;
    height: 25px;
    font-size: 14px;
    padding-top: 4px;
}

.count {
    color: $na_color;
}

.count_holder {
    padding-left: 10px;
}

.bar {
    padding-left: 5px;
    font-weight: 700;
    border-radius: 8px;
}

.ok .bar {
    background-color: $ok_color;
    color: white;
}

.failed .bar {
    background-color: $failed_color;
    color: white;
}

.na .bar {
    background-color: $na_bar_color;
}

.small_label {
    font-weight: 700;
    color: $text-color;
    padding-left: 5px;
}

.reg .bar {
    background-color: #555cb3;
    color: white;
}
</style>
