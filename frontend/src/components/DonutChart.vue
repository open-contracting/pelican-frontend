<template>
    <GChart type="PieChart" :data="chartData" :options="chartOptions" />
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
                    alignment: "center"
                },
                chartArea: { left: 10, top: 20, width: "100%", height: "100%" },
                pieHole: 0.4,
                colors: [
                    "#555CB3",
                    "#6169CC",
                    "#6C75E1",
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
        this.chartData.push(["Category", "Share"]);
        for (var key in this.check.meta.shares) {
            this.chartData.push([key, this.check.meta.shares[key].count]);
        }
    }
};
</script>

<style>
</style>