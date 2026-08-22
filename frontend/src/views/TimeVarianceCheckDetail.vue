<template>
  <dashboard-detail>
    <template
      v-if="loaded"
      #content
    >
      <h2>{{ $t("timeLevel." + check.name + ".name") }}</h2>
      <p v-html="$t('timeLevel.' + check.name + '.descriptionLong')" />

      <h5>
        {{ $t("timeLevel.coverage.header") }}
        <span class="bold">{{ formatNumber(check.meta.total_count) }}</span>
        <Tooltip :text="$t('timeLevel.coverage.header_tooltip')" />
      </h5>
      <div class="result_box">
        <table class="table table-borderless table-sm">
          <tbody>
            <tr>
              <td class="text-end label">
                <span class="check_name">{{ $t("timeLevel.coverage.ok") }}</span>
              </td>
              <td>
                <InlineBar
                  :numerator="check.meta.coverage_count"
                  :denominator="check.meta.total_count"
                  :count="check.meta.coverage_count"
                  state="ok"
                  :show-count="true"
                />
              </td>
            </tr>
            <tr>
              <td class="text-end label">
                <span class="check_name">{{ $t("timeLevel.coverage.failed") }}</span>
              </td>
              <td>
                <InlineBar
                  :numerator="check.meta.total_count - check.meta.coverage_count"
                  :denominator="check.meta.total_count"
                  :count="check.meta.total_count - check.meta.coverage_count"
                  state="failed"
                  :show-count="true"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <h5>
        {{ $t("timeLevel.check.header") }}
        <span class="bold">{{ formatNumber(check.meta.coverage_count) }}</span>
        <Tooltip :text="$t('timeLevel.check.header_tooltip')" />
      </h5>
      <div class="result_box">
        <table class="table table-borderless table-sm">
          <tbody>
            <tr>
              <td class="text-end label">
                <span class="check_name">{{ $t("timeLevel.check.ok") }}</span>
              </td>
              <td>
                <InlineBar
                  :numerator="check.meta.ok_count"
                  :denominator="check.meta.coverage_count"
                  :count="check.meta.ok_count"
                  state="ok"
                  :show-count="true"
                />
              </td>
            </tr>
            <tr>
              <td class="text-end label">
                <span class="check_name">{{ $t("timeLevel.check.failed") }}</span>
              </td>
              <td>
                <InlineBar
                  :numerator="check.meta.failed_count"
                  :denominator="check.meta.coverage_count"
                  :count="check.meta.failed_count"
                  state="failed"
                  :show-count="true"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="check.meta.examples && check.meta.examples.length > 0"
        class="result_box"
      >
        <table class="table table-sm">
          <thead>
            <tr>
              <th
                style="width: 75%"
                scope="col"
              >
                {{ $t("examples.ocid") }}
              </th>
              <th
                colspan="3"
                class="text-start"
                scope="col"
              >
                {{ $t("examples.actions") }}
              </th>
            </tr>
          </thead>
          <tbody>
            <!-- The OCID repeats. Showing it once would need a different layout. -->
            <template v-for="(item, index) in check.meta.examples.slice(0, 5)" :key="index">
              <tr
                class="new_row"
              >
                <td class="text-start numeric">
                  <div class="d-flex align-items-center example_ocid">
                    <span class="check_name">{{ item.new_item_ocid }}</span>
                    <span class="example_version">[{{ $t("examples.new") }}]</span>
                  </div>
                </td>
                <td class="clickable">
                  <button
                    v-if="'new_' + index != selectedKey"
                    type="button"
                    class="examples_button"
                    :title="$t('examples.preview.tooltip')"
                    :disabled="loadingPreviewData"
                    @click.stop.prevent="previewDataItem(item.new_item_id, 'new_' + index)"
                  >
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['far', 'eye']"
                    />
                  </button>
                  <span v-if="'new_' + index == selectedKey">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'eye']"
                    />
                  </span>
                </td>
                <td class="clickable">
                  <button
                    type="button"
                    class="examples_button"
                    :title="$t('examples.download.tooltip')"
                    @click.stop.prevent="download(item.new_item_id)"
                  >
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'cloud-download-alt']"
                    />
                  </button>
                </td>
                <td class="clickable">
                  <button
                    type="button"
                    class="examples_button"
                    :title="$t('examples.copyToClipboard.tooltip')"
                    @click.stop.prevent="copyToClipboard(item.new_item_id)"
                  >
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'clipboard']"
                    />
                  </button>
                </td>
              </tr>
              <tr
                class="old_row"
              >
                <td class="text-start numeric">
                  <div class="d-flex align-items-center example_ocid">
                    <span class="check_name">{{ item.ocid }}</span>
                    <span class="example_version">[{{ $t("examples.old") }}]</span>
                  </div>
                </td>
                <td class="clickable">
                  <button
                    v-if="'old_' + index != selectedKey"
                    type="button"
                    class="examples_button"
                    :title="$t('examples.preview.tooltip')"
                    :disabled="loadingPreviewData"
                    @click.stop.prevent="previewDataItem(item.item_id, 'old_' + index)"
                  >
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['far', 'eye']"
                    />
                  </button>
                  <span v-if="'old_' + index == selectedKey">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'eye']"
                    />
                  </span>
                </td>
                <td class="clickable">
                  <button
                    type="button"
                    class="examples_button"
                    :title="$t('examples.download.tooltip')"
                    @click.stop.prevent="download(item.item_id)"
                  >
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'cloud-download-alt']"
                    />
                  </button>
                </td>
                <td class="clickable">
                  <button
                    type="button"
                    class="examples_button"
                    :title="$t('examples.copyToClipboard.tooltip')"
                    @click.stop.prevent="copyToClipboard(item.item_id)"
                  >
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'clipboard']"
                    />
                  </button>
                </td>
              </tr>
            </template>
            <tr v-if="!showMore && check.meta.examples.length > 5">
              <td
                colspan="4"
                class="text-center bold clickable moreLess"
                @click.stop="showMore = true"
              >
                <a>
                  <FontAwesomeIcon icon="chevron-down" />
                  {{ $t("examples.showMore") }}
                </a>
              </td>
            </tr>
            <template v-if="showMore">
              <template v-for="(item, index) in check.meta.examples.slice(5)" :key="index + 5">
                <tr
                  class="new_row"
                >
                  <td class="text-start numeric">
                    <div class="d-flex align-items-center example_ocid">
                      <span class="check_name">{{ item.new_item_ocid }}</span>
                      <span class="example_version">[{{ $t("examples.new") }}]</span>
                    </div>
                  </td>
                  <td class="clickable">
                    <button
                      v-if="'new_' + (index + 5) != selectedKey"
                      type="button"
                      class="examples_button"
                      :title="$t('examples.preview.tooltip')"
                      :disabled="loadingPreviewData"
                      @click.stop.prevent="previewDataItem(item.new_item_id, 'new_' + (index + 5))"
                    >
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['far', 'eye']"
                      />
                    </button>
                    <span v-if="'new_' + (index + 5) == selectedKey">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'eye']"
                      />
                    </span>
                  </td>
                  <td class="clickable">
                    <button
                      type="button"
                      class="examples_button"
                      :title="$t('examples.download.tooltip')"
                      @click.stop.prevent="download(item.new_item_id)"
                    >
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'cloud-download-alt']"
                      />
                    </button>
                  </td>
                  <td class="clickable">
                    <button
                      type="button"
                      class="examples_button"
                      :title="$t('examples.copyToClipboard.tooltip')"
                      @click.stop.prevent="copyToClipboard(item.new_item_id)"
                    >
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'clipboard']"
                      />
                    </button>
                  </td>
                </tr>
                <tr
                  class="old_row"
                >
                  <td class="text-start numeric">
                    <div class="d-flex align-items-center example_ocid">
                      <span class="check_name">{{ item.ocid }}</span>
                      <span class="example_version">[{{ $t("examples.old") }}]</span>
                    </div>
                  </td>
                  <td class="clickable">
                    <button
                      v-if="'old_' + (index + 5) != selectedKey"
                      type="button"
                      class="examples_button"
                      :title="$t('examples.preview.tooltip')"
                      :disabled="loadingPreviewData"
                      @click.stop.prevent="previewDataItem(item.item_id, 'old_' + (index + 5))"
                    >
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['far', 'eye']"
                      />
                    </button>
                    <span v-if="'old_' + (index + 5) == selectedKey">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'eye']"
                      />
                    </span>
                  </td>
                  <td class="clickable">
                    <button
                      type="button"
                      class="examples_button"
                      :title="$t('examples.download.tooltip')"
                      @click.stop.prevent="download(item.item_id)"
                    >
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'cloud-download-alt']"
                      />
                    </button>
                  </td>
                  <td class="clickable">
                    <button
                      type="button"
                      class="examples_button"
                      :title="$t('examples.copyToClipboard.tooltip')"
                      @click.stop.prevent="copyToClipboard(item.item_id)"
                    >
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'clipboard']"
                      />
                    </button>
                  </td>
                </tr>
              </template>
            </template>
            <tr v-if="showMore">
              <td
                colspan="4"
                class="text-center bold clickable moreLess"
                @click.stop="showMore = false"
              >
                <a>
                  <FontAwesomeIcon icon="chevron-up" />
                  {{ $t("examples.showLess") }}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <template #preview>
      <h5>{{ $t("preview.metadata") }}</h5>
      <vue-json-pretty
        :deep="3"
        :data="previewMetadata"
      />

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

