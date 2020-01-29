<template>
    <dashboard-detail>
        <template v-if="check" v-slot:content>
            <h2 v-if="check">{{ $t("resourceLevel." + check.name + ".name") }}</h2>
            <p class="description" v-html="$t('resourceLevel.' + check.name + '.description')"></p>

            <h5>
                {{ $t("resourceLevel.count_header") }}
                <span class="bold">{{ check.passed_count + check.failed_count + check.undefined_count | formatNumber }}</span>
                &nbsp;
                <Tooltip :text="$t('resourceLevel.count_header_tooltip')"></Tooltip>
            </h5>

            <CheckDetailResultBox :check="check" ok failed na />

            <h5>
                {{ $t("resourceLevel.application_count_header") }}
                <span class="bold">{{ check.individual_application_count | formatNumber }}</span>&nbsp;
                <Tooltip :text="$t('resourceLevel.application_count_header_tooltip')"></Tooltip>
            </h5>
            <CheckDetailResultBox :check="check" individualPass individualNonPass />

            <ExampleBoxes :examples="examples" v-on:preview="preview" :loaded="check.examples_filled" :previewDisabled="loadingPreviewData"></ExampleBoxes>
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
                <h5>{{ $t("preview.ocds_data") }}</h5>
                <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewData"></vue-json-pretty>
            </span>

        </template>
    </dashboard-detail>
</template>

<script>
import VueJsonPretty from "vue-json-pretty";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import resourceCheckMixin from "@/plugins/resourceCheckMixins.js";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import Tooltip from "@/components/Tooltip.vue";

export default {
    name: "resourceCheckDetail",
    mixins: [resourceCheckMixin],
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
                this.loadingPreviewData = false;
            });
            this.previewDataItemId = itemId;

            var allExamples = [];
            allExamples = allExamples.concat(this.check.failed_examples);
            allExamples = allExamples.concat(this.check.passed_examples);
            allExamples = allExamples.concat(this.check.undefined_examples);

            var result = allExamples.find(function(element) {
                return element.meta.item_id == itemId;
            });
            if (result) {
                this.previewMetaData = result.result;
            }
        }
    },
    computed: {
        check() {
            var stats = this.$store.getters.resourceLevelStats;
            if (stats != null) {
                return stats.find(
                    item => item.name === this.$route.params.check
                );
            } else {
                return null;
            }
        },
        examples() {
            var examples = [];
            if (this.check != [] && this.check.name != undefined) {
                var failed = this.check.failed_examples;
                var passed = this.check.passed_examples;
                var undefined = this.check.undefined_examples;

                if (failed.length > 0) {
                    examples.push([
                        this.$t("core.failedExamples"),
                        failed.map(function(val) {
                            return val.meta;
                        })
                    ]);
                }

                if (passed.length > 0) {
                    examples.push([
                        this.$t("core.passedExamples"),
                        passed.map(function(val) {
                            return val.meta;
                        })
                    ]);
                }

                if (undefined.length > 0) {
                    examples.push([
                        this.$t("core.undefinedExamples"),
                        undefined.map(function(val) {
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
</style>