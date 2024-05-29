<template>
  <dashboard-detail>
    <template
      v-if="check"
      #content
    >
      <h2 v-if="check">
        <span class="category_name">
          {{ $t("resourceLevel." + check.name.split(".")[0] + ".categoryName") }}:
        </span>
        {{ $t("resourceLevel." + check.name + ".name") }}
      </h2>
      <p
        class="description"
        v-html="$t('resourceLevel.' + check.name + '.description')"
      />

      <h5>
        {{ $t("resourceLevel.count_header") }}
        <span class="bold">{{
          (check.passed_count + check.failed_count + check.undefined_count) | formatNumber
        }}</span>
                &nbsp;
        <Tooltip :text="$t('resourceLevel.count_header_tooltip')" />
      </h5>

      <CheckDetailResultBox
        :check="check"
        ok
        failed
        na
      />

      <h5>
        {{ $t("resourceLevel.application_count_header") }}
        <span class="bold">{{ check.individual_application_count | formatNumber }}</span>&nbsp;
        <Tooltip :text="$t('resourceLevel.application_count_header_tooltip')" />
      </h5>
      <CheckDetailResultBox
        :check="check"
        individual-pass
        individual-non-pass
      />

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
import resourceCheckMixin from "@/plugins/resourceCheckMixins.js";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import VueJsonPretty from "vue-json-pretty";

export default {
    name: "ResourceCheckDetail",
    components: {
        VueJsonPretty,
        DashboardDetail,
        ExampleBoxes,
        CheckDetailResultBox,
        Tooltip,
    },
    mixins: [resourceCheckMixin],
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

            let allExamples = [];
            allExamples = allExamples.concat(this.check.failed_examples);
            allExamples = allExamples.concat(this.check.passed_examples);
            allExamples = allExamples.concat(this.check.undefined_examples);
            return allExamples;
        },
        check() {
            const stats = this.$store.getters.resourceLevelStats;
            if (stats != null) {
                return stats.find((item) => item.name === this.$route.params.check);
            }
            return null;
        },
        exampleSections() {
            const exampleSections = [];
            if (this.check !== [] && this.check.name !== undefined) {
                const failed = this.check.failed_examples;
                const passed = this.check.passed_examples;
                const undefineds = this.check.undefined_examples;

                if (failed.length > 0) {
                    exampleSections.push({
                        id: "failed",
                        header: this.$t("core.failedExamples"),
                        examples: failed.map((val) => val.meta),
                    });
                }

                if (passed.length > 0) {
                    exampleSections.push({
                        id: "passed",
                        header: this.$t("core.passedExamples"),
                        examples: passed.map((val) => val.meta),
                    });
                }

                if (undefineds.length > 0) {
                    exampleSections.push({
                        id: "undefined",
                        header: this.$t("core.undefinedExamples"),
                        examples: undefineds.map((val) => val.meta),
                    });
                }
            }

            return exampleSections;
        },
        previewData() {
            const result = this.$store.getters.dataItemById(this.previewDataItemId);

            if (result) {
                return result.data;
            }

            return null;
        },
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

            const result = this.allExamples.find((element) => element.meta.item_id === itemId);
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
</style>
