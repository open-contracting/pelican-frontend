<template>
  <dashboard-detail>
    <template
      v-if="check"
      #content
    >
      <h2>{{ $t("fieldDetail.path") }}: {{ check.path }}</h2>

      <template v-for="(c, k) in check.coverage.checks">
        <h5 :key="k">
          <span class="category_name"> {{ $t("fieldDetail.coverage.label") }}: </span>
          &ldquo;{{ $t("fieldDetail.coverage." + k + ".count_header") }}&rdquo;
          {{ $t("fieldDetail.checked") }}: &nbsp;
          <span class="bold">
            {{ (c.passed_count + c.failed_count) | formatNumber }}
          </span>
                    &nbsp;
          <Tooltip :text="$t('fieldDetail.coverage.' + k + '.count_header_tooltip')" />
        </h5>
        <CheckDetailResultBox
          :key="k + '-box'"
          :check="c"
          ok
          failed
        />
      </template>

      <template v-for="(c, k) in check.quality.checks">
        <h5 :key="k">
          <span class="category_name"> {{ $t("fieldDetail.quality.label") }}: </span>
          &ldquo;{{ $t("fieldDetail.quality." + k + ".count_header") }}&rdquo;
          {{ $t("fieldDetail.checked") }}: &nbsp;
          <span class="bold">
            {{ (c.passed_count + c.failed_count) | formatNumber }}
          </span>
                    &nbsp;
          <Tooltip :text="$t('fieldDetail.quality.' + k + '.count_header_tooltip')" />
        </h5>
        <CheckDetailResultBox
          :key="k + '-box'"
          :check="c"
          ok
          failed
        />
      </template>

      <ExampleBoxes
        :example-sections="exampleSections"
        :loaded="check.examples_filled"
        :preview-disabled="loadingPreviewData"
        @preview="preview"
      />
    </template>

    <template #preview>
      <span v-if="previewMetaData">
        <h5>{{ $t("preview.metadata") }}</h5>
        <vue-json-pretty
          :highlight-mouseover-node="true"
          :data="previewMetaData"
        />
      </span>

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
import VueJsonPretty from "vue-json-pretty";
import 'vue-json-pretty/lib/styles.css';
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import Tooltip from "@/components/Tooltip.vue";

export default {
    name: "FieldCheckDetail",
    components: {
        VueJsonPretty,
        DashboardDetail,
        ExampleBoxes,
        CheckDetailResultBox,
        Tooltip
    },
    data: function () {
        return {
            previewMetaData: null,
            previewDataItemId: null,
            loadingPreviewData: false
        };
    },
    computed: {
        allExamples() {
            if (!this.check) {
                return [];
            }

            var allExamples = [];
            if (this.check.coverage) {
                Object.values(this.check.coverage.checks).forEach(value => {
                    allExamples = allExamples.concat(value.failed_examples);
                });
                allExamples = allExamples.concat(this.check.coverage.passed_examples);
            }
            if (this.check.quality) {
                Object.values(this.check.quality.checks).forEach(value => {
                    allExamples = allExamples.concat(value.failed_examples);
                });
                allExamples = allExamples.concat(this.check.quality.passed_examples);
            }

            return allExamples;
        },
        check() {
            return this.$store.getters.fieldLevelCheckByPath(this.$route.params.path);
        },
        exampleSections() {
            var exampleSections = [];
            if (this.check != [] && this.check.path != undefined) {
                Object.keys(this.check.coverage.checks).forEach(key => {
                    var failed = this.check.coverage.checks[key].failed_examples;
                    if (failed != undefined && failed.length > 0) {
                        exampleSections.push({
                            prefix: this.$t("fieldDetail.coverage.failureSamplesPrefix"),
                            header: this.$t("fieldDetail.coverage." + key + ".count_header"),
                            examples: failed.map(val => val.meta)
                        });
                    }
                });

                Object.keys(this.check.quality.checks).forEach(key => {
                    var failed = this.check.quality.checks[key].failed_examples;
                    if (failed != undefined && failed.length > 0) {
                        exampleSections.push({
                            prefix: this.$t("fieldDetail.quality.failureSamplesPrefix"),
                            header: this.$t("fieldDetail.quality." + key + ".count_header"),
                            examples: failed.map(val => val.meta)
                        });
                    }
                });

                var passedSection = {
                    header: this.$t("core.passedExamples"),
                    examples: []
                };
                if (this.check.quality.passed_examples != undefined && this.check.quality.passed_examples.length > 0) {
                    passedSection.examples = this.check.quality.passed_examples.map(val => val.meta);
                } else if (
                    this.check.coverage.passed_examples != undefined &&
                    this.check.coverage.passed_examples.length > 0
                ) {
                    passedSection.examples = this.check.coverage.passed_examples.map(val => val.meta);
                }
                if (passedSection.examples.length > 0) {
                    exampleSections.push(passedSection);
                }
            }

            return exampleSections;
        },
        previewData() {
            var result = this.$store.getters.dataItemById(this.previewDataItemId);

            if (result) {
                return result["data"];
            }

            return null;
        }
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

            var result = this.allExamples.find(function (element) {
                return element.meta.item_id == itemId;
            });

            if (result) {
                this.previewMetaData = result.result;
            }
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.category_name {
    color: $headings-light-color;
    font-family: $font-family-thin;
}

.label {
    padding-top: 6px;
}
</style>
