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
        <span class="bold">{{ formatNumber(check.individual_application_count) }}</span>
        <Tooltip :text="$t('resourceLevel.application_count_header_tooltip')" />
      </h5>
      <CheckDetailResultBox
        :check="check"
        individual-pass
        individual-non-pass
      />

      <ExampleBoxes
        :example-sections="exampleSections"
        :loading="!check.examples_filled"
        @preview="preview"
      />
    </template>

    <template #preview>
      <span v-if="previewMetadata">
        <h5>{{ $t("preview.metadata") }}</h5>
        <vue-json-pretty :data="previewMetadata" />
      </span>

      <div class="spacer" />

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

<script setup lang="ts">
import { BSpinner } from "bootstrap-vue-next";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import VueJsonPretty from "vue-json-pretty";
import { useRoute } from "vue-router";
import { useDatasetStore } from "@/stores/dataset.js";
import "vue-json-pretty/lib/styles.css";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import Tooltip from "@/components/Tooltip.vue";
import { useDataItem } from "@/composables/useDataItem.js";
import { useFormatters } from "@/composables/useFormatters";
import type { JSONData } from "@/types.js";
import DashboardDetail from "./layouts/DashboardDetail.vue";

const { formatNumber } = useFormatters();

const route = useRoute();
const datasetStore = useDatasetStore();
const { t } = useI18n();
const { previewDataItem, previewData, loadingPreviewData } = useDataItem();

const previewMetadata = ref<JSONData>(null);

const check = computed(() => datasetStore.resourceLevelCheckByName(String(route.params.check)));
const allExamples = computed(() => {
  if (!check.value) {
    return [];
  }

  return [...check.value.failed_examples, ...check.value.passed_examples, ...check.value.undefined_examples];
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

function preview(itemId: number) {
  previewDataItem(itemId);

  const result = allExamples.value.find((element) => element.meta.item_id === itemId);
  if (result) {
    previewMetadata.value = result.result;
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
