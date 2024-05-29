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
        <span class="bold">{{ check.meta.total_count | formatNumber }}</span>
                &nbsp;
        <Tooltip :text="$t('timeLevel.coverage.header_tooltip')" />
      </h5>
      <div class="result_box">
        <table class="table table-borderless table-sm">
          <tbody>
            <tr class="d-flex">
              <td class="col-4 text-right label">
                <span class="check_name">{{ $t("timeLevel.coverage.ok") }}</span>
              </td>
              <td class="col-8">
                <InlineBar
                  :count="check.meta.coverage_count"
                  :percentage="coveragePercentage"
                  :state="'ok'"
                  :show-count="true"
                />
              </td>
            </tr>
            <tr class="d-flex">
              <td class="col-4 text-right label">
                <span class="check_name">{{ $t("timeLevel.coverage.failed") }}</span>
              </td>
              <td class="col-8">
                <InlineBar
                  :count="check.meta.total_count - check.meta.coverage_count"
                  :percentage="100.0 - coveragePercentage"
                  :state="'failed'"
                  :show-count="true"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <h5>
        {{ $t("timeLevel.check.header") }}
        <span class="bold">{{ check.meta.coverage_count | formatNumber }}</span>
                &nbsp;
        <Tooltip :text="$t('timeLevel.check.header_tooltip')" />
      </h5>
      <div class="result_box">
        <table class="table table-borderless table-sm">
          <tbody>
            <tr class="d-flex">
              <td class="col-4 text-right label">
                <span class="check_name">{{ $t("timeLevel.check.ok") }}</span>
              </td>
              <td class="col-8">
                <InlineBar
                  :count="check.meta.ok_count"
                  :percentage="checkPercentage"
                  :state="'ok'"
                  :show-count="true"
                />
              </td>
            </tr>
            <tr class="d-flex">
              <td class="col-4 text-right label">
                <span class="check_name">{{ $t("timeLevel.check.failed") }}</span>
              </td>
              <td class="col-8">
                <InlineBar
                  :count="check.meta.failed_count"
                  :percentage="100.0 - checkPercentage"
                  :state="'failed'"
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
                class="col-1 text-left"
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
            <template v-for="(item, index) in check.meta.examples.slice(0, 5)">
              <tr
                :key="'new_' + index"
                class="d-flex new_row"
              >
                <td class="col-9 text-left numeric d-flex align-items-center">
                  <span class="check_name">{{ item.new_item_ocid }}</span>
                                    &nbsp;
                  <span class="example_version">[{{ $t("examples.new") }}]</span>
                </td>
                <td class="col-1 clickable">
                  <span v-if="'new_' + index != selectedKey">
                    <font-awesome-icon
                      v-if="!loadingPreviewData"
                      :id="'preview_new_' + index"
                      class="examples_icon"
                      :icon="['far', 'eye']"
                      @click.stop.prevent="preview('new_' + index, item.new_item_id)"
                    />
                    <font-awesome-icon
                      v-else
                      class="examples_icon"
                      :icon="['far', 'eye']"
                    />
                    <b-tooltip
                      :target="'preview_new_' + index"
                      triggers="hover"
                    >
                      <span
                        class="tooltip_text"
                        v-html="$t('examples.preview.tooltip')"
                      />
                    </b-tooltip>
                  </span>
                  <span v-if="'new_' + index == selectedKey">
                    <font-awesome-icon
                      class="examples_icon"
                      :icon="['fas', 'eye']"
                    />
                  </span>
                </td>
                <td class="col-1 clickable">
                  <span>
                    <font-awesome-icon
                      :id="'download_new_' + index"
                      class="examples_icon"
                      :icon="['fas', 'cloud-download-alt']"
                      @click.stop.prevent="download(item.new_item_id)"
                    />
                    <b-tooltip
                      :target="'download_new_' + index"
                      triggers="hover"
                    >
                      <span
                        class="tooltip_text"
                        v-html="$t('examples.download.tooltip')"
                      />
                    </b-tooltip>
                  </span>
                </td>
                <td class="col-1 clickable">
                  <span>
                    <font-awesome-icon
                      :id="'clipboard_new_' + index"
                      class="examples_icon"
                      :icon="['fas', 'clipboard']"
                      @click.stop.prevent="copyToClipboard(item.new_item_id)"
                    />
                    <b-tooltip
                      :target="'clipboard_new_' + index"
                      triggers="hover"
                    >
                      <span
                        class="tooltip_text"
                        v-html="$t('examples.copyToClipboard.tooltip')"
                      />
                    </b-tooltip>
                  </span>
                </td>
              </tr>
              <tr
                :key="'old_' + index"
                class="d-flex old_row"
              >
                <td class="col-9 text-left numeric d-flex align-items-center">
                  <span class="check_name">{{ item.ocid }}</span>
                                    &nbsp;
                  <span class="example_version">[{{ $t("examples.old") }}]</span>
                </td>
                <td class="col-1 clickable">
                  <span v-if="'old_' + index != selectedKey">
                    <font-awesome-icon
                      v-if="!loadingPreviewData"
                      :id="'preview_old_' + index"
                      class="examples_icon"
                      :icon="['far', 'eye']"
                      @click.stop.prevent="preview('old_' + index, item.item_id)"
                    />
                    <font-awesome-icon
                      v-else
                      class="examples_icon"
                      :icon="['far', 'eye']"
                    />
                    <b-tooltip
                      :target="'preview_old_' + index"
                      triggers="hover"
                    >
                      <span
                        class="tooltip_text"
                        v-html="$t('examples.preview.tooltip')"
                      />
                    </b-tooltip>
                  </span>
                  <span v-if="'old_' + index == selectedKey">
                    <font-awesome-icon
                      class="examples_icon"
                      :icon="['fas', 'eye']"
                    />
                  </span>
                </td>
                <td class="col-1 clickable">
                  <span>
                    <font-awesome-icon
                      :id="'download_old_' + index"
                      class="examples_icon"
                      :icon="['fas', 'cloud-download-alt']"
                      @click.stop.prevent="download(item.item_id)"
                    />
                    <b-tooltip
                      :target="'download_old_' + index"
                      triggers="hover"
                    >
                      <span
                        class="tooltip_text"
                        v-html="$t('examples.download.tooltip')"
                      />
                    </b-tooltip>
                  </span>
                </td>
                <td class="col-1 clickable">
                  <span>
                    <font-awesome-icon
                      :id="'clipboard_old_' + index"
                      class="examples_icon"
                      :icon="['fas', 'clipboard']"
                      @click.stop.prevent="copyToClipboard(item.item_id)"
                    />
                    <b-tooltip
                      :target="'clipboard_old_' + index"
                      triggers="hover"
                    >
                      <span
                        class="tooltip_text"
                        v-html="$t('examples.copyToClipboard.tooltip')"
                      />
                    </b-tooltip>
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
                  <font-awesome-icon icon="chevron-down" />
                  {{ $t("examples.showMore") }}
                </a>
              </td>
            </tr>
            <span v-if="showMore">
              <template v-for="(item, index) in check.meta.examples.slice(5)">
                <tr
                  :key="'new_' + (index + 5)"
                  class="d-flex new_row"
                >
                  <td class="col-9 text-left numeric d-flex align-items-center">
                    <span class="check_name">{{ item.new_item_ocid }}</span>
                                        &nbsp;
                    <span class="example_version">[{{ $t("examples.new") }}]</span>
                  </td>
                  <td class="col-1 clickable">
                    <span v-if="'new_' + (index + 5) != selectedKey">
                      <font-awesome-icon
                        v-if="!loadingPreviewData"
                        :id="'preview_new_' + (index + 5)"
                        class="examples_icon"
                        :icon="['far', 'eye']"
                        @click.stop.prevent="preview('new_' + (index + 5), item.new_item_id)"
                      />
                      <font-awesome-icon
                        v-else
                        class="examples_icon"
                        :icon="['far', 'eye']"
                      />
                      <b-tooltip
                        :target="'preview_new_' + (index + 5)"
                        triggers="hover"
                      >
                        <span
                          class="tooltip_text"
                          v-html="$t('examples.preview.tooltip')"
                        />
                      </b-tooltip>
                    </span>
                    <span v-if="'new_' + (index + 5) == selectedKey">
                      <font-awesome-icon
                        class="examples_icon"
                        :icon="['fas', 'eye']"
                      />
                    </span>
                  </td>
                  <td class="col-1 clickable">
                    <span>
                      <font-awesome-icon
                        :id="'download_new_' + (index + 5)"
                        class="examples_icon"
                        :icon="['fas', 'cloud-download-alt']"
                        @click.stop.prevent="download(item.new_item_id)"
                      />
                      <b-tooltip
                        :target="'download_new_' + (index + 5)"
                        triggers="hover"
                      >
                        <span
                          class="tooltip_text"
                          v-html="$t('examples.download.tooltip')"
                        />
                      </b-tooltip>
                    </span>
                  </td>
                  <td class="col-1 clickable">
                    <span>
                      <font-awesome-icon
                        :id="'clipboard_new_' + (index + 5)"
                        class="examples_icon"
                        :icon="['fas', 'clipboard']"
                        @click.stop.prevent="copyToClipboard(item.new_item_id)"
                      />
                      <b-tooltip
                        :target="'clipboard_new_' + (index + 5)"
                        triggers="hover"
                      >
                        <span
                          class="tooltip_text"
                          v-html="$t('examples.copyToClipboard.tooltip')"
                        />
                      </b-tooltip>
                    </span>
                  </td>
                </tr>
                <tr
                  :key="'old_' + (index + 5)"
                  class="d-flex old_row"
                >
                  <td class="col-9 text-left numeric d-flex align-items-center">
                    <span class="check_name">{{ item.ocid }}</span>
                                        &nbsp;
                    <span class="example_version">[{{ $t("examples.old") }}]</span>
                  </td>
                  <td class="col-1 clickable">
                    <span v-if="'old_' + (index + 5) != selectedKey">
                      <font-awesome-icon
                        v-if="!loadingPreviewData"
                        :id="'preview_old_' + (index + 5)"
                        class="examples_icon"
                        :icon="['far', 'eye']"
                        @click.stop.prevent="preview('old_' + (index + 5), item.item_id)"
                      />
                      <font-awesome-icon
                        v-else
                        class="examples_icon"
                        :icon="['far', 'eye']"
                      />
                      <b-tooltip
                        :target="'preview_old_' + (index + 5)"
                        triggers="hover"
                      >
                        <span
                          class="tooltip_text"
                          v-html="$t('examples.preview.tooltip')"
                        />
                      </b-tooltip>
                    </span>
                    <span v-if="'old_' + (index + 5) == selectedKey">
                      <font-awesome-icon
                        class="examples_icon"
                        :icon="['fas', 'eye']"
                      />
                    </span>
                  </td>
                  <td class="col-1 clickable">
                    <span>
                      <font-awesome-icon
                        :id="'download_old_' + (index + 5)"
                        class="examples_icon"
                        :icon="['fas', 'cloud-download-alt']"
                        @click.stop.prevent="download(item.item_id)"
                      />
                      <b-tooltip
                        :target="'download_old_' + (index + 5)"
                        triggers="hover"
                      >
                        <span
                          class="tooltip_text"
                          v-html="$t('examples.download.tooltip')"
                        />
                      </b-tooltip>
                    </span>
                  </td>
                  <td class="col-1 clickable">
                    <span>
                      <font-awesome-icon
                        :id="'clipboard_old_' + (index + 5)"
                        class="examples_icon"
                        :icon="['fas', 'clipboard']"
                        @click.stop.prevent="copyToClipboard(item.item_id)"
                      />
                      <b-tooltip
                        :target="'clipboard_old_' + (index + 5)"
                        triggers="hover"
                      >
                        <span
                          class="tooltip_text"
                          v-html="$t('examples.copyToClipboard.tooltip')"
                        />
                      </b-tooltip>
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
                  <font-awesome-icon icon="chevron-up" />
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
        :highlight-mouseover-node="true"
        :deep="3"
        :data="previewMetadata"
      />

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
import InlineBar from "@/components/InlineBar.vue";
import Tooltip from "@/components/Tooltip.vue";
import timeMixins from "@/plugins/timeMixins.js";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import VueJsonPretty from "vue-json-pretty";

