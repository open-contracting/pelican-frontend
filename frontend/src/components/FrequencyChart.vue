<template>
  <table class="table table-borderless table-sm">
    <tbody>
      <tr
        v-for="item in chartData"
        :key="item.label"
      >
        <td class="text-end label">
          <span class="check_name">{{ item.label }}</span>
        </td>
        <td class="text-end">
          <InlineBar
            :numerator="item.count"
            :denominator="denominator"
            :count="item.count"
            :show-count="showCount"
            state="reg"
          />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import InlineBar from "./InlineBar.vue";

const props = defineProps(["check", "showCount"]);
const { t } = useI18n();

const denominator = computed(() => props.check.meta.total_buyer_count);
const chartData = computed(() => [
    {
        label: t("datasetLevel.charts.label_1"),
        count: props.check.meta.counts["1"].total_buyer_count,
    },
    {
        label: t("datasetLevel.charts.label_2_20"),
        count: props.check.meta.counts["2_20"].total_buyer_count,
    },
    {
        label: t("datasetLevel.charts.label_21_50"),
        count: props.check.meta.counts["21_50"].total_buyer_count,
    },
    {
        label: t("datasetLevel.charts.label_51_100"),
        count: props.check.meta.counts["51_100"].total_buyer_count,
    },
    {
        label: t("datasetLevel.charts.label_100"),
        count: props.check.meta.counts["100+"].total_buyer_count,
    },
]);
</script>

<style>
.table td.label {
    width: 80px;
    padding-top: 7px;
}
</style>
