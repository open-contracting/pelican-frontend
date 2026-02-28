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
        <span class="bold">{{ $filters.formatNumber(check.meta.total_count) }}</span>
                &nbsp;
        <Tooltip :text="$t('timeLevel.coverage.header_tooltip')" />
      </h5>
      <div class="result_box">
        <table class="table table-borderless table-sm">
          <tbody>
            <tr class="d-flex">
              <td class="col-4 text-end label">
                <span class="check_name">{{ $t("timeLevel.coverage.ok") }}</span>
              </td>
              <td class="col-8">
                <InlineBar
                  :numerator="check.meta.coverage_count"
                  :denominator="check.meta.total_count"
                  :count="check.meta.coverage_count"
                  state="ok"
                  :show-count="true"
                />
              </td>
            </tr>
            <tr class="d-flex">
              <td class="col-4 text-end label">
                <span class="check_name">{{ $t("timeLevel.coverage.failed") }}</span>
              </td>
              <td class="col-8">
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
        <span class="bold">{{ $filters.formatNumber(check.meta.coverage_count) }}</span>
                &nbsp;
        <Tooltip :text="$t('timeLevel.check.header_tooltip')" />
      </h5>
      <div class="result_box">
        <table class="table table-borderless table-sm">
          <tbody>
            <tr class="d-flex">
              <td class="col-4 text-end label">
                <span class="check_name">{{ $t("timeLevel.check.ok") }}</span>
              </td>
              <td class="col-8">
                <InlineBar
                  :numerator="check.meta.ok_count"
                  :denominator="check.meta.coverage_count"
                  :count="check.meta.ok_count"
                  state="ok"
                  :show-count="true"
                />
              </td>
            </tr>
            <tr class="d-flex">
              <td class="col-4 text-end label">
                <span class="check_name">{{ $t("timeLevel.check.failed") }}</span>
              </td>
              <td class="col-8">
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
            <tr class="d-flex">
              <th
                class="col-9"
                scope="col"
              >
                {{ $t("examples.ocid") }}
              </th>
              <th
                class="col-1 text-start"
                scope="col"
              >
                {{ $t("examples.actions") }}
              </th>
              <th
                class="col-1 text-center"
                scope="col"
              />
              <th
                class="col-1 text-center"
                scope="col"
              />
            </tr>
          </thead>
          <tbody>
            <template v-for="(item, index) in check.meta.examples.slice(0, 5)" :key="index">
              <tr
                class="d-flex new_row"
              >
                <td class="col-9 text-start numeric d-flex align-items-center">
                  <span class="check_name">{{ item.new_item_ocid }}</span>
                                    &nbsp;
                  <span class="example_version">[{{ $t("examples.new") }}]</span>
                </td>
                <td class="clickable">
                  <span
                    v-if="'new_' + index != selectedKey"
                    :title="$t('examples.preview.tooltip')"
                  >
                    <FontAwesomeIcon
                      v-if="!loadingPreviewData"
                      class="examples_icon"
                      :icon="['far', 'eye']"
                      @click.stop.prevent="preview('new_' + index, item.new_item_id)"
                    />
                    <FontAwesomeIcon
                      v-else
                      class="examples_icon"
                      :icon="['far', 'eye']"
                    />
                  </span>
                  <span v-if="'new_' + index == selectedKey">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'eye']"
                    />
                  </span>
                </td>
                <td class="clickable">
                  <span :title="$t('examples.download.tooltip')">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'cloud-download-alt']"
                      @click.stop.prevent="download(item.new_item_id)"
                    />
                  </span>
                </td>
                <td class="clickable">
                  <span :title="$t('examples.copyToClipboard.tooltip')">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'clipboard']"
                      @click.stop.prevent="copyToClipboard(item.new_item_id)"
                    />
                  </span>
                </td>
              </tr>
              <tr
                class="d-flex old_row"
              >
                <td class="col-9 text-start numeric d-flex align-items-center">
                  <span class="check_name">{{ item.ocid }}</span>
                                    &nbsp;
                  <span class="example_version">[{{ $t("examples.old") }}]</span>
                </td>
                <td class="clickable">
                  <span
                    v-if="'old_' + index != selectedKey"
                    :title="$t('examples.preview.tooltip')"
                  >
                    <FontAwesomeIcon
                      v-if="!loadingPreviewData"
                      class="examples_icon"
                      :icon="['far', 'eye']"
                      @click.stop.prevent="preview('old_' + index, item.item_id)"
                    />
                    <FontAwesomeIcon
                      v-else
                      class="examples_icon"
                      :icon="['far', 'eye']"
                    />
                  </span>
                  <span v-if="'old_' + index == selectedKey">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'eye']"
                    />
                  </span>
                </td>
                <td class="clickable">
                  <span :title="$t('examples.download.tooltip')">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'cloud-download-alt']"
                      @click.stop.prevent="download(item.item_id)"
                    />
                  </span>
                </td>
                <td class="clickable">
                  <span :title="$t('examples.copyToClipboard.tooltip')">
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['fas', 'clipboard']"
                      @click.stop.prevent="copyToClipboard(item.item_id)"
                    />
                  </span>
                </td>
              </tr>
            </template>
            <tr v-if="!showMore && check.meta.examples.length > 5">
              <td
                colspan="2"
                class="text-center bold clickable moreLess"
                @click.stop="showMore = true"
              >
                <a>
                  <FontAwesomeIcon icon="chevron-down" />
                  {{ $t("examples.showMore") }}
                </a>
              </td>
            </tr>
            <span v-if="showMore">
              <template v-for="(item, index) in check.meta.examples.slice(5)" :key="index + 5">
                <tr
                  class="d-flex new_row"
                >
                  <td class="col-9 text-start numeric d-flex align-items-center">
                    <span class="check_name">{{ item.new_item_ocid }}</span>
                                        &nbsp;
                    <span class="example_version">[{{ $t("examples.new") }}]</span>
                  </td>
                  <td class="clickable">
                    <span
                      v-if="'new_' + (index + 5) != selectedKey"
                      :title="$t('examples.preview.tooltip')"
                    >
                      <FontAwesomeIcon
                        v-if="!loadingPreviewData"
                        class="examples_icon"
                        :icon="['far', 'eye']"
                        @click.stop.prevent="preview('new_' + (index + 5), item.new_item_id)"
                      />
                      <FontAwesomeIcon
                        v-else
                        class="examples_icon"
                        :icon="['far', 'eye']"
                      />
                    </span>
                    <span v-if="'new_' + (index + 5) == selectedKey">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'eye']"
                      />
                    </span>
                  </td>
                  <td class="clickable">
                    <span :title="$t('examples.download.tooltip')">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'cloud-download-alt']"
                        @click.stop.prevent="download(item.new_item_id)"
                      />
                    </span>
                  </td>
                  <td class="clickable">
                    <span :title="$t('examples.copyToClipboard.tooltip')">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'clipboard']"
                        @click.stop.prevent="copyToClipboard(item.new_item_id)"
                      />
                    </span>
                  </td>
                </tr>
                <tr
                  class="d-flex old_row"
                >
                  <td class="col-9 text-start numeric d-flex align-items-center">
                    <span class="check_name">{{ item.ocid }}</span>
                                        &nbsp;
                    <span class="example_version">[{{ $t("examples.old") }}]</span>
                  </td>
                  <td class="clickable">
                    <span
                      v-if="'old_' + (index + 5) != selectedKey"
                      :title="$t('examples.preview.tooltip')"
                    >
                      <FontAwesomeIcon
                        v-if="!loadingPreviewData"
                        class="examples_icon"
                        :icon="['far', 'eye']"
                        @click.stop.prevent="preview('old_' + (index + 5), item.item_id)"
                      />
                      <FontAwesomeIcon
                        v-else
                        class="examples_icon"
                        :icon="['far', 'eye']"
                      />
                    </span>
                    <span v-if="'old_' + (index + 5) == selectedKey">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'eye']"
                      />
                    </span>
                  </td>
                  <td class="clickable">
                    <span :title="$t('examples.download.tooltip')">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'cloud-download-alt']"
                        @click.stop.prevent="download(item.item_id)"
                      />
                    </span>
                  </td>
                  <td class="clickable">
                    <span :title="$t('examples.copyToClipboard.tooltip')">
                      <FontAwesomeIcon
                        class="examples_icon"
                        :icon="['fas', 'clipboard']"
                        @click.stop.prevent="copyToClipboard(item.item_id)"
                      />
                    </span>
                  </td>
                </tr>
              </template>
            </span>
            <tr v-if="showMore">
              <td
                colspan="2"
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
import { BSpinner, BTooltip } from "bootstrap-vue-next";
import { computed, onBeforeMount, ref } from "vue";
import { useI18n } from "vue-i18n";
import VueJsonPretty from "vue-json-pretty";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import "vue-json-pretty/lib/styles.css";
import InlineBar from "@/components/InlineBar.vue";
import Tooltip from "@/components/Tooltip.vue";
import DashboardDetail from "./layouts/DashboardDetail.vue";

