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
            :show-count="true"
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
        InlineBar
    },
    props: ["check"],
    data() {
        return {};
    },
    computed: {
        chartData() {
            var chartData = [];
            chartData.push([
                this.$t("datasetLevel.label_0_1"),
                this.check.meta.counts["0_1"],
                this.check.meta.shares["0_1"]
            ]);
            chartData.push([
                this.$t("datasetLevel.label_1_5"),
                this.check.meta.counts["1_5"],
                this.check.meta.shares["1_5"]
            ]);
            chartData.push([
                this.$t("datasetLevel.label_5_20"),
                this.check.meta.counts["5_20"],
                this.check.meta.shares["5_20"]
            ]);
            chartData.push([
                this.$t("datasetLevel.label_20_50"),
                this.check.meta.counts["20_50"],
                this.check.meta.shares["20_50"]
            ]);
            chartData.push([
                this.$t("datasetLevel.label_50_100"),
                this.check.meta.counts["50_100"],
                this.check.meta.shares["50_100"]
            ]);

            return chartData;
        }
    }
};
</script>

<style>
.table td.label {
    width: 80px;
    padding-top: 7px;
}
</style>
