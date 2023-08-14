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
    props: ["check", "limit"],
    data() {
        return {
            chartData: [
                [
                    this.$t("datasetLevel.charts.code"),
                    this.$t("datasetLevel.charts.share"),
                    {role: "custom"},
                    {role: "annotation"},
                ]
            ],
            // https://developers.google.com/chart/interactive/docs/gallery/barchart
            chartOptions: {
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
            }
        };
    },
    mounted() {
        var shares = this.orderedShares(this.check.meta.shares);
        var labelLength = 0;

        // Index 0 is the header.
        for (var key in shares) {
            if (this.limit && this.chartData.length > 10) {
                this.chartData[10][0] = this.$t("datasetLevel.charts.other");
                this.chartData[10][1] += shares[key][1].share;
                this.chartData[10][2] += shares[key][1].count;
                this.chartData[10][3] += shares[key][1].share;
            } else {
                this.chartData.push([
                    shares[key][0],
                    shares[key][1].share,
                    shares[key][1].count,
                    shares[key][1].share,
                ]);
                labelLength += shares[key][0].length;
            }
        }

        for (let i = 1; i < this.chartData.length; i++) {
            if (this.limit) {
                this.chartData[i][3] = this.$options.filters.formatPercentage(100 * this.chartData[i][3]);
            } else {
                this.chartData[i][3] = `${this.$options.filters.formatPercentage(100 * this.chartData[i][3])} (${this.$options.filters.formatNumber(this.chartData[i][2])})`;
            }
        }

        // ticks is undefined in data().
        if (this.ticks) {
            this.chartOptions.hAxis.ticks = this.ticks;
        } else {
            // Hide the x-axis and use the full height.
            this.chartOptions.chartArea.height = this.chartOptions.height;
            this.chartOptions.hAxis.textPosition = "none";
        }

        // Make more room for long labels.
        var averageLabelLength = labelLength / shares.length;
        if (averageLabelLength > 10) {
            this.chartOptions.chartArea.left = `${~~(averageLabelLength * 2)}%`;
            this.chartOptions.chartArea.width = "60%"; // for a 100% bar to be fully visible
        }

        if (!this.limit) {
            this.chartOptions.chartArea.width = averageLabelLength > 10 ? "50%" : "55%"; // longer annotations
            this.chartOptions.height = shares.length * 30;
            if (this.ticks) {
                this.chartOptions.chartArea.height = this.chartOptions.height;
                this.chartOptions.height += 30;
            } else {
                this.chartOptions.chartArea.height = "100%";
            }
        }
    }
};
</script>
