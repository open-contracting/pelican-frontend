import { computed, onMounted, ref, useTemplateRef } from "vue";
import type { GChart } from "vue-google-charts";
import { useI18n } from "vue-i18n";
import { useFormatters } from "@/composables/useFormatters";

// Spreading this into a chart's options copies the nested objects by reference: replace them, don't mutate.
// https://developers.google.com/chart/interactive/docs/gallery/barchart
export const BAR_CHART_OPTIONS = {
  enableInteractivity: false,
  legend: {
    position: "none",
  },
  baselineColor: "transparent",
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

/** A row of a chart's data: the label, the share, then the annotation and style columns. */
export type ChartRow = (string | number | { role: string })[];

// The annotations are bold and monospace, unlike the labels.
export const ANNOTATION_FONT = `bold ${BAR_CHART_OPTIONS.fontSize}px ${BAR_CHART_OPTIONS.annotations.textStyle.fontName}`;

// A canvas element always has a 2D context. getContext() is nullable for the contexts that a browser can lack.
const context = document.createElement("canvas").getContext("2d") as CanvasRenderingContext2D;

/** The width in pixels of the widest text, as the chart draws it. */
export function textWidth(texts: string[], font = `${BAR_CHART_OPTIONS.fontSize}px ${BAR_CHART_OPTIONS.fontName}`) {
  context.font = font;
  return Math.max(...texts.map((text) => context.measureText(text).width));
}

// Google Charts draws an annotation this far after its bar. Reserving less clips it.
export const GAP = 12;

// Elide long labels instead of crowding the bars.
export const MAX_LABEL_WIDTH = 0.5;

/** Color a bar by whether its share is within the check's thresholds. */
export function shareStyle(share: number, ticks: [number, number]) {
  return ticks[0] <= share && share <= ticks[1] ? "color: #919C03" : "color: #d0021b";
}

interface BarChartProps {
  ticks: [number, number];
  showCount?: boolean;
}

/** Build the data and options for a bar chart. ``bars`` returns one entry per bar, top to bottom. */
export function useBarChart(props: BarChartProps, bars: () => { key: string; share: number; count: number }[]) {
  const { t } = useI18n();
  const { formatNumber, formatPercentage } = useFormatters();

  const element = useTemplateRef<InstanceType<typeof GChart>>("chart");
  // The chart's width is only known once it is in the document.
  const width = ref(0);

  onMounted(() => {
    width.value = element.value?.$el.clientWidth ?? 0;
  });

  const rows = computed(() =>
    bars().map(({ key, share, count }, index) => ({
      label: t(key),
      share,
      annotation: props.showCount ? `${formatPercentage(share)} (${formatNumber(count)})` : formatPercentage(share),
      // Only the first bar is colored, as the check's thresholds apply to it alone.
      style: index === 0 ? shareStyle(share, props.ticks) : "",
    })),
  );

  const chartData = computed<ChartRow[]>(() => [
    [t("datasetLevel.charts.group"), t("datasetLevel.charts.share"), { role: "annotation" }, { role: "style" }],
    ...rows.value.map(({ label, share, annotation, style }) => [label, share, annotation, style]),
  ]);

  const chartOptions = computed(() => {
    const labelWidth = Math.min(textWidth(rows.value.map((row) => row.label)) + GAP, width.value * MAX_LABEL_WIDTH);
    const annotationWidth = textWidth(
      rows.value.map((row) => row.annotation),
      ANNOTATION_FONT,
    );

    return {
      ...BAR_CHART_OPTIONS,
      height: 200,
      chartArea: {
        top: 0,
        height: 180,
        left: `${(labelWidth / width.value) * 100}%`,
        width: `${((width.value - labelWidth - annotationWidth - GAP) / width.value) * 100}%`,
      },
      hAxis: {
        viewWindow: {
          min: 0,
          max: 1,
        },
        ticks: props.ticks.slice(1),
        format: "percent",
      },
    };
  });

  return { chartData, chartOptions };
}
