<template>
  <GChart
    ref="chart"
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup>
import { onMounted, reactive, useTemplateRef } from "vue";
import { GChart } from "vue-google-charts";
import { useI18n } from "vue-i18n";
import { ANNOTATION_FONT, BAR_CHART_OPTIONS, shareStyle, textWidth } from "@/composables/useBarChart.js";
import { useFormatters } from "@/composables/useFormatters.js";
import { DATASET_CHECK_STYLES, DATASET_CHECK_TICKS } from "@/config.js";
import { orderedShares } from "@/util.js";

const props = defineProps(["check", "limit"]);
const { t } = useI18n();
const { formatPercentage, formatNumber } = useFormatters();

const chart = useTemplateRef("chart");

const ROW_HEIGHT = 30;
// Google Charts draws an annotation this far after its bar. Reserving less clips it.
const GAP = 12;
// Elide long labels instead of crowding the bars.
const MAX_LABEL_WIDTH = 0.5;

const chartData = reactive([
  [
    t("datasetLevel.charts.code"),
    t("datasetLevel.charts.share"),
    { role: "annotation" },
    { role: "style" },
    { role: "custom" },
  ],
]);

const chartOptions = reactive({
  ...BAR_CHART_OPTIONS,
  chartArea: {
    top: 0,
  },
  hAxis: {
    viewWindow: {
      min: 0,
      max: 1,
    },
    gridlines: {
      count: 0,
    },
    format: "#,###.#%",
  },
});

onMounted(() => {
  const shares = orderedShares(props.check.meta.shares);
  const ticks = DATASET_CHECK_TICKS[props.check.name];
  const styles = DATASET_CHECK_STYLES[props.check.name];

  // Index 0 of chartData is the header.
  for (const key in shares) {
    if (props.limit && chartData.length > 10) {
      chartData[10][0] = t("datasetLevel.charts.other");
      chartData[10][1] += shares[key][1].share;
      chartData[10][2] += shares[key][1].share;
      chartData[10][4] += shares[key][1].count;
    } else {
      let chartStyles = "";
      if (ticks && (!styles?.length || styles.includes(shares[key][0]))) {
        chartStyles = shareStyle(shares[key][1].share, ticks);
      }
      chartData.push([shares[key][0], shares[key][1].share, shares[key][1].share, chartStyles, shares[key][1].count]);
    }
  }

  for (let i = 1; i < chartData.length; i++) {
    if (props.limit) {
      chartData[i][2] = formatPercentage(chartData[i][2]);
    } else {
      chartData[i][2] = `${formatPercentage(chartData[i][2])} (${formatNumber(chartData[i][4])})`;
    }
  }

  // Size the chart to its bars, so that they are as thick here as in the other charts.
  chartOptions.chartArea.height = (chartData.length - 1) * ROW_HEIGHT;
  chartOptions.height = chartOptions.chartArea.height + (ticks ? ROW_HEIGHT : 0);

  if (ticks) {
    chartOptions.hAxis.ticks = ticks.slice(1);
  } else {
    chartOptions.hAxis.textPosition = "none";
  }

  // Reserve room for the widest label and annotation, which Google Charts otherwise elides.
  const width = chart.value.$el.clientWidth;
  const labelWidth = Math.min(textWidth(chartData.slice(1).map((row) => row[0])) + GAP, width * MAX_LABEL_WIDTH);
  const annotationWidth = textWidth(
    chartData.slice(1).map((row) => row[2]),
    ANNOTATION_FONT,
  );
  chartOptions.chartArea.left = `${(labelWidth / width) * 100}%`;
  chartOptions.chartArea.width = `${((width - labelWidth - annotationWidth - GAP) / width) * 100}%`;
});
</script>
