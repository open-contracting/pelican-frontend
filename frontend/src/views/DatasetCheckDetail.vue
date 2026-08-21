<template>
  <dashboard-detail>
    <template
      v-if="check"
      #content
    >
      <div class="row">
        <div class="col col-10">
          <h2>{{ $t("datasetLevel." + check.name + ".name") }}</h2>
        </div>
        <div class="col col-2 text-end">
          <span
            v-if="!reportOnly && check.result === true"
            class="badge rounded-pill ok_status"
          >{{ $t("passed") }}</span>
          <span
            v-if="!reportOnly && check.result === false"
            class="badge rounded-pill failed_status"
          >{{ $t("failed") }}</span>
        </div>
      </div>
      <p
        class="description"
        v-html="$t('datasetLevel.' + check.name + '.descriptionLong')"
      />

      <div
        v-if="check.meta.reason == null"
        class="result_box"
      >
        <div v-if="checkType === 'percentile'">
          <PercentileChart v-if="ticks" :check="check" :ticks="ticks" show-count />
        </div>

        <div v-else-if="checkType === 'code'">
          <CodeChart :check="check" :limit="false" />
        </div>

        <div v-else-if="checkType === 'top3'">
          <table class="table table-sm">
            <thead>
              <tr>
                <th>{{ $t("datasetLevel.top3.value") }}</th>
                <th class="text-center">
                  {{ $t("datasetLevel.top3.share") }}
                </th>
                <th class="text-center">
                  {{ $t("datasetLevel.top3.count") }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(item, index) in top3Meta.most_frequent"
                :key="index"
              >
                <td>{{ item.value_str }}</td>
                <td class="text-end numeric">
                  {{ formatPercentage2D(item.share) }}
                </td>
                <td class="text-end numeric">
                  {{ formatNumber(item.count) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else-if="checkType === 'numeric'">
          <div class="row text-center">
            <div class="numeric_result color_ok col-4">
              <div class="check_numeric_value">
                {{ formatNumber(numericMeta.total_passed) }}
              </div>
              {{ $t("datasetLevel.numeric.passed") }}
            </div>

            <div class="numeric_result color_failed col-4">
              <div class="check_numeric_value">
                {{ formatNumber(numericMeta.total_processed - numericMeta.total_passed) }}
              </div>
              {{ $t("datasetLevel.numeric.failed") }}
            </div>

            <div class="numeric_result color_na col-4">
              <div class="check_numeric_value">
                {{ formatNumber(numericMeta.total_processed) }}
              </div>
              {{ $t("datasetLevel.numeric.processed") }}
            </div>
          </div>
        </div>

        <div
          v-else-if="checkType === 'biggest_share'"
          class="biggest_share"
        >
          <div class="row text-start">
            <div class="col-7 specifics">
              <span
                v-for="(item, index) in biggestShareMeta.specifics"
                :key="index"
              >
                <h3>{{ index }}</h3>
                <p class="specifics_values">{{ item }}</p>
              </span>
            </div>

            <div class="numeric_result col-5">
              <div class="row">
                <div
                  class="col col-12 text-center total_share"
                  :class="{
                    color_failed: check.result === false,
                    color_ok: check.result === true
                  }"
                >
                  {{ formatPercentage2D(biggestShareMeta.ocid_share) }}
                </div>
              </div>
              <div class="row">
                <div class="col col-12 text-center ocid_count">
                  {{ $t("datasetLevel.ocid_share", { share: $n(biggestShareMeta.ocid_count), total: $n(biggestShareMeta.total_ocid_count) }) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="checkType === 'single_value_share'">
          <FrequencyChart v-if="ticks" :check="check" :ticks="ticks" show-count />
        </div>
      </div>

      <ExampleBoxes
        :example-sections="exampleSections"
        @preview="previewDataItem"
      />
    </template>

    <template #preview>
      <h5>{{ $t("preview.metadata") }}</h5>
      <vue-json-pretty
        :deep="3"
        :data="previewMetadata"
      />

      <div class="spacer" />

      <span v-if="loadingPreviewData">
        <div class="result_box loader text-center">
          <div class="spinner">
            <BSpinner
              variant="primary"
              style="width: 4rem; height: 4rem"
              type="grow"
              class="spinner"
            />
          </div>
          {{ $t("loader.data") }}
        </div>
      </span>

      <span v-else-if="previewData">
        <h5>{{ $t("preview.ocdsData") }}</h5>
        <vue-json-pretty
          :deep="2"
          :data="previewData"
        />
      </span>
    </template>
  </dashboard-detail>
</template>

<script setup lang="ts">
import { BSpinner } from "bootstrap-vue-next";
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import VueJsonPretty from "vue-json-pretty";
import { useRoute } from "vue-router";
import { useDatasetStore } from "@/stores/dataset.js";
import "vue-json-pretty/lib/styles.css";
import CodeChart from "@/components/CodeChart.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import FrequencyChart from "@/components/FrequencyChart.vue";
import PercentileChart from "@/components/PercentileChart.vue";
import { useDataItem } from "@/composables/useDataItem.js";
import { useFormatters } from "@/composables/useFormatters";
import { DATASET_CHECK_REPORT_ONLY, DATASET_CHECK_TICKS, DATASET_CHECK_TYPES } from "@/config.js";
import type {
  BiggestShareMeta,
  CodeMeta,
  DatasetLevelMeta,
  ExampleSection,
  JSONData,
  NumericMeta,
  PercentileMeta,
  Top3Meta,
} from "@/types.js";
import { orderedShares, withoutExamples } from "@/util.js";
import DashboardDetail from "./layouts/DashboardDetail.vue";

const { formatNumber, formatPercentage2D } = useFormatters();

const route = useRoute();
const datasetStore = useDatasetStore();
const { t } = useI18n();
const { previewDataItem, previewData, loadingPreviewData } = useDataItem();

const check = computed(() => datasetStore.datasetLevelCheckByName(String(route.params.check)));
const previewMetadata = computed(() => (check.value == null ? null : (withoutExamples(check.value.meta) as JSONData)));
const checkType = computed(() => (check.value == null ? undefined : DATASET_CHECK_TYPES[check.value.name]));
const reportOnly = computed(() => (check.value == null ? undefined : DATASET_CHECK_REPORT_ONLY[check.value.name]));
const ticks = computed(() => (check.value == null ? undefined : DATASET_CHECK_TICKS[check.value.name]));

// The template renders each of these in the branch for the check type whose meta has that shape.
const meta = computed<DatasetLevelMeta>(() => check.value?.meta ?? {});
const numericMeta = computed(() => meta.value as NumericMeta);
const top3Meta = computed(() => meta.value as Top3Meta);
const biggestShareMeta = computed(() => meta.value as BiggestShareMeta);

const exampleSections = computed(() => {
  const sections: ExampleSection[] = [];

  if (!check.value) {
    return sections;
  }

  if (checkType.value === "code") {
    for (const [code, share] of orderedShares((meta.value as CodeMeta).shares ?? {})) {
      if (share.examples.length > 0) {
        sections.push({
          header: code,
          examples: share.examples,
        });
      }
    }
  } else if (checkType.value === "percentile") {
    for (const [range, examples] of Object.entries((meta.value as PercentileMeta).examples ?? {})) {
      if (examples.length > 0) {
        sections.push({
          header: t(`datasetLevel.charts.label_${range}`),
          examples,
        });
      }
    }
  } else if (checkType.value === "top3") {
    for (const value of top3Meta.value.most_frequent ?? []) {
      if (value.examples.length > 0) {
        sections.push({
          header: value.value_str,
          examples: value.examples,
        });
      }
    }
  } else if (checkType.value === "numeric") {
    if (numericMeta.value.failed_examples?.length) {
      sections.push({
        header: t("datasetLevel.numeric.failedExamples"),
        examples: numericMeta.value.failed_examples,
      });
    }

    if (numericMeta.value.passed_examples?.length) {
      sections.push({
        header: t("datasetLevel.numeric.passedExamples"),
        examples: numericMeta.value.passed_examples,
      });
    }
  } else if (checkType.value === "biggest_share" || checkType.value === "single_value_share") {
    if (biggestShareMeta.value.examples?.length) {
      sections.push({
        header: t("datasetLevel.examples"),
        examples: biggestShareMeta.value.examples,
      });
    }
  }

  return sections;
});
</script>

<style scoped lang="scss">
@import "@/scss/variables";

.ok_status {
    background-color: $ok_color;
    color: white;
    font-size: 15px;
    padding: 10px;
}

.failed_status {
    background-color: $failed_color;
    color: white;
    font-size: 15px;
    padding: 10px;
}

.label {
    padding-top: 6px;
}

.numeric_result {
    display: inline-block;
}

.check_numeric_value {
    display: block;
    font-size: 40px;
    font-weight: 700;
}

.check_numeric_count {
    font-size: 30px;
    font-weight: 700;
}

.biggest_share .total_share {
    font-size: 70px;
    font-weight: 700;
}

.biggest_share .ocid_count {
    font-size: 12px;
    font-weight: 700;
}

.biggest_share .specifics_values {
    overflow-wrap: break-word;
}
</style>
