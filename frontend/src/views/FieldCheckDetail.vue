<template>
    <dashboard-detail>
        <template v-if="check" v-slot:content>
            <h2>{{ $t("fieldDetail.path") }}: {{ check.path }}</h2>

            <template v-for="(c, k) in check.coverage.checks">
                <h5 :key="k">
                    &ldquo;{{ $t("fieldDetail.coverage." + k + ".count_header") }}&rdquo; {{ $t("fieldDetail.checked") }}:
                    &nbsp;
                    <span
                        class="bold"
                    >{{ c.passed_count + c.failed_count | formatNumber }}</span>
                    &nbsp;
                    <Tooltip :text="$t('fieldDetail.coverage.' + k + '.count_header_tooltip')"></Tooltip>
                </h5>
                <CheckDetailResultBox :key="k + '-box'" :check="c" ok failed />
            </template>

            <template v-for="(c, k) in check.quality.checks">
                <h5 :key="k">
                    &ldquo;{{ $t("fieldDetail.quality." + k + ".count_header") }}&rdquo; {{ $t("fieldDetail.checked") }}:
                    &nbsp;
                    <span
                        class="bold"
                    >{{ c.passed_count + c.failed_count | formatNumber }}</span>
                    &nbsp;
                    <Tooltip :text="$t('fieldDetail.quality.' + k + '.count_header_tooltip')"></Tooltip>
                </h5>
                <CheckDetailResultBox :key="k + '-box'" :check="c" ok failed />
            </template>

            <ExampleBoxes
                :examples="failedCoverageExamples.concat(failedQualityExamples).concat(passedExamples)"
                v-on:preview="preview"
                :loaded="check.examples_filled"
                :previewDisabled="loadingPreviewData"
            />
        </template>

        <template v-slot:preview>
            <span v-if="previewMetaData">
                <h5>{{ $t("preview.metadata") }}</h5>
                <vue-json-pretty :highlightMouseoverNode="true" :data="previewMetaData"></vue-json-pretty>
            </span>

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
import VueJsonPretty from "vue-json-pretty";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import Tooltip from "@/components/Tooltip.vue";

export default {
    name: "fieldCheckDetail",
    data: function() {
        return {
            previewMetaData: null,
            previewDataItemId: null,
            loadingPreviewData: false
        };
    },
    components: {
        VueJsonPretty,
        DashboardDetail,
        ExampleBoxes,
        CheckDetailResultBox,
        Tooltip
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

            var result = this.allExamples.find(function(element) {
                return element.meta.item_id == itemId;
            });

            if (result) {
                this.previewMetaData = result.result;
            }
        },
    },
    computed: {
        allExamples() {
            if (!this.check) {
                return [];
            }

            var allExamples = [];
            if (this.check.coverage) {
                allExamples = allExamples.concat(
                    this.check.coverage.failed_examples
                );
                allExamples = allExamples.concat(
                    this.check.coverage.passed_examples
                );
            }
            if (this.check.quality) {
                allExamples = allExamples.concat(
                    this.check.quality.failed_examples
                );
                allExamples = allExamples.concat(
                    this.check.quality.passed_examples
                );
            }

            return allExamples;
        },
        check() {
            return this.$store.getters.fieldLevelCheckByPath(
                this.$route.params.path
            );
        },
        failedCoverageExamples() {
            var examples = [];
            if (this.check != [] && this.check.path != undefined) {
                var failed = this.check.coverage.failed_examples;

                if (failed != undefined && failed.length > 0) {
                    examples.push([
                        this.$t("fieldDetail.coverage.label") +
                            " - " +
                            this.$t("core.failedExamples"),
                        failed.map(function(val) {
                            return val.meta;
                        })
                    ]);
                }
            }

            return examples;
        },
        failedQualityExamples() {
            var examples = [];
            if (this.check != [] && this.check.path != undefined) {
                var failed = this.check.quality.failed_examples;

                if (failed != undefined && failed.length > 0) {
                    examples.push([
                        this.$t("fieldDetail.quality.label") +
                            " - " +
                            this.$t("core.failedExamples"),
                        failed.map(function(val) {
                            return val.meta;
                        })
                    ]);
                }
            }

            return examples;
        },
        passedExamples() {
            var examples = [];
            if (this.check != [] && this.check.path != undefined) {
                var passed = [];
                if (this.check.coverage.passed_examples != undefined) {
                    passed = passed.concat(this.check.coverage.passed_examples);
                }

                if (this.check.quality.passed_examples != undefined) {
                    passed = passed.concat(this.check.quality.passed_examples);
                }

                if (passed != undefined && passed.length > 0) {
                    examples.push([
                        this.$t("core.passedExamples"),
                        passed.map(function(val) {
                            return val.meta;
                        })
                    ]);
                }
            }

            return examples;
        },
        previewData() {
            var result = this.$store.getters.dataItemById(
                this.previewDataItemId
            );

            if (result) {
                return result["data"];
            }

            return null;
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.label {
    padding-top: 6px;
}
</style>