<script setup>
import { BSpinner } from "bootstrap-vue-next";
import { computed, ref } from "vue";
import VueJsonPretty from "vue-json-pretty";
import { useRoute } from "vue-router";
import { useDatasetStore } from "@/stores/dataset.js";
import "vue-json-pretty/lib/styles.css";
import InlineBar from "@/components/InlineBar.vue";
import Tooltip from "@/components/Tooltip.vue";
import { useDataItem } from "@/composables/useDataItem.js";
import { useFormatters } from "@/composables/useFormatters";
import { withoutExamples } from "@/util.js";
import DashboardDetail from "./layouts/DashboardDetail.vue";

const { formatNumber } = useFormatters();

const route = useRoute();
const datasetStore = useDatasetStore();
const { previewDataItem, previewData, loadingPreviewData, selectedKey, download, copyToClipboard } = useDataItem();

const showMore = ref(false);

const check = computed(() => datasetStore.timeVarianceLevelCheckByName(route.params.check));
const loaded = computed(() => check.value != null);
const previewMetadata = computed(() => (check.value == null ? null : withoutExamples(check.value.meta)));
</script>

<style scoped lang="scss">
@import "@/scss/variables";

.result_box .table {
    table-layout: fixed;
}

.result_box .table td.label {
    width: 33%;
}

.examples_button {
    padding: 0;
    border: none;
    background: none;
}

.examples_icon {
    color: $primary;
}

.new_row > td {
    border: none;
}

.example_version {
    color: $headings_light_color;
}

// A flex container drops whitespace-only text; 1ch is a space in the monospace font.
.example_ocid {
    column-gap: 1ch;
}
</style>
