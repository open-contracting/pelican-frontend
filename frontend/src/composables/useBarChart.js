import { onMounted, ref } from "vue";
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

/** Color a bar by whether its share is within the check's thresholds. */
export function shareStyle(share, ticks) {
  return ticks[0] <= share && share <= ticks[1] ? "color: #919C03" : "color: #d0021b";
}

/** Build the data and options for a bar chart. ``bars`` returns one entry per bar, top to bottom. */
export function useBarChart(props, bars) {
  const { t } = useI18n();
  const { formatNumber, formatPercentage } = useFormatters();

  const chartData = ref([
    [t("datasetLevel.charts.group"), t("datasetLevel.charts.share"), { role: "annotation" }, { role: "style" }],
  ]);

  const chartOptions = {
    ...BAR_CHART_OPTIONS,
    height: 200,
    chartArea: {
      top: 0,
      width: "50%",
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

  onMounted(() => {
    chartData.value.push(
      ...bars().map(({ key, share, count }, index) => [
        t(key),
        share,
        props.showCount ? `${formatPercentage(share)} (${formatNumber(count)})` : formatPercentage(share),
        // Only the first bar is colored, as the check's thresholds apply to it alone.
        index === 0 ? shareStyle(share, props.ticks) : "",
      ]),
    );
  });

  return { chartData, chartOptions };
}
