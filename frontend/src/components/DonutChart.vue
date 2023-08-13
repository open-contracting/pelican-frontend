<template>
  <GChart
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import { GChart } from "vue-google-charts";
import datasetMixin from "@/plugins/datasetMixins.js";

export default {
    components: { GChart },
    mixins: [datasetMixin],
    props: ["check"],
    data() {
        return {
            chartData: [],
            // https://developers.google.com/chart/interactive/docs/gallery/barchart
            chartOptions: {
                height: 300,
                legend: {
                    position: "none",
                },
                chartArea: {
                    top: 0,
                    height: 280,
                },
                hAxis: {
                    viewWindowMode: "maximized",
                    minValue: 0,
                },
                annotations: {
                    stem: {
                        color: "transparent",
                        length: 5,
                    }
                },
                colors: ["#555cb3"],
                fontName: "GTEestiProDisplay-Regular",
                fontSize: 14,
            }
        };
    },
    mounted() {
        this.chartData.push([
            this.$t("datasetLevel.code"),
            this.$t("datasetLevel.count"),
            {label: this.$t("datasetLevel.percent"), role: "annotation"}
        ]);

        var shares = this.orderedShares(this.check.meta.shares);
        var labelLength = 0;

        for (var key in shares) {
            this.chartData.push([
                shares[key][0],
                shares[key][1].count,
                this.$options.filters.formatPercentage(100 * shares[key][1].share)
            ]);
            labelLength += shares[key][0].length;
        }

        // Make more room for long labels.
        if (labelLength / shares.length > 10) {
            this.chartOptions.chartArea.left = 120;
            this.chartOptions.chartArea.width = 200;
        }
    }
};
</script>

<style>
svg > g > g:last-child {
    pointer-events: none;
}
</style>
