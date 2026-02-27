<template>
  <dashboard-detail>
    <template
      v-if="loaded"
      #content
    >
      <div class="row">
        <div class="col col-10">
          <h2>{{ $t("datasetLevel." + check.name + ".name") }}</h2>
        </div>
        <div class="col col-2">
          <span
            v-if="!reportOnly && check.result == true"
            class="badge rounded-pill ok_status"
          >{{ $t("passed") }}</span>
          <span
            v-if="!reportOnly && check.result == false"
            class="badge rounded-pill failed_status"
          >{{ $t("failed") }}</span>
        </div>
      </div>
      <p
        class="description"
        v-html="$t('datasetLevel.' + check.name + '.description_long')"
      />

      <div class="result_box">
        <div v-if="checkType == 'bar'">
          <BarChartBig :check="check" :ticks="ticks" />
        </div>

        <div v-if="checkType == 'unique'">
          {{ $t("datasetLevel.unique.ok") }}
        </div>

        <div v-if="checkType == 'donut'">
          <DonutChart :check="check" :limit="false" />
        </div>

        <div v-if="checkType == 'top3'">
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
                v-for="(item, index) in check.meta.most_frequent"
                :key="index"
              >
                <td>{{ item.value_str }}</td>
                <td class="text-end numeric">
                  {{ $filters.formatPercentage2D(item.share * 100) }}
                </td>
                <td class="text-end numeric">
                  {{ $filters.formatNumber(item.count) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="checkType == 'numeric'">
          <div class="row text-center">
            <div class="numeric_result color_ok col-4">
              <div class="check_numeric_value">
                {{ $filters.formatNumber(check.meta.total_passed) }}
              </div>
              {{ $t("datasetLevel.numeric.passed") }}
            </div>

            <div class="numeric_result color_failed col-4">
              <div class="check_numeric_value">
                {{ $filters.formatNumber(check.meta.total_processed - check.meta.total_passed) }}
              </div>
              {{ $t("datasetLevel.numeric.failed") }}
            </div>

            <div class="numeric_result color_na col-4">
              <div class="check_numeric_value">
                {{ $filters.formatNumber(check.meta.total_processed) }}
              </div>
              {{ $t("datasetLevel.numeric.processed") }}
            </div>
          </div>
        </div>

        <div
          v-if="checkType == 'biggest_share'"
          class="biggest_share"
        >
          <div class="row text-start">
            <div class="col-7 specifics">
              <span
                v-for="(item, index) in check.meta.specifics"
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
                    color_failed: check.result == false,
                    color_ok: check.result == true
                  }"
                >
                  {{ $filters.formatPercentage2D(check.meta.ocid_share * 100) }}
                </div>
              </div>
              <div class="row">
                <div class="col col-12 text-center ocid_count">
                  {{ $t("datasetLevel.ocid_share", { share: $n(check.meta.ocid_count), total: $n(check.meta.total_ocid_count) }) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="checkType == 'single_value_share'"
          class="single_value_share"
        >
          <div class="row text-center">
            <BarChartSingleValue
              :check="check"
              :show-count="true"
            />
          </div>
        </div>
      </div>

      <ExampleBoxes
        :example-sections="exampleSections"
        :loaded="true"
        :preview-disabled="loadingPreviewData"
        @preview="preview"
      />
    </template>

    <template #preview>
      <h5>{{ $t("preview.metadata") }}</h5>
      <vue-json-pretty
        :deep="3"
        :data="previewMetadata"
      />

      <div class="divider">
&nbsp;
      </div>

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

<script setup>
import { BSpinner } from "bootstrap-vue-next";
import { computed, onBeforeMount, ref } from "vue";
import { useI18n } from "vue-i18n";
import VueJsonPretty from "vue-json-pretty";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import "vue-json-pretty/lib/styles.css";
import BarChartBig from "@/components/BarChartBig.vue";
import BarChartSingleValue from "@/components/BarChartSingleValue.vue";
import DonutChart from "@/components/DonutChart.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import { CHECK_TICKS, CHECK_TYPES, REPORT_ONLY_CHECKS } from "@/config.js";
import { orderedShares } from "@/util.js";
import DashboardDetail from "./layouts/DashboardDetail.vue";

const route = useRoute();
const store = useStore();
const { t } = useI18n();

const check = ref(null);
const previewDataItemId = ref(null);
const previewMetadata = ref(null);
const exampleSections = ref(null);
const loadingPreviewData = ref(false);

const checkType = computed(() => CHECK_TYPES[check.value?.name]);
const reportOnly = computed(() => REPORT_ONLY_CHECKS[check.value?.name]);
const ticks = computed(() => CHECK_TICKS[check.value?.name]);
const previewData = computed(() => store.getters.dataItemById(previewDataItemId.value)?.data);
const loaded = computed(() => {
    loadCheck();
    return check.value != null;
});

function preview(itemId) {
    loadingPreviewData.value = true;
    store.dispatch("loadDataItem", itemId).finally(() => {
        if (store.getters.dataItemJSONLines(itemId) < 3000) {
            previewDataItemId.value = itemId;
        } else {
            // Toast handled by component
            previewDataItemId.value = null;
        }
        loadingPreviewData.value = false;
    });
}

function loadCheck() {
    check.value = store.getters.datasetLevelCheckByName(route.params.check);

    if (check.value != null) {
        previewMetadata.value = check.value.meta;

        if (checkType.value === "donut") {
            exampleSections.value = [];
            const shares = orderedShares(check.value.meta.shares);
            for (const key in shares) {
                if (shares[key][1].examples.length > 0) {
                    exampleSections.value.push({
                        header: shares[key][0],
                        examples: shares[key][1].examples,
                    });
                }
            }
        }

        if (checkType.value === "bar") {
            exampleSections.value = [];
            for (const barKey in check.value.meta.examples) {
                if (check.value.meta.examples[barKey].length > 0) {
                    exampleSections.value.push({
                        header: t(`datasetLevel.charts.label_${barKey}`),
                        examples: check.value.meta.examples[barKey],
                    });
                }
            }
        }

        if (checkType.value === "top3") {
            exampleSections.value = [];
            const mostFrequent = check.value.meta.most_frequent;
            for (const topKey in mostFrequent) {
                if (mostFrequent[topKey].examples.length > 0) {
                    exampleSections.value.push({
                        header: mostFrequent[topKey].value_str,
                        examples: mostFrequent[topKey].examples,
                    });
                }
            }
        }

        if (checkType.value === "numeric") {
            exampleSections.value = [];
            const failed = check.value.meta.failed_examples;
            const passed = check.value.meta.passed_examples;

            if (failed.length > 0) {
                exampleSections.value.push({
                    header: t("datasetLevel.numeric.failedExamples"),
                    examples: failed,
                });
            }

            if (passed.length > 0) {
                exampleSections.value.push({
                    header: t("datasetLevel.numeric.passedExamples"),
                    examples: passed,
                });
            }
        }

        if (checkType.value === "biggest_share" || checkType.value === "single_value_share") {
            exampleSections.value = [];
            if (check.value.meta.examples.length > 0) {
                exampleSections.value.push({
                    header: t("datasetLevel.examples"),
                    examples: check.value.meta.examples,
                });
            }
        }
    }
}

onBeforeMount(() => {
    loadCheck();
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
