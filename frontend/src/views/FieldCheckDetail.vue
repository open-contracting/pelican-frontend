<template>
  <dashboard-detail>
    <template
      v-if="check"
      #content
    >
      <h2>{{ $t("field.path") }}: {{ check.path }}</h2>

      <template v-for="(c, k) in check.coverage.checks" :key="k">
        <h5>
          <span class="category_name"> {{ $t("field.coverage") }}: </span>
          &ldquo;{{ $t("fieldDetail.coverage." + k + ".name") }}&rdquo;
          <span class="bold">
            {{ formatNumber(c.passed_count + c.failed_count) }}
          </span>
          <Tooltip :text="$t('fieldDetail.coverage.' + k + '.description')" />
        </h5>
        <CheckDetailResultBox
          :check="c"
          :passed-label="k == 'exists' ? 'fieldDetail.set' : undefined"
          :failed-label="k == 'exists' ? 'fieldDetail.notset' : undefined"
          ok
          failed
        />
      </template>

      <template v-for="(c, k) in check.quality.checks" :key="k">
        <h5>
          <span class="category_name"> {{ $t("field.quality") }}: </span>
          &ldquo;{{ $t("fieldDetail.quality." + k + ".name") }}&rdquo;
          <span class="bold">
            {{ formatNumber(c.passed_count + c.failed_count) }}
          </span>
          <Tooltip :text="$t('fieldDetail.quality.' + k + '.description')" />
        </h5>
        <CheckDetailResultBox
          :check="c"
          :classes="'quality'"
          ok
          failed
        />
      </template>

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
import { useRoute } from "vue-router";
import { useDatasetStore } from "@/stores/dataset.js";
import "vue-json-pretty/lib/styles.css";
import VueJsonPretty from "vue-json-pretty";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import Tooltip from "@/components/Tooltip.vue";
import { useDataItem } from "@/composables/useDataItem.js";
import { useFormatters } from "@/composables/useFormatters";
import type { ExampleSection, FieldLevelExample, JSONData } from "@/types.js";
import DashboardDetail from "./layouts/DashboardDetail.vue";

type Group = "coverage" | "quality";

const GROUPS = ["coverage", "quality"] as const;

const route = useRoute();
const datasetStore = useDatasetStore();
const { t } = useI18n();
const { formatNumber } = useFormatters();
const { previewDataItem, previewData, loadingPreviewData } = useDataItem();

const previewMetadata = ref<JSONData>(null);

const check = computed(() => datasetStore.fieldLevelCheckByPath(String(route.params.path)));

const allExamples = computed(() => {
  const result: Record<Group, FieldLevelExample[]> = { coverage: [], quality: [] };

  if (check.value) {
    for (const group of GROUPS) {
      for (const value of Object.values(check.value[group].checks)) {
        result[group] = result[group].concat(value.failed_examples ?? []);
      }
      result[group] = result[group].concat(check.value[group].passed_examples ?? []);
    }
  }

  return result;
});

const exampleSections = computed(() => {
  const sections: ExampleSection[] = [];

  if (check.value) {
    for (const group of GROUPS) {
      for (const [key, counts] of Object.entries(check.value[group].checks)) {
        const failed = counts.failed_examples;
        if (failed?.length) {
          sections.push({
            id: `${group}_${key}`,
            prefix: t(`fieldDetail.${group}.failureSamplesPrefix`),
            header: t(`fieldDetail.${group}.${key}.name`),
            examples: failed.map((val) => val.meta),
            group,
          });
        }
      }
    }

    const passed = check.value.quality.passed_examples?.length
      ? check.value.quality.passed_examples
      : (check.value.coverage.passed_examples ?? []);
    if (passed.length > 0) {
      sections.push({
        id: "passed",
        header: t("core.passedExamples"),
        examples: passed.map((val) => val.meta),
      });
    }
  }

  return sections;
});

function preview(itemId: number, group?: Group) {
  previewDataItem(itemId);

  const examples = group ? allExamples.value[group] : Object.values(allExamples.value).flat();
  const result = examples.find((e) => e.meta.item_id === itemId);

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

.label {
    padding-top: 6px;
}
</style>
