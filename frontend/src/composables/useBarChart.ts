import { computed } from "vue";
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

  // Computed, not built once, so that the labels and the annotations follow the reader's language.
  const chartData = computed<ChartRow[]>(() => [
    [t("datasetLevel.charts.group"), t("datasetLevel.charts.share"), { role: "annotation" }, { role: "style" }],
    ...bars().map(({ key, share, count }, index) => [
      t(key),
      share,
      props.showCount ? `${formatPercentage(share)} (${formatNumber(count)})` : formatPercentage(share),
      // Only the first bar is colored, as the check's thresholds apply to it alone.
      index === 0 ? shareStyle(share, props.ticks) : "",
    ]),
  ]);

  const chartOptions = {
    ...BAR_CHART_OPTIONS,
    height: 200,
    // Room for the widest label, which Google Charts otherwise wraps onto a second line, and for the
    // annotation after the longest bar.
    chartArea: {
      top: 0,
      left: "42%",
      width: "43%",
      height: 180,
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

  return { chartData, chartOptions };
}
