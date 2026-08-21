<template>
  <GChart
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup lang="ts">
import { GChart } from "vue-google-charts";
import { useBarChart } from "@/composables/useBarChart";
import type { DatasetLevelCheck, PercentileMeta } from "@/types.js";

const props = defineProps<{
  check: DatasetLevelCheck;
  ticks: [number, number];
  showCount?: boolean;
}>();

const ranges = [
  ["0_1", "datasetLevel.charts.label_0_1"],
  ["1_5", "datasetLevel.charts.label_1_5"],
  ["5_20", "datasetLevel.charts.label_5_20"],
  ["20_50", "datasetLevel.charts.label_20_50"],
  ["50_100", "datasetLevel.charts.label_50_100"],
];

const { chartData, chartOptions } = useBarChart(props, () => {
  const meta = props.check.meta as PercentileMeta;

  return ranges.map(([range, key]) => ({
    key,
    share: meta.shares[range],
    count: meta.counts[range],
  }));
});
</script>