const route = useRoute();
const store = useStore();

const check = ref(null);
const previewDataItemId = ref(null);
const previewMetadata = ref(null);
const loadingPreviewData = ref(false);
const examples = ref(null);
const showMore = ref(false);
const selectedKey = ref(null);

const previewData = computed(() => store.getters.dataItemById(previewDataItemId.value)?.data);
const coverageState = computed(() => (check.value?.coverage_result ? "ok" : "failed"));
const checkState = computed(() => (check.value?.check_result ? "ok" : "failed"));
const loaded = computed(() => {
    loadCheck();
    return check.value != null;
});

function loadCheck() {
    check.value = store.getters.timeVarianceLevelCheckByName(route.params.check);

    if (check.value != null) {
        previewMetadata.value = { ...check.value.meta };
        previewMetadata.value.examples = undefined;
    }
}

function preview(key, itemId) {
    loadingPreviewData.value = true;
    store
        .dispatch("loadDataItem", itemId)
        .then(() => {
            if (store.getters.dataItemJSONLines(itemId) < 3000) {
                previewDataItemId.value = itemId;
                selectedKey.value = key;
            } else {
                // Toast handled by component
                previewDataItemId.value = null;
                selectedKey.value = null;
            }
        })
        .catch(() => {
            // Toast handled by component
            previewDataItemId.value = null;
            selectedKey.value = null;
        })
        .finally(() => {
            loadingPreviewData.value = false;
        });
}

function download(itemId) {
    store
        .dispatch("loadDataItem", itemId)
        .then(() => {
            const result = store.getters.dataItemById(itemId);
            const fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(result.data, null, 2)]));
            const fileLink = document.createElement("a");

            fileLink.href = fileURL;
            fileLink.setAttribute("download", `data_item_${itemId}.json`);
            document.body.appendChild(fileLink);

            fileLink.click();

            // Toast handled by component
        })
        .catch(() => {
            // Toast handled by component
        });
}

function copyToClipboard(itemId) {
    store
        .dispatch("loadDataItem", itemId)
        .then(() => {
            if (store.getters.dataItemJSONLines(itemId) < 3000) {
                navigator.clipboard.writeText(store.getters.dataItemJSON(itemId));
                // Toast handled by component
            } else {
                // Toast handled by component
            }
        })
        .catch(() => {
            // Toast handled by component
        });
}

onBeforeMount(() => {
    loadCheck();
});
</script>

<style lang="scss">
@import "@/scss/variables";

.examples_icon {
    color: $primary;
}

.old_row > td {
    border: none;
}

.example_version {
    color: $headings_light_color;
}
</style>
