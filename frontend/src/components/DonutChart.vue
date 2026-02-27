<template>
  <GChart
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script setup>
import { onMounted, reactive } from "vue";
import { GChart } from "vue-google-charts";
import { useI18n } from "vue-i18n";
import { useFormatters } from "@/composables/useFormatters.js";
import { CHECK_STYLES, CHECK_TICKS } from "@/config.js";
import { orderedShares } from "@/util.js";

const props = defineProps(["check", "limit"]);
const { t } = useI18n();
const { formatPercentage, formatNumber } = useFormatters();

const chartData = reactive([
    [
        t("datasetLevel.charts.code"),
        t("datasetLevel.charts.share"),
        { role: "annotation" },
        { role: "style" },
        { role: "custom" },
    ],
]);

// https://developers.google.com/chart/interactive/docs/gallery/barchart
const chartOptions = reactive({
    enableInteractivity: false,
    height: 250,
    chartArea: {
        top: 0,
        height: 230,
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
        gridlines: {
            count: 0,
        },
        format: "#,###.#%",
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
});

onMounted(() => {
    const shares = orderedShares(props.check.meta.shares);
    const ticks = CHECK_TICKS[props.check.name];
    const styles = CHECK_STYLES[props.check.name];
    let labelLength = 0;

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
                chartStyles =
                    ticks[0] <= shares[key][1].share && shares[key][1].share <= ticks[1]
                        ? "color: #919C03"
                        : "color: #d0021b";
            }
            chartData.push([
                shares[key][0],
                shares[key][1].share,
                shares[key][1].share,
                chartStyles,
                shares[key][1].count,
            ]);
        }
        if (shares.length <= 10 || chartData <= 10) {
            labelLength += shares[key][0].length;
        }
    }

    for (let i = 1; i < chartData.length; i++) {
        if (props.limit) {
            chartData[i][2] = formatPercentage(chartData[i][2]);
        } else {
            chartData[i][2] = `${formatPercentage(chartData[i][2])} (${formatNumber(chartData[i][4])})`;
        }
    }

    if (ticks) {
        chartOptions.hAxis.ticks = ticks.slice(1);
    } else {
        // Hide the x-axis and use the full height.
        chartOptions.hAxis.textPosition = "none";
        chartOptions.chartArea.height = chartOptions.height;
    }

    const averageLabelLength = labelLength / shares.length;
    if (averageLabelLength > 10) {
        // Make room for long labels, and allow a 100% bar to be fully visible.
        chartOptions.chartArea.left = `${~~(averageLabelLength * 2)}%`;
        chartOptions.chartArea.width = "60%";
    }

    if (!props.limit) {
        // Allow longer annotations to be fully visible.
        chartOptions.chartArea.width = averageLabelLength > 10 ? "50%" : "55%";
        chartOptions.height = shares.length * 30;
        if (ticks) {
            // Make room for the ticks.
            chartOptions.chartArea.height = chartOptions.height;
            chartOptions.height += 30;
        } else {
            chartOptions.chartArea.height = "100%";
        }
    }
});
</script>
