<template>
  <GChart
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup>
import { GChart } from "vue-google-charts";
import { useBarChart } from "@/composables/useBarChart";

const props = defineProps({
  check: { type: Object, required: true },
  ticks: { type: Array, required: true },
  showCount: Boolean,
});

const ranges = [
  ["0_1", "datasetLevel.charts.label_0_1"],
  ["1_5", "datasetLevel.charts.label_1_5"],
  ["5_20", "datasetLevel.charts.label_5_20"],
  ["20_50", "datasetLevel.charts.label_20_50"],
  ["50_100", "datasetLevel.charts.label_50_100"],
];

const { chartData, chartOptions } = useBarChart(props, () =>
  ranges.map(([range, key]) => ({
    key,
    share: props.check.meta.shares[range],
    count: props.check.meta.counts[range],
  })),
);
</script>
