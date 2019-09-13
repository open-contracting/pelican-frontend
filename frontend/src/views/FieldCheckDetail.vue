<template>
    <dashboard-detail>
        <template v-if="check" v-slot:content>
            <h3>{{ $t("header").toUpperCase() }}</h3>
            <h2>{{ $t("fieldLevel." + check.path + ".name") }}</h2>
            <p>{{ $t("fieldLevel." + check.path + ".description") }}</p>

            <template v-for="(c, k) in check.coverage.checks">
                <h5 :key="k">{{ $t("fieldLevel.coverage." + k + ".count_header") }}: {{ c.passed_count + c.failed_count + c.undefined_count | formatNumber }}</h5>
                <CheckDetailResultBox :key="k + '-box'" :check="c" ok failed />
            </template>

            <template v-for="(c, k) in check.quality.checks">
                <h5 :key="k">{{ $t("fieldLevel.quality." + k + ".count_header") }}: {{ c.passed_count + c.failed_count + c.undefined_count | formatNumber }}</h5>
                <CheckDetailResultBox :key="k + '-box'" :check="c" ok failed />
            </template>

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
    components: { VueJsonPretty, DashboardDetail, ExampleBoxes, CheckDetailResultBox },
    methods: {
        preview: function(itemId) {
            // this.$store.dispatch("loadDataItem", itemId);
            // this.previewDataItemId = itemId;

            // var allExamples = [];
            // allExamples = allExamples.concat(this.check.failed_examples);
            // allExamples = allExamples.concat(this.check.passed_examples);
            // allExamples = allExamples.concat(this.check.undefined_examples);

            // var result = allExamples.find(function(element) {
            //     return element.meta.item_id == itemId;
            // });
            // if (result) {
            //     this.previewMetaData = result.result;
            // }
        }
    },
    computed: {
        check() {
            return this.$store.getters.fieldLevelCheckByPath(this.$route.params.path)
        },
        examples() {
            var examples = [];
            if (this.check != [] && this.check.path != undefined) {
                var failed = this.check.coverage.failed_examples;
                var passed = this.check.coverage.passed_examples;

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