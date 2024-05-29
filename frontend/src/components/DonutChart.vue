<template>
  <GChart
    type="BarChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import datasetMixin from "@/plugins/datasetMixins.js";
import { GChart } from "vue-google-charts";

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
                    { role: "annotation" },
                    { role: "style" },
                    { role: "custom" },
                ],
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
            },
        };
    },
    mounted() {
        const shares = this.orderedShares(this.check.meta.shares);
        let labelLength = 0;

        // Index 0 of chartData is the header.
        for (const key in shares) {
            if (this.limit && this.chartData.length > 10) {
                this.chartData[10][0] = this.$t("datasetLevel.charts.other");
                this.chartData[10][1] += shares[key][1].share;
                this.chartData[10][2] += shares[key][1].share;
                this.chartData[10][4] += shares[key][1].count;
            } else {
                let styles = "";
                if (this.ticks && (!this.styles.length || this.styles.includes(shares[key][0]))) {
                    styles =
                        this.ticks[0] <= shares[key][1].share && shares[key][1].share <= this.ticks[1]
                            ? "color: #919C03"
                            : "color: #d0021b";
                }
                this.chartData.push([
                    shares[key][0],
                    shares[key][1].share,
                    shares[key][1].share,
                    styles,
                    shares[key][1].count,
                ]);
            }
            if (shares.length <= 10 || this.chartData <= 10) {
                labelLength += shares[key][0].length;
            }
        }

        for (let i = 1; i < this.chartData.length; i++) {
            if (this.limit) {
                this.chartData[i][2] = this.$options.filters.formatPercentage(100 * this.chartData[i][2]);
            } else {
                this.chartData[i][2] = `${this.$options.filters.formatPercentage(
                    100 * this.chartData[i][2],
                )} (${this.$options.filters.formatNumber(this.chartData[i][4])})`;
            }
        }

        // ticks is undefined in data().
        if (this.ticks) {
            this.chartOptions.hAxis.ticks = this.ticks.slice(1);
        } else {
            // Hide the x-axis and use the full height.
            this.chartOptions.hAxis.textPosition = "none";
            this.chartOptions.chartArea.height = this.chartOptions.height;
        }

        const averageLabelLength = labelLength / shares.length;
        if (averageLabelLength > 10) {
            // Make room for long labels, and allow a 100% bar to be fully visible.
            this.chartOptions.chartArea.left = `${~~(averageLabelLength * 2)}%`;
            this.chartOptions.chartArea.width = "60%";
        }

        if (!this.limit) {
            // Allow longer annotations to be fully visible.
            this.chartOptions.chartArea.width = averageLabelLength > 10 ? "50%" : "55%";
            this.chartOptions.height = shares.length * 30;
            if (this.ticks) {
                // Make room for the ticks.
                this.chartOptions.chartArea.height = this.chartOptions.height;
                this.chartOptions.height += 30;
            } else {
                this.chartOptions.chartArea.height = "100%";
            }
        }
    },
};
</script>
