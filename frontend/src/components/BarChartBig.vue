<template>
    <GChart type="BarChart" :data="chartData" :options="chartOptions" />
</template>

<script>
import { GChart } from "vue-google-charts";

export default {
    data() {
        return {
            // Array will be automatically processed with visualization.arrayToDataTable function
            chartData: [],
            chartOptions: {
                legend: {
                    position: "none"
                },
                chartArea: { top: 0, height: "90%" },
                hAxis: {
                    minValue: 0,
                    maxValue: 100,
                    format: "#'%'",
                    ticks: [50],
                    gridlines: { color: "#333", count: 4 }
                },
                colors: [
                    "#7B82E3",
                    "#8A91E7",
                    "#989EE9",
                    "#A7ACED",
                    "#B7BBF0",
                    "#C4C7F3",
                    "#D3D5F6",
                    "#E3E5F9",
                    "#F1F2FC",
                    "#313566",
                    "#3D4280",
                    "#494F99"
                ]
            }
        };
    },
    props: ["check"],
    components: { GChart },
    mounted() {
        var sum =
            this.check.meta.shares["0_1"] +
            this.check.meta.shares["1_5"] +
            this.check.meta.shares["5_20"] +
            this.check.meta.shares["20_50"] +
            this.check.meta.shares["50_100"];

        this.chartData.push(["Category", "Share"]);
        this.chartData.push([
            this.$t("datasetLevel.label_0_1"),
            Math.round(this.check.meta.shares["0_1"] / (sum / 100))
        ]);
        this.chartData.push([
            this.$t("datasetLevel.label_1_5"),
            Math.round(this.check.meta.shares["1_5"] / (sum / 100))
        ]);
        this.chartData.push([
            this.$t("datasetLevel.label_5_20"),
            Math.round(this.check.meta.shares["5_20"] / (sum / 100))
        ]);
        this.chartData.push([
            this.$t("datasetLevel.label_20_50"),
            Math.round(this.check.meta.shares["20_50"] / (sum / 100))
        ]);
        this.chartData.push([
            this.$t("datasetLevel.label_50_100"),
            Math.round(this.check.meta.shares["50_100"] / (sum / 100))
        ]);
    }
};
</script>

<style>
</style>