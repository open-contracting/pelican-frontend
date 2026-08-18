<template>
  <GChart
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { GChart } from "vue-google-charts";
import { useI18n } from "vue-i18n";
import { useFormatters } from "@/composables/useFormatters";

const props = defineProps(["check", "ticks", "showCount"]);

const { t } = useI18n();
const { formatNumber, formatPercentage } = useFormatters();

const chartData = ref([
  [t("datasetLevel.charts.group"), t("datasetLevel.charts.share"), { role: "annotation" }, { role: "style" }],
]);

// https://developers.google.com/chart/interactive/docs/gallery/barchart
const chartOptions = {
  enableInteractivity: false,
  height: 200,
  chartArea: {
    top: 0,
    width: "50%",
    height: 180,
  },
  legend: {
    position: "none",
  },
  baselineColor: "transparent",
  hAxis: {
    viewWindow: {
      min: 0,
      max: 1,
    },
    ticks: props.ticks.slice(1),
    format: "percent",
  },
  annotations: {
    alwaysOutside: true,
    stem: {
      color: "transparent",
    },
    textStyle: {
      color: "#4a4a4a",
      fontName: "'Ubuntu Mono', monospace",
      bold: true,
    },
  },
  colors: ["#555cb3"],
  fontName: "GTEestiProDisplay-Regular",
  fontSize: 14,
};

const ranges = [
  ["0_1", "datasetLevel.charts.label_0_1"],
  ["1_5", "datasetLevel.charts.label_1_5"],
  ["5_20", "datasetLevel.charts.label_5_20"],
  ["20_50", "datasetLevel.charts.label_20_50"],
  ["50_100", "datasetLevel.charts.label_50_100"],
];

onMounted(() => {
  chartData.value.push(
    ...ranges.map(([range, key], index) => {
      const share = props.check.meta.shares[range];
      return [
        t(key),
        share,
        props.showCount
          ? `${formatPercentage(share)} (${formatNumber(props.check.meta.counts[range])})`
          : formatPercentage(share),
        // Only the first bar is colored, by whether its share is within the check's thresholds.
        index === 0 ? (props.ticks[0] <= share && share <= props.ticks[1] ? "color: #919C03" : "color: #d0021b") : "",
      ];
    }),
  );
});
</script>
