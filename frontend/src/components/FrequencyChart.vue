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
  ["1", "datasetLevel.charts.label_1"],
  ["2_20", "datasetLevel.charts.label_2_20"],
  ["21_50", "datasetLevel.charts.label_21_50"],
  ["51_100", "datasetLevel.charts.label_51_100"],
  ["100+", "datasetLevel.charts.label_100"],
];

const { chartData, chartOptions } = useBarChart(props, () =>
  ranges.map(([range, key]) => {
    const count = props.check.meta.counts[range].total_unique_count;
    return { key, share: count / props.check.meta.total_unique_count, count };
  }),
);
</script>
