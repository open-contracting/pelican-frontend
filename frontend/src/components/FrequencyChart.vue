<template>
  <GChart
    ref="chart"
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup lang="ts">
import { GChart } from "vue-google-charts";
import { useBarChart } from "@/composables/useBarChart";
import type { DatasetLevelCheck, SingleValueShareMeta } from "@/types.js";

const props = defineProps<{
  check: DatasetLevelCheck;
  ticks: [number, number];
  showCount?: boolean;
}>();

const ranges = [
  ["1", "datasetLevel.charts.label_1"],
  ["2_20", "datasetLevel.charts.label_2_20"],
  ["21_50", "datasetLevel.charts.label_21_50"],
  ["51_100", "datasetLevel.charts.label_51_100"],
  ["100+", "datasetLevel.charts.label_100"],
];

const { chartData, chartOptions } = useBarChart(props, () => {
  const meta = props.check.meta as SingleValueShareMeta;

  return ranges.map(([range, key]) => {
    const count = meta.counts[range].total_unique_count;
    return { key, share: count / meta.total_unique_count, count };
  });
});
</script>
