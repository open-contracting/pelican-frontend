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
            class="badge badge-pill ok_status"
          >{{ $t("passed") }}</span>
          <span
            v-if="!reportOnly && check.result == false"
            class="badge badge-pill failed_status"
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
                <td class="text-right numeric">
                  {{ (item.share * 100) | formatPercentage2D }}
                </td>
                <td class="text-right numeric">
                  {{ item.count | formatNumber }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="checkType == 'numeric'">
          <div class="row text-center">
            <div class="numeric_result color_ok col-4">
              <div class="check_numeric_value">
                {{ check.meta.total_passed | formatNumber }}
              </div>
              {{ $t("datasetLevel.numeric.passed") }}
            </div>

            <div class="numeric_result color_failed col-4">
              <div class="check_numeric_value">
                {{ (check.meta.total_processed - check.meta.total_passed) | formatNumber }}
              </div>
              {{ $t("datasetLevel.numeric.failed") }}
            </div>

            <div class="numeric_result color_na col-4">
              <div class="check_numeric_value">
                {{ check.meta.total_processed | formatNumber }}
              </div>
              {{ $t("datasetLevel.numeric.processed") }}
            </div>
          </div>
        </div>

        <div
          v-if="checkType == 'biggest_share'"
          class="biggest_share"
        >
          <div class="row text-left">
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
                  {{ (check.meta.ocid_share * 100) | formatPercentage2D }}
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
        :highlight-mouseover-node="true"
        :deep="3"
        :data="previewMetadata"
      />

      <div class="divider">
&nbsp;
      </div>

      <span v-if="loadingPreviewData">
        <div class="result_box loader text-center">
          <div class="spinner">
            <b-spinner
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
          :highlight-mouseover-node="true"
          :deep="2"
          :data="previewData"
        />
      </span>
    </template>
  </dashboard-detail>
</template>

<script>
import "vue-json-pretty/lib/styles.css";
import BarChartBig from "@/components/BarChartBig.vue";
import BarChartSingleValue from "@/components/BarChartSingleValue.vue";
import DonutChart from "@/components/DonutChart.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import datasetMixin from "@/plugins/datasetMixins.js";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import VueJsonPretty from "vue-json-pretty";

export default {
    name: "DatasetCheckDetail",
    components: {
        DonutChart,
        BarChartBig,
        VueJsonPretty,
        DashboardDetail,
        ExampleBoxes,
        BarChartSingleValue,
    },
    mixins: [datasetMixin],
    data: () => ({
        check: null,
        previewDataItemId: null,
        previewMetadata: null,
        exampleSections: null,
        loadingPreviewData: false,
    }),
    computed: {
        previewData() {
            return this.$store.getters.dataItemById(this.previewDataItemId)?.data;
        },
        loaded() {
            this.loadCheck();

            return this.check != null;
        },
    },
    created() {
        this.loadCheck();
    },
    methods: {
        preview: function (itemId) {
            this.loadingPreviewData = true;
            this.$store.dispatch("loadDataItem", itemId).finally(() => {
                if (this.$store.getters.dataItemJSONLines(itemId) < 3000) {
                    this.previewDataItemId = itemId;
                } else {
                    this.$alert(this.$t("preview.cannotDisplay"), null, "error");
                    this.previewDataItemId = null;
                }

                this.loadingPreviewData = false;
            });
        },
        loadCheck: function () {
            this.check = this.$store.getters.datasetLevelCheckByName(this.$route.params.check);

            if (this.check != null) {
                this.previewMetadata = this.check.meta;

                if (this.checkType === "donut") {
                    this.exampleSections = [];
                    for (const key in this.shares) {
                        if (this.shares[key][1].examples.length > 0) {
                            this.exampleSections.push({
                                header: this.shares[key][0],
                                examples: this.shares[key][1].examples,
                            });
                        }
                    }
                }

                if (this.checkType === "bar") {
                    this.exampleSections = [];
                    for (const barKey in this.check.meta.examples) {
                        if (this.check.meta.examples[barKey].length > 0) {
                            this.exampleSections.push({
                                header: this.$t(`datasetLevel.charts.label_${barKey}`),
                                examples: this.check.meta.examples[barKey],
                            });
                        }
                    }
                }

                if (this.checkType === "top3") {
                    this.exampleSections = [];
                    const mostFrequent = this.check.meta.most_frequent;
                    for (const topKey in mostFrequent) {
                        if (mostFrequent[topKey].examples.length > 0) {
                            this.exampleSections.push({
                                header: mostFrequent[topKey].value_str,
                                examples: mostFrequent[topKey].examples,
                            });
                        }
                    }
                }

                if (this.checkType === "numeric") {
                    this.exampleSections = [];
                    const failed = this.check.meta.failed_examples;
                    const passed = this.check.meta.passed_examples;

                    if (failed.length > 0) {
                        this.exampleSections.push({
                            header: this.$t("datasetLevel.numeric.failedExamples"),
                            examples: failed,
                        });
                    }

                    if (passed.length > 0) {
                        this.exampleSections.push({
                            header: this.$t("datasetLevel.numeric.passedExamples"),
                            examples: passed,
                        });
                    }
                }

                if (this.checkType === "biggest_share" || this.checkType === "single_value_share") {
                    this.exampleSections = [];
                    if (this.check.meta.examples.length > 0) {
                        this.exampleSections.push({
                            header: this.$t("datasetLevel.examples"),
                            examples: this.check.meta.examples,
                        });
                    }
                }
            }
        },
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

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
