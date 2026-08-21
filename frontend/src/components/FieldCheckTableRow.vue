<template>
  <tr
    v-if="check"
    class="clickable"
    @click="navigate($event, detailRouterArguments)"
  >
    <td class="break_word">
      <slot :to="detailRouterArguments">
        <RouterLink
          class="check_link"
          :to="detailRouterArguments"
        >{{ check.path }}</RouterLink>
      </slot>
    </td>

    <td>
      <div
        v-if="showStats"
        class="row h-100 g-0 align-items-center"
      >
        <div
          class="col col-3 col-lg-2 col-xl-2 field_check_result d-flex align-items-center justify-content-end"
        >
          <span class="field_check_result_value">{{ formatPercentage(check.coverageOkRatio) }}</span>
        </div>
        <div
          class="col col-9 col-lg-7 col-xl-5 col-xxl-4 col-xxxxl-3 numeric field_check_count d-flex align-items-center justify-content-end"
        >{{ formatNumber(check.coverage.passed_count) }}/{{ formatNumber(check.coverage.total_count) }}</div>
        <div
          class="col col-12 col-lg-3 col-xl-4 col-xxl-6 col-xxxxl-7 field_check_bar d-flex align-items-center justify-content-end"
        >
          <span class="field_check_bar_envelope">
            <ProgressBar
              :ok="check.coverageOkRatio * 100"
              :failed="check.coverageFailedRatio * 100"
            />
          </span>
        </div>
      </div>
    </td>

    <template v-if="check.quality.total_count">
      <td>
        <div
          v-if="showStats"
          class="row h-100 g-0 align-items-center"
        >
          <div
            class="col col-3 col-lg-2 col-xl-2 field_check_result d-flex align-items-center justify-content-end"
          >
            <span class="field_check_result_value">{{ formatPercentage(check.qualityOkRatio) }}</span>
          </div>
          <div
            class="col col-9 col-lg-7 col-xl-5 col-xxl-4 col-xxxxl-3 numeric field_check_count d-flex align-items-center justify-content-end"
          >{{ formatNumber(check.quality.passed_count) }}/{{ formatNumber(check.quality.total_count) }}</div>
          <div
            class="col col-12 col-lg-3 col-xl-4 col-xxl-6 col-xxxxl-7 field_check_bar d-flex align-items-center justify-content-end"
          >
            <span class="field_check_bar_envelope">
              <ProgressBar
                v-if="check.quality.total_count"
                :ok="check.qualityOkRatio * 100"
                :failed="check.qualityFailedRatio * 100"
              />
            </span>
          </div>
        </div>
      </td>
    </template>
    <td v-else />
  </tr>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useClickable } from "@/composables/useClickable";
import { useFormatters } from "@/composables/useFormatters";
import { useDatasetStore } from "@/stores/dataset.js";
import type { FieldLevelCheck } from "@/types.js";
import ProgressBar from "./ProgressBar.vue";

const props = withDefaults(
  defineProps<{
    check: FieldLevelCheck;
    showStats?: boolean;
  }>(),
  { showStats: true },
);

const datasetStore = useDatasetStore();
const { navigate } = useClickable();
const { formatNumber, formatPercentage } = useFormatters();

const detailRouterArguments = computed(() => ({
  name: "fieldCheckDetail",
  params: {
    path: props.check.path,
    datasetId: datasetStore.datasetId,
  },
}));
</script>

<style scoped lang="scss">

tbody tr {
    cursor: pointer;
}

.field_check_result {
    color: #4a4a4a;
    font-family: $font-family-bold;
    font-size: 16px;
    font-weight: 700;
    line-height: 16px;
}

.field_check_result_value {
    position: relative;
    top: 1px;
}

.field_check_count {
    color: $na_color;
    font-size: 12px;
    align-items: center;
}

.field_check_bar_envelope {
    padding-left: 10px;
    width: 100%;
    position: relative;
    top: -1px;
}
</style>
