<template>
  <table class="table table-borderless table-sm">
    <tbody>
      <tr
        v-for="item in chartData"
        :key="item[0]"
      >
        <td class="text-right label">
          <span class="check_name">{{ item[0] }}</span>
        </td>
        <td class="text-right">
          <InlineBar
            :count="item[1]"
            :show-count="showCount"
            :percentage="item[2] * 100"
            :state="'reg'"
          />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import InlineBar from "@/components/InlineBar.vue";

export default {
    components: {
        InlineBar,
    },
    props: ["check", "showCount"],
    data() {
        return {};
    },
    computed: {
        chartData() {
            var chartData = [];
            var onePercent = this.check.meta.total_buyer_count;
            chartData.push([
                this.$t("datasetLevel.charts.label_1"),
                this.check.meta.counts["1"].total_buyer_count,
                this.check.meta.counts["1"].total_buyer_count / onePercent,
            ]);
            chartData.push([
                this.$t("datasetLevel.charts.label_2_20"),
                this.check.meta.counts["2_20"].total_buyer_count,
                this.check.meta.counts["2_20"].total_buyer_count / onePercent,
            ]);
            chartData.push([
                this.$t("datasetLevel.charts.label_21_50"),
                this.check.meta.counts["21_50"].total_buyer_count,
                this.check.meta.counts["21_50"].total_buyer_count / onePercent,
            ]);
            chartData.push([
                this.$t("datasetLevel.charts.label_51_100"),
                this.check.meta.counts["51_100"].total_buyer_count,
                this.check.meta.counts["51_100"].total_buyer_count / onePercent,
            ]);
            chartData.push([
                this.$t("datasetLevel.charts.label_100"),
                this.check.meta.counts["100+"].total_buyer_count,
                this.check.meta.counts["100+"].total_buyer_count / onePercent,
            ]);

            return chartData;
        },
    },
};
</script>

<style>
.table td.label {
    width: 80px;
    padding-top: 7px;
}
</style>
