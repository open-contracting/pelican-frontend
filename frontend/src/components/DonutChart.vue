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
                height: 250,
                legend: {
                    position: "none",
                },
                chartArea: {
                    top: 0,
                    height: 230,
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

            // Index 0 is the header.
        for (var key in shares) {
            if (this.chartData.length > 10) {
                this.chartData[10][0] = this.$t("datasetLevel.other");
                this.chartData[10][1] += shares[key][1].count;
                this.chartData[10][2] += shares[key][1].share;
            } else {
                this.chartData.push([
                    shares[key][0],
                    shares[key][1].count,
                    shares[key][1].share,
                ]);
                labelLength += shares[key][0].length;
            }
        }

        for (let i = 1; i < this.chartData.length; i++) {
            this.chartData[i][2] = this.$options.filters.formatPercentage(100 * this.chartData[i][2]);
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
