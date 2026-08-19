<template>
  <dashboard-detail>
    <template
      v-if="check"
      #content
    >
      <h2>{{ $t("fieldDetail.path") }}: {{ check.path }}</h2>

      <template v-for="(c, k) in check.coverage.checks" :key="k">
        <h5>
          <span class="category_name"> {{ $t("fieldDetail.coverage.label") }}: </span>
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
          <span class="category_name"> {{ $t("fieldDetail.quality.label") }}: </span>
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
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import "vue-json-pretty/lib/styles.css";
import VueJsonPretty from "vue-json-pretty";
import CheckDetailResultBox from "@/components/CheckDetailResultBox.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";
import Tooltip from "@/components/Tooltip.vue";
import { useDataItem } from "@/composables/useDataItem.js";
import { useFormatters } from "@/composables/useFormatters";
import DashboardDetail from "./layouts/DashboardDetail.vue";

const route = useRoute();
const store = useStore();
const { t } = useI18n();
const { formatNumber } = useFormatters();
const { previewDataItem, previewData, loadingPreviewData } = useDataItem();

const previewMetadata = ref(null);

const check = computed(() => store.getters.fieldLevelCheckByPath(route.params.path));

const allExamples = computed(() => {
  if (!check.value) {
    return { coverage: [], quality: [] };
  }

  const result = { coverage: [], quality: [] };
  if (check.value.coverage) {
    for (const value of Object.values(check.value.coverage.checks)) {
      result.coverage = result.coverage.concat(value.failed_examples ?? []);
    }
    result.coverage = result.coverage.concat(check.value.coverage.passed_examples ?? []);
  }
  if (check.value.quality) {
    for (const value of Object.values(check.value.quality.checks)) {
      result.quality = result.quality.concat(value.failed_examples ?? []);
    }
    result.quality = result.quality.concat(check.value.quality.passed_examples ?? []);
  }
  return result;
});

const exampleSections = computed(() => {
  const sections = [];
  let failed;
  if (check.value) {
    for (const key of Object.keys(check.value.coverage.checks)) {
      failed = check.value.coverage.checks[key].failed_examples;
      if (failed?.length > 0) {
        sections.push({
          id: `coverage_${key}`,
          prefix: t("fieldDetail.coverage.failureSamplesPrefix"),
          header: t(`fieldDetail.coverage.${key}.name`),
          examples: failed.map((val) => val.meta),
          group: "coverage",
        });
      }
    }

    for (const key of Object.keys(check.value.quality.checks)) {
      failed = check.value.quality.checks[key].failed_examples;
      if (failed?.length > 0) {
        sections.push({
          id: `quality_${key}`,
          prefix: t("fieldDetail.quality.failureSamplesPrefix"),
          header: t(`fieldDetail.quality.${key}.name`),
          examples: failed.map((val) => val.meta),
          group: "quality",
        });
      }
    }

    const passedSection = {
      id: "passed",
      header: t("core.passedExamples"),
      examples: [],
    };
    if (check.value.quality.passed_examples?.length > 0) {
      passedSection.examples = check.value.quality.passed_examples.map((val) => val.meta);
    } else if (check.value.coverage.passed_examples?.length > 0) {
      passedSection.examples = check.value.coverage.passed_examples.map((val) => val.meta);
    }
    if (passedSection.examples.length > 0) {
      sections.push(passedSection);
    }
  }

  return sections;
});

function preview(itemId, group) {
  previewDataItem(itemId);

  let result;
  if (group) {
    result = allExamples.value[group].find((e) => e.meta.item_id === itemId);
  } else {
    result = Object.values(allExamples.value)
      .flat()
      .find((e) => e.meta.item_id === itemId);
  }

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
