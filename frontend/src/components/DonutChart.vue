<template>
    <GChart type="PieChart" :data="chartData" :options="chartOptions" />
</template>

<script>
const chroma = require("chroma-js");
import { GChart } from "vue-google-charts";
import datasetMixin from "@/plugins/datasetMixins.js";

export default {
    mixins: [datasetMixin],
    data() {
        return {
            // Array will be automatically processed with visualization.arrayToDataTable function
            chartData: [],
            chartOptions: {
                legend: {
                    alignment: "center"
                },
                fontName: "GTEestiProDisplay-Regular",
                chartArea: { left: 10, top: 20, width: "100%", height: "85%" },
                pieHole: 0.4,
                sliceVisibilityThreshold: 0.5 / 360,
                colors: []
            }
        };
    },
    props: ["check"],
    components: { GChart },
    mounted() {
        this.chartData.push(["Category", "Share"]);

        var totalCount = 0;
        var shares = this.orderedShares(this.check.meta.shares);
        for (var key in shares) {
            this.chartData.push([shares[key][0], shares[key][1].count]);
            totalCount += shares[key][1].count;
        }

        this.chartOptions.colors = this.generateGradient(
            this.chartData.slice(1).filter(v => v[1] / totalCount >= this.chartOptions.sliceVisibilityThreshold)
                .length + 1
        );
    },
    methods: {
        generateGradient: function (colorCount) {
            return chroma.scale(["#2B2E5A", "#EFF0FC"]).mode("lab").colors(colorCount);
        }
    }
};
</script>

<style>
svg > g > g:last-child {
    pointer-events: none;
}
</style>