export default {
    name: "TimeVarianceCheckDetail",
    components: {
        VueJsonPretty,
        DashboardDetail,
        InlineBar,
        Tooltip,
    },
    mixins: [timeMixins],
    data: () => ({
        check: null,
        previewDataItemId: null,
        previewMetadata: null,
        loadingPreviewData: false,
        examples: null,
        showMore: false,
        selectedKey: null,
    }),
    computed: {
        previewData() {
            const result = this.$store.getters.dataItemById(this.previewDataItemId);

            if (result) {
                return result.data;
            }

            return null;
        },
        coverageState() {
            return this.check.coverage_result ? "ok" : "failed";
        },
        checkState() {
            return this.check.check_result ? "ok" : "failed";
        },
        loaded() {
            this.loadCheck();

            return this.check != null;
        },
    },
    created() {
        this.loadCheck();
    },
    methods: {
        loadCheck: function () {
            this.check = this.$store.getters.timeVarianceLevelCheckByName(this.$route.params.check);

            if (this.check != null) {
                this.previewMetadata = Object.assign({}, this.check.meta);
                this.previewMetadata.examples = undefined;
            }
        },
        preview: function (selectedKey, itemId) {
            this.loadingPreviewData = true;
            this.$store
                .dispatch("loadDataItem", itemId)
                .then(() => {
                    if (this.$store.getters.dataItemJSONLines(itemId) < 3000) {
                        this.previewDataItemId = itemId;
                        this.selectedKey = selectedKey;
                    } else {
                        this.$alert(this.$t("preview.cannotDisplay"), null, "error");
                        this.previewDataItemId = null;
                        this.selectedKey = null;
                    }
                })
                .catch(() => {
                    this.$alert(this.$t("preview.nonExisting"), null, "error");
                    this.previewDataItemId = null;
                    this.selectedKey = null;
                })
                .finally(() => {
                    this.loadingPreviewData = false;
                });
        },
        download: function (itemId) {
            this.$store
                .dispatch("loadDataItem", itemId)
                .then(() => {
                    const result = this.$store.getters.dataItemById(itemId);
                    const fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(result.data, null, 2)]));
                    const fileLink = document.createElement("a");

                    fileLink.href = fileURL;
                    fileLink.setAttribute("download", `data_item_${itemId}.json`);
                    document.body.appendChild(fileLink);

                    fileLink.click();

                    this.$alert(this.$t("examples.download.success"), null, "success");
                })
                .catch(() => {
                    this.$alert(this.$t("preview.nonExisting"), null, "error");
                });
        },
        copyToClipboard: function (itemId) {
            this.$store
                .dispatch("loadDataItem", itemId)
                .then(() => {
                    if (this.$store.getters.dataItemJSONLines(itemId) < 3000) {
                        this.$clipboard(this.$store.getters.dataItemJSON(itemId));
                        this.$alert(this.$t("examples.copyToClipboard.success"), null, "success");
                    } else {
                        this.$alert(this.$t("examples.copyToClipboard.failure"), null, "error");
                    }
                })
                .catch(() => {
                    this.$alert(this.$t("preview.nonExisting"), null, "error");
                });
        },
    },
};
</script>

<style lang="scss">
@import "src/scss/variables";

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
