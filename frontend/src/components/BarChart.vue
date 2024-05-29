<template>
  <GChart
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import { GChart } from "vue-google-charts";

export default {
    components: { GChart },
    props: ["check", "ticks"],
    data() {
        return {
            chartData: [
                [
                    this.$t("datasetLevel.charts.group"),
                    this.$t("datasetLevel.charts.share"),
                    { role: "annotation" },
                    { role: "style" },
                ],
            ],
            // https://developers.google.com/chart/interactive/docs/gallery/barchart
            chartOptions: {
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
                    ticks: this.ticks.slice(1),
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
            },
        };
    },
    mounted() {
        this.chartData.push([
            this.$t("datasetLevel.charts.label_0_1"),
            this.check.meta.shares["0_1"],
            this.$options.filters.formatPercentage(100 * this.check.meta.shares["0_1"]),
            this.ticks[0] <= this.check.meta.shares["0_1"] && this.check.meta.shares["0_1"] <= this.ticks[1]
                ? "color: #919C03"
                : "color: #d0021b",
        ]);
        this.chartData.push([
            this.$t("datasetLevel.charts.label_1_5"),
            this.check.meta.shares["1_5"],
            this.$options.filters.formatPercentage(100 * this.check.meta.shares["1_5"]),
            "",
        ]);
        this.chartData.push([
            this.$t("datasetLevel.charts.label_5_20"),
            this.check.meta.shares["5_20"],
            this.$options.filters.formatPercentage(100 * this.check.meta.shares["5_20"]),
            "",
        ]);
        this.chartData.push([
            this.$t("datasetLevel.charts.label_20_50"),
            this.check.meta.shares["20_50"],
            this.$options.filters.formatPercentage(100 * this.check.meta.shares["20_50"]),
            "",
        ]);
        this.chartData.push([
            this.$t("datasetLevel.charts.label_50_100"),
            this.check.meta.shares["50_100"],
            this.$options.filters.formatPercentage(100 * this.check.meta.shares["50_100"]),
            "",
        ]);
    },
};
</script>
