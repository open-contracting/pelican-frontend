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
          formatNumber(check.passed_count + check.failed_count + check.undefined_count)
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
        <span class="bold">{{ formatNumber(check.individual_application_count) }}</span>&nbsp;
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
        @preview="preview"
      />
    </template>

    <template #preview>
      <span v-if="previewMetaData">
        <h5>{{ $t("preview.metadata") }}</h5>
        <vue-json-pretty :data="previewMetaData" />
      </span>

      <div class="divider">
&nbsp;
      </div>

      <span v-if="loadingPreviewData">
        <div class="result_box loader text-center">
          <div class="spinner">
            <BSpinner
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
          :deep="2"
          :data="previewData"
        />
      </span>
    </template>
  </dashboard-detail>
</template>

<script setup>
import { BSpinner } from "bootstrap-vue-next";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import VueJsonPretty from "vue-json-pretty";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import "vue-json-pretty/lib/styles.css";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import Tooltip from "@/components/Tooltip.vue";
import { useDataItem } from "@/composables/useDataItem.js";
import { useFormatters } from "@/composables/useFormatters";
import DashboardDetail from "./layouts/DashboardDetail.vue";

const { formatNumber } = useFormatters();

const route = useRoute();
const store = useStore();
const { t } = useI18n();
const { previewDataItem, previewData, loadingPreviewData } = useDataItem();

const previewMetaData = ref(null);

const check = computed(() => store.getters.resourceLevelStats?.find((item) => item.name === route.params.check));
const allExamples = computed(() => {
  if (!check.value) {
    return [];
  }

  let examples = [];
  examples = examples.concat(check.value.failed_examples);
  examples = examples.concat(check.value.passed_examples);
  examples = examples.concat(check.value.undefined_examples);
  return examples;
});
const exampleSections = computed(() => {
  const sections = [];
  if (check.value) {
    const failed = check.value.failed_examples;
    const passed = check.value.passed_examples;
    const undefineds = check.value.undefined_examples;

    if (failed.length > 0) {
      sections.push({
        id: "failed",
        header: t("core.failedExamples"),
        examples: failed.map((val) => val.meta),
      });
    }

    if (passed.length > 0) {
      sections.push({
        id: "passed",
        header: t("core.passedExamples"),
        examples: passed.map((val) => val.meta),
      });
    }

    if (undefineds.length > 0) {
      sections.push({
        id: "undefined",
        header: t("core.undefinedExamples"),
        examples: undefineds.map((val) => val.meta),
      });
    }
  }

  return sections;
});

function preview(itemId) {
  previewDataItem(itemId);

  const result = allExamples.value.find((element) => element.meta.item_id === itemId);
  if (result) {
    previewMetaData.value = result.result;
  }
}
</script>

<style scoped lang="scss">
@import "@/scss/variables";

.category_name {
    color: $headings-light-color;
    font-family: $font-family-thin;
}
</style>
