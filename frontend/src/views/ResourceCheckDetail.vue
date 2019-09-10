<template>
    <dashboard-detail>
        <template v-slot:content>
            <h3>{{ $t("header").toUpperCase() }}</h3>
            <h2>{{ $t("resourceLevel." + check.name + ".name") }}</h2>
            <p>{{ $t("resourceLevel." + check.name + ".description") }}</p>

            <h5>{{ $t("resourceLevel.count_header") }} {{ check.passed_count + check.failed_count + check.undefined_count | formatNumber }}</h5>
            <div class="result_box">
                <table class="table table-borderless table-sm">
                    <tbody>
                        <tr class="d-flex">
                            <td class="col-3 text-right label">
                                <span class="check_name">{{ $t("passed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.passed_count" :percentage="okPercentage" :state="'ok'" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-3 text-right label">
                                <span class="check_name">{{ $t("failed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.failed_count" :percentage="failedPercentage" :state="'failed'" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-3 text-right label">
                                <span class="check_name">{{ $t("notAvailable") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.undefined_count" :percentage="naPercentage" :state="'na'" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h5>{{ $t("resourceLevel.application_count_header") }} {{ applicationCount() | formatNumber }}</h5>
            <div class="result_box">
                <table class="table table-borderless table-sm">
                    <tbody>
                        <tr class="d-flex">
                            <td class="col-3 text-right label">
                                <span class="check_name">{{ $t("passed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.passed_count" :percentage="passPercentage" :state="'ok'" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-3 text-right label">
                                <span class="check_name">{{ $t("failed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.failed_count" :percentage="nonpassPercentage" :state="'failed'" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <ExampleBoxes :examples="examples" v-on:preview="preview"></ExampleBoxes>
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
import InlineBar from "@/components/InlineBar";
import VueJsonPretty from "vue-json-pretty";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import resourceCheckMixin from "@/plugins/resourceCheckMixins.js";
import ExampleBoxes from "@/components/ExampleBoxes.vue";

export default {
    name: "resourceCheckDetail",
    mixins: [resourceCheckMixin],
    data: function() {
        return {
            check: null,
            previewMetaData: null,
            previewDataItemId: null
        };
    },
    components: { InlineBar, VueJsonPretty, DashboardDetail, ExampleBoxes },
    created() {
        this.$store.dispatch('loadResourceLevelCheckDetail', this.$route.params.check);
        this.check = this.$store.getters.resourceLevelCheckByName(
            this.$route.params.check
        );

        // if (this.check.failed_examples.length > 0) {
        //     this.previewMetadata = this.check.examples.failed[0].meta;
        //     this.previewData = this.check.examples.failed[0].data;
        //     this.selectedKey = 0;
        //     this.selectedSection = "failed";
        // }
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
        examples() {
            var examples = [];
            var failed = this.check.failed_examples;
            var passed = this.check.passed_examples;
            var undefined = this.check.undefined_examples;

            if (failed.length > 0) {
                examples.push([
                    this.$t("core.failedExamples"),
                    failed.map(function(val){
                        return val.meta;
                    })
                ]);
            }

            if (passed.length > 0) {
                examples.push([
                    this.$t("core.passedExamples"),
                    passed.map(function(val){
                        return val.meta;
                    })
                ]);
            }

            if (undefined.length > 0) {
                examples.push([
                    this.$t("core.undefinedExamples"),
                    undefined.map(function(val){
                        return val.meta;
                    })
                ]);
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