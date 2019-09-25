<template>
    <dashboard-detail>
        <template v-if="check" v-slot:content>
            <h2 v-if="check">{{ $t("resourceLevel." + check.name + ".name") }}</h2>
            <p v-if="check">{{ $t("resourceLevel." + check.name + ".description") }}</p>

            <h5>{{ $t("resourceLevel.count_header") }} {{ check.passed_count + check.failed_count + check.undefined_count | formatNumber }}</h5>
            <CheckDetailResultBox :check="check" ok failed na />

            <h5>{{ $t("resourceLevel.application_count_header") }} {{ applicationCount() | formatNumber }}</h5>
            <CheckDetailResultBox :check="check" pass nonPass />

            <ExampleBoxes :examples="examples" v-on:preview="preview" :loaded="check.examples_filled"></ExampleBoxes>
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
import resourceCheckMixin from "@/plugins/resourceCheckMixins.js";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";

export default {
    name: "resourceCheckDetail",
    mixins: [resourceCheckMixin],
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
            return this.$store.getters.dataItemById(this.previewDataItemId);
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";
</style>