<template>
    <dashboard-detail>
        <template v-if="check" v-slot:content>
            <h3>{{ $t("header") }}</h3>
            <h2>{{ $t("fieldDetail." + check.path + ".name") }}</h2>
            <p class="description">{{ $t("fieldDetail." + check.path + ".description") }}</p>

            <template v-for="(c, k) in check.coverage.checks">
                <h5 :key="k">
                    &ldquo;{{ $t("fieldDetail.coverage." + k + ".count_header") }}&rdquo; {{ $t("fieldDetail.checks") }}:
                    {{ c.passed_count + c.failed_count | formatNumber }}
                </h5>
                <CheckDetailResultBox :key="k + '-box'" :check="c" ok failed />
            </template>

            <template v-for="(c, k) in check.quality.checks">
                <h5 :key="k">
                    &ldquo;{{ $t("fieldDetail.quality." + k + ".count_header") }}&rdquo; {{ $t("fieldDetail.checks") }}:
                    {{ c.passed_count + c.failed_count | formatNumber }}
                </h5>
                <CheckDetailResultBox :key="k + '-box'" :check="c" ok failed />
            </template>

            <ExampleBoxes
                :examples="failedCoverageExamples.concat(failedQualityExamples).concat(passedExamples)"
                v-on:preview="preview"
                :loaded="check.examples_filled"
            />
        </template>

        <template v-slot:preview>
            <h5>{{ $t("preview.metadata") }}</h5>
            <vue-json-pretty :highlightMouseoverNode="true" :data="previewMetaData"></vue-json-pretty>

            <div class="divider">&nbsp;</div>

            <h5>{{ $t("preview.ocds_data") }}</h5>
            <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewData"></vue-json-pretty>
        </template>
    </dashboard-detail>
</template>

<script>
import VueJsonPretty from "vue-json-pretty";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";

export default {
    name: "fieldCheckDetail",
    data: function() {
        return {
            previewMetaData: null,
            previewDataItemId: null
        };
    },
    components: {
        VueJsonPretty,
        DashboardDetail,
        ExampleBoxes,
        CheckDetailResultBox
    },
    methods: {
        preview: function(itemId) {
            this.$store.dispatch("loadDataItem", itemId);
            this.previewDataItemId = itemId;

            var result = this.allExamples.find(function(element) {
                return element.meta.item_id == itemId;
            });

            if (result) {
                this.previewMetaData = result.result;
            }
        }
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

                if (failed.length > 0) {
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

                if (failed.length > 0) {
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
                var passed = this.check.coverage.passed_examples.concat(
                    this.check.quality.passed_examples
                );

                if (passed.length > 0) {
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
            return this.$store.getters.dataItemById(this.previewDataItemId);
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