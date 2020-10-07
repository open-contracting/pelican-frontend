<template>
    <dashboard-detail>
        <template v-if="loaded" v-slot:content>
            <div class="row">
                <div class="col col-10">
                    <h2>{{ $t("datasetLevel." + check.name + ".name") }}</h2>
                </div>
                <div class="col col-2">
                    <span v-if="check.result == true" class="badge badge-pill ok_status">{{ $t("passed") }}</span>
                    <span v-if="check.result == false" class="badge badge-pill failed_status">{{ $t("failed") }}</span>
                </div>
            </div>
            <p class="description" v-html=" $t('datasetLevel.' + check.name + '.description_long')"></p>

            <div class="result_box">
                <div v-if="checkType == 'bar'">
                    <BarChartBig :check="check"></BarChartBig>
                </div>

                <div v-if="checkType == 'unique'">{{ $t("datasetLevel.unique.ok") }}</div>

                <div v-if="checkType == 'donut'">
                    <table class="table table-borderless table-sm">
                        <tbody>
                            <tr v-for="share in shares" v-bind:key="share[0]">
                                <td class="text-right label">
                                    <span class="check_name">{{ share[0] }}</span>
                                </td>
                                <td class="text-right">
                                    <InlineBar
                                        :count="share[1]['count']"
                                        :percentage="share[1]['share'] * 100"
                                        :state="'reg'"
                                        showCount="true"
                                    />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-if="checkType == 'top3'">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>{{ $t("datasetLevel.top3.value") }}</th>
                                <th class="text-center">{{ $t("datasetLevel.top3.share") }}</th>
                                <th class="text-center">{{ $t("datasetLevel.top3.count") }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in check.meta.most_frequent" v-bind:key="index">
                                <td>{{ item.value_str }}</td>
                                <td class="text-right numeric">{{ item.share | formatPercentage2D }}</td>
                                <td class="text-right numeric">{{ item.count | formatNumber }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-if="checkType == 'numeric'">
                    <div class="row text-center">
                        <div class="numeric_result color_ok col-4">
                            <div class="check_numeric_value">{{ check.meta.total_passed }}</div>
                            {{ $t("datasetLevel.numeric.passed") }}
                        </div>

                        <div class="numeric_result color_failed col-4">
                            <div class="check_numeric_value">{{ check.meta.total_processed - check.meta.total_passed }}</div>
                            {{ $t("datasetLevel.numeric.failed") }}
                        </div>

                        <div class="numeric_result color_na col-4">
                            <div class="check_numeric_value">{{ check.meta.total_processed }}</div>
                            {{ $t("datasetLevel.numeric.processed") }}
                        </div>
                    </div>
                </div>

                <div v-if="checkType == 'biggest_share'" class="biggest_share">
                    <div class="row text-left">
                        <div class="col-7 specifics">
                            <span v-for="(item, index) in check.meta.specifics" v-bind:key="index">
                                <h3>{{ index }}</h3>
                                <p class="specifics_values">{{ item }}</p>
                            </span>
                        </div>

                        <div class="numeric_result col-5">
                            <div class="row">
                                <div
                                    class="col col-12 text-center total_share"
                                    v-bind:class="{ color_failed: check.result == false, color_ok: check.result == true }"
                                >{{ check.meta.ocid_share * 100 | formatPercentage2D }}</div>
                            </div>
                            <div class="row">
                                <div
                                    class="col col-12 text-center ocid_count"
                                >{{ check.meta.ocid_count | formatNumber }}&nbsp;{{ $t("datasetLevel.from") }}&nbsp;{{ check.meta.total_ocid_count | formatNumber }} {{ $t("ocids") }}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="checkType == 'single_value_share'" class="single_value_share">
                    <div class="row text-center">
                        <BarChartSingleValue :check="check" :showCount="true"></BarChartSingleValue>
                    </div>
                </div>
            </div>

            <ExampleBoxes
                :exampleSections="exampleSections"
                v-on:preview="preview"
                :loaded="true"
                :previewDisabled="loadingPreviewData"
            />
        </template>

        <template v-slot:preview>
            <h5>{{ $t("preview.metadata") }}</h5>
            <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewMetadata"></vue-json-pretty>

            <div class="divider">&nbsp;</div>
            
            <span v-if="loadingPreviewData">
                <div class="result_box loader text-center">
                    <div class="spinner">
                        <b-spinner variant="primary" style="width: 4rem; height: 4rem;" type="grow" class="spinner"></b-spinner>
                    </div>
                    {{ $t("loader.data") }}
                </div>
            </span>

            <span v-else-if="previewData">
                <h5>{{ $t("preview.ocdsData") }}</h5>
                <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewData"></vue-json-pretty>
            </span>
        </template>
    </dashboard-detail>
</template>

<script>
import BarChartBig from "@/components/BarChartBig";
import BarChartSingleValue from "@/components/BarChartSingleValue";
import InlineBar from "@/components/InlineBar";
import VueJsonPretty from "vue-json-pretty";
import datasetMixin from "@/plugins/datasetMixins.js";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";

export default {
    name: "datasetCheckDetail",
    mixins: [datasetMixin],
    data: function() {
        return {
            check: null,
            previewDataItemId: null,
            previewMetadata: null,
            exampleSections: null,
            loadingPreviewData: false
        };
    },
    components: {
        BarChartBig,
        VueJsonPretty,
        DashboardDetail,
        InlineBar,
        ExampleBoxes,
        BarChartSingleValue
    },
    created() {
        this.loadCheck();
    },
    methods: {
        preview: function(itemId) {
            this.loadingPreviewData = true;
            this.$store.dispatch("loadDataItem", itemId).finally(() => {
                if (this.$store.getters.dataItemJSONLines(itemId) < 3000) {
                    this.previewDataItemId = itemId;
                } else {
                    this.$alert(this.$t("preview.cannotDisplay"), null, 'error');
                    this.previewDataItemId = null;
                }

                this.loadingPreviewData = false;
            });
        },
        loadCheck: function() {
            this.check = this.$store.getters.datasetLevelCheckByName(
                this.$route.params.check
            );

            if (this.check != null) {
                this.previewMetadata = this.check.meta;

                if (this.checkType == "donut") {
                    this.exampleSections = [];
                    for (var key in this.shares) {
                        if (this.shares[key][1].examples.length > 0) {
                            this.exampleSections.push({
                                header: this.shares[key][0],
                                examples: this.shares[key][1].examples
                            });
                        }
                    }
                }

                if (this.checkType == "bar") {
                    this.exampleSections = [];
                    for (var barKey in this.check.meta.examples) {
                        if (this.check.meta.examples[barKey].length > 0) {
                            this.exampleSections.push({
                                header: this.$t("datasetLevel.label_" + barKey),
                                examples: this.check.meta.examples[barKey]
                            });
                        }
                    }
                }

                if (this.checkType == "top3") {
                    this.exampleSections = [];
                    var mostFrequent = this.check.meta.most_frequent;
                    for (var topKey in mostFrequent) {
                        if (mostFrequent[topKey].examples.length > 0) {
                            this.exampleSections.push({
                                header: mostFrequent[topKey].value_str,
                                examples: mostFrequent[topKey].examples
                            });
                        }
                    }
                }

                if (this.checkType == "numeric") {
                    this.exampleSections = [];
                    var failed = this.check.meta.failed_examples;
                    var passed = this.check.meta.passed_examples;

                    if (failed.length > 0) {
                        this.exampleSections.push({
                            header: this.$t("datasetLevel.numeric.failedExamples"),
                            examples: failed
                        });
                    }

                    if (passed.length > 0) {
                        this.exampleSections.push({
                            header: this.$t("datasetLevel.numeric.passedExamples"),
                            examples: passed
                        });
                    }
                }

                if (
                    this.checkType == "biggest_share" ||
                    this.checkType == "single_value_share"
                ) {
                    this.exampleSections = [];
                    if (this.check.meta.examples.length > 0) {
                        this.exampleSections.push({
                            header: this.$t("datasetLevel.examples"),
                            examples: this.check.meta.examples
                        });
                    }
                }
            }
        }
    },
    computed: {
        previewData() {
            var result = this.$store.getters.dataItemById(
                this.previewDataItemId
            );

            if (result) {
                return result["data"];
            }

            return null;
        },
        loaded() {
            this.loadCheck();

            return this.check != null;
        }
    }
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
    font-size: 60px;
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