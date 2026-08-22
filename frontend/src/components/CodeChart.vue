<template>
  <GChart
    ref="chart"
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup lang="ts">
import { onMounted, ref, useTemplateRef } from "vue";
import { GChart } from "vue-google-charts";
import type { GoogleChartOptions } from "vue-google-charts/dist/types";
import { useI18n } from "vue-i18n";
import type { ChartRow } from "@/composables/useBarChart.js";
import {
  ANNOTATION_FONT,
  BAR_CHART_OPTIONS,
  GAP,
  MAX_LABEL_WIDTH,
  shareStyle,
  textWidth,
} from "@/composables/useBarChart.js";
import { useFormatters } from "@/composables/useFormatters.js";
import { DATASET_CHECKS } from "@/config.js";
import type { CodeMeta, DatasetLevelCheck } from "@/types.js";
import { orderedShares } from "@/util.js";

/** A bar, before it becomes a row: the chart formats the share and the count into one annotation. */
interface Bar {
  code: string;
  share: number;
  count: number;
  style: string;
}

const props = defineProps<{
  check: DatasetLevelCheck;
  limit?: boolean;
}>();
const { t } = useI18n();
const { formatPercentage, formatNumber } = useFormatters();

const element = useTemplateRef<InstanceType<typeof GChart>>("chart");

const ROW_HEIGHT = 30;
// Beyond this many bars, a limited chart merges the remaining shares into the last one.
const MAX_BARS = 10;

const chartData = ref<ChartRow[]>([
  [
    t("datasetLevel.charts.code"),
    t("datasetLevel.charts.share"),
    { role: "annotation" },
    { role: "style" },
    { role: "custom" },
  ],
]);

// The rest of the options depend on the bars, which are only known once the chart can be measured.
const chartOptions = ref<GoogleChartOptions>({ ...BAR_CHART_OPTIONS });

onMounted(() => {
  const meta = props.check.meta as CodeMeta;
  // Only a code check is charted here, and only that type has styles.
  const chart = DATASET_CHECKS[props.check.name];
  const { ticks, styles } = chart?.type === "code" ? chart : { ticks: undefined, styles: undefined };
  const bars: Bar[] = [];

  for (const [code, share] of orderedShares(meta.shares)) {
    if (props.limit && bars.length === MAX_BARS) {
      const other = bars[MAX_BARS - 1];
      other.code = t("datasetLevel.charts.other");
      other.share += share.share;
      other.count += share.count;
    } else {
      bars.push({
        code,
        share: share.share,
        count: share.count,
        style: ticks && (!styles?.length || styles.includes(code)) ? shareStyle(share.share, ticks) : "",
      });
    }
  }

  const annotation = (bar: Bar) =>
    props.limit ? formatPercentage(bar.share) : `${formatPercentage(bar.share)} (${formatNumber(bar.count)})`;

  chartData.value.push(...bars.map((bar): ChartRow => [bar.code, bar.share, annotation(bar), bar.style, bar.count]));

  // Size the chart to its bars, so that they are as thick here as in the other charts.
  const height = bars.length * ROW_HEIGHT;

  // Reserve room for the widest label and annotation, which Google Charts otherwise elides.
  const width = element.value?.$el.clientWidth ?? 0;
  const labelWidth = Math.min(textWidth(bars.map((bar) => bar.code)) + GAP, width * MAX_LABEL_WIDTH);
  const annotationWidth = textWidth(bars.map(annotation), ANNOTATION_FONT);

  chartOptions.value = {
    ...BAR_CHART_OPTIONS,
    height: height + (ticks ? ROW_HEIGHT : 0),
    chartArea: {
      top: 0,
      height,
      left: `${(labelWidth / width) * 100}%`,
      width: `${((width - labelWidth - annotationWidth - GAP) / width) * 100}%`,
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
      // Without thresholds to mark, the axis has nothing to label.
      ...(ticks ? { ticks: ticks.slice(1) } : { textPosition: "none" }),
    },
  };
});
</script>
