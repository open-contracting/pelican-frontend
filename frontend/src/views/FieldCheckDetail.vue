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
          &ldquo;{{ $t("fieldDetail.coverage." + k + ".count_header") }}&rdquo; &nbsp;
          <span class="bold">
            {{ (c.passed_count + c.failed_count) | formatNumber }}
          </span>
                    &nbsp;
          <Tooltip :text="$t('fieldDetail.coverage.' + k + '.count_header_tooltip')" />
        </h5>
        <CheckDetailResultBox
          :key="k + '-box'"
          :check="c"
          :passed-label="k == 'exists' ? 'fieldDetail.set' : undefined"
          :failed-label="k == 'exists' ? 'fieldDetail.notset' : undefined"
          ok
          failed
        />
      </template>

      <template v-for="(c, k) in check.quality.checks">
        <h5 :key="k">
          <span class="category_name"> {{ $t("fieldDetail.quality.label") }}: </span>
          &ldquo;{{ $t("fieldDetail.quality." + k + ".count_header") }}&rdquo; &nbsp;
          <span class="bold">
            {{ (c.passed_count + c.failed_count) | formatNumber }}
          </span>
                    &nbsp;
          <Tooltip :text="$t('fieldDetail.quality.' + k + '.count_header_tooltip')" />
        </h5>
        <CheckDetailResultBox
          :key="k + '-box'"
          :check="c"
          :classes="'quality'"
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
import "vue-json-pretty/lib/styles.css";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import Tooltip from "@/components/Tooltip.vue";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import VueJsonPretty from "vue-json-pretty";

export default {
    name: "FieldCheckDetail",
    components: {
        VueJsonPretty,
        DashboardDetail,
        ExampleBoxes,
        CheckDetailResultBox,
        Tooltip,
    },
    data: () => ({
        previewMetaData: null,
        previewDataItemId: null,
        loadingPreviewData: false,
    }),
    computed: {
        allExamples() {
            if (!this.check) {
                return [];
            }

            var allExamples = { coverage: [], quality: [] };
            if (this.check.coverage) {
                Object.values(this.check.coverage.checks).forEach((value) => {
                    allExamples.coverage = allExamples.coverage.concat(value.failed_examples);
                });
                allExamples.coverage = allExamples.coverage.concat(this.check.coverage.passed_examples);
            }
            if (this.check.quality) {
                Object.values(this.check.quality.checks).forEach((value) => {
                    allExamples.quality = allExamples.quality.concat(value.failed_examples);
                });
                allExamples.quality = allExamples.quality.concat(this.check.quality.passed_examples);
            }
            return allExamples;
        },
        check() {
            return this.$store.getters.fieldLevelCheckByPath(this.$route.params.path);
        },
        exampleSections() {
            var exampleSections = [];
            if (this.check !== [] && this.check.path !== undefined) {
                Object.keys(this.check.coverage.checks).forEach((key) => {
                    var failed = this.check.coverage.checks[key].failed_examples;
                    if (failed !== undefined && failed.length > 0) {
                        exampleSections.push({
                            id: `coverage_${key}`,
                            prefix: this.$t("fieldDetail.coverage.failureSamplesPrefix"),
                            header: this.$t(`fieldDetail.coverage.${key}.count_header`),
                            examples: failed.map((val) => val.meta),
                            group: "coverage",
                        });
                    }
                });

                Object.keys(this.check.quality.checks).forEach((key) => {
                    var failed = this.check.quality.checks[key].failed_examples;
                    if (failed !== undefined && failed.length > 0) {
                        exampleSections.push({
                            id: `quality_${key}`,
                            prefix: this.$t("fieldDetail.quality.failureSamplesPrefix"),
                            header: this.$t(`fieldDetail.quality.${key}.count_header`),
                            examples: failed.map((val) => val.meta),
                            group: "quality",
                        });
                    }
                });

                var passedSection = {
                    id: "passed",
                    header: this.$t("core.passedExamples"),
                    examples: [],
                };
                if (
                    this.check.quality.passed_examples !== undefined &&
                    this.check.quality.passed_examples.length > 0
                ) {
                    passedSection.examples = this.check.quality.passed_examples.map((val) => val.meta);
                } else if (
                    this.check.coverage.passed_examples !== undefined &&
                    this.check.coverage.passed_examples.length > 0
                ) {
                    passedSection.examples = this.check.coverage.passed_examples.map((val) => val.meta);
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
        },
    },
    methods: {
        preview: function (itemId, group) {
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

            var result;
            if (group) {
                result = this.allExamples[group].find((e) => e.meta.item_id === itemId);
            } else {
                result = Object.values(this.allExamples)
                    .flat()
                    .find((e) => e.meta.item_id === itemId);
            }

            if (result) {
                this.previewMetaData = result.result;
            }
        },
    },
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
