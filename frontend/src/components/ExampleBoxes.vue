<template>
  <span>
    <span v-if="!loaded">
      <div class="result_box loader text-center">
        <div class="spinner">
          <b-spinner
            variant="primary"
            style="width: 4rem; height: 4rem"
            type="grow"
            class="spinner"
          />
        </div>
        {{ $t("loader.examples") }}
      </div>
    </span>
    <span
      v-for="section in exampleSections"
      :key="section.header"
    >
      <h5>
        <span
          v-if="section.prefix"
          class="prefix"
        >{{ section.prefix }}:&nbsp;"</span>{{ section.header
        }}<span
          v-if="section.prefix"
          class="prefix"
        >"</span>
      </h5>
      <div class="result_box" :class="section.group">
        <table class="table table-sm">
          <thead>
            <tr class="d-flex">
              <th
                class="col-9"
                scope="col"
              >{{ $t("examples.ocid") }}</th>
              <th
                class="col-1 text-left"
                scope="col"
              >{{ $t("examples.actions") }}</th>
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
            <tr
              v-for="(item, index) in section.examples.slice(0, 5)"
              :key="index"
              class="d-flex"
            >
              <td class="col-9 text-left numeric">
                <span class="check_name">{{ item.ocid }}</span>
              </td>
              <td class="col-1 clickable">
                <span v-if="index != selectedKey || selectedSection != section.header">
                  <font-awesome-icon
                    :id="'preview_' + section.id + '_' + index"
                    class="examples_icon"
                    :icon="['far', 'eye']"
                    @click.stop.prevent="preview(index, section.header, item.item_id, section.group)"
                  />
                  <b-tooltip
                    :target="'preview_' + section.id + '_' + index"
                    triggers="hover"
                  >
                    <span
                      class="tooltip_text"
                      v-html="$t('examples.preview.tooltip')"
                    />
                  </b-tooltip>
                </span>
                <span v-if="index == selectedKey && selectedSection == section.header">
                  <font-awesome-icon
                    :id="'preview_' + section.id + '_' + index"
                    class="examples_icon"
                    :icon="['fas', 'eye']"
                  />
                </span>
              </td>
              <td class="col-1 clickable">
                <span>
                  <font-awesome-icon
                    :id="'download_' + section.id + '_' + index"
                    class="examples_icon"
                    :icon="['fas', 'cloud-download-alt']"
                    @click.stop.prevent="download(item.item_id)"
                  />
                  <b-tooltip
                    :target="'download_' + section.id + '_' + index"
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
                    :id="'clipboard_' + section.id + '_' + index"
                    class="examples_icon"
                    :icon="['fas', 'clipboard']"
                    @click.stop.prevent="copyToClipboard(item.item_id)"
                  />
                  <b-tooltip
                    :target="'clipboard_' + section.id + '_' + index"
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
            <tr v-if="!visibleSections(section.header) && section.examples.length > 5">
              <td
                colspan="2"
                class="text-center bold clickable moreLess"
                @click.stop="showMore(section.header)"
              >
                <a>
                  <font-awesome-icon icon="chevron-down" />
                  {{ $t("examples.showMore") }}
                </a>
              </td>
            </tr>
            <span v-if="visibleSections(section.header)">
              <tr
                v-for="(item, index) in section.examples.slice(5)"
                :key="index"
                class="d-flex"
              >
                <td class="col-9 text-left numeric">
                  <span class="check_name">{{ item.ocid }}</span>
                </td>
                <td class="col-1 clickable">
                  <span v-if="index + 5 != selectedKey || selectedSection != section.header">
                    <font-awesome-icon
                      :id="'preview_' + section.id + '_' + (index + 5)"
                      class="examples_icon"
                      :icon="['far', 'eye']"
                      @click.stop.prevent="preview(index + 5, section.header, item.item_id, section.group)"
                    />
                    <b-tooltip
                      :target="'preview_' + section.id + '_' + (index + 5)"
                      triggers="hover"
                    >
                      <span
                        class="tooltip_text"
                        v-html="$t('examples.preview.tooltip')"
                      />
                    </b-tooltip>
                  </span>
                  <span v-if="index + 5 == selectedKey && selectedSection == section.header">
                    <font-awesome-icon
                      :id="'preview_' + section.id + '_' + (index + 5)"
                      class="examples_icon"
                      :icon="['fas', 'eye']"
                    />
                  </span>
                </td>
                <td class="col-1 clickable">
                  <span>
                    <font-awesome-icon
                      :id="'download_' + section.id + '_' + (index + 5)"
                      class="examples_icon"
                      :icon="['fas', 'cloud-download-alt']"
                      @click.stop.prevent="download(item.item_id)"
                    />
                    <b-tooltip
                      :target="'download_' + section.id + '_' + (index + 5)"
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
                      :id="'clipboard_' + section.id + '_' + (index + 5)"
                      class="examples_icon"
                      :icon="['fas', 'clipboard']"
                      @click.stop.prevent="copyToClipboard(item.item_id)"
                    />
                    <b-tooltip
                      :target="'clipboard_' + section.id + '_' + (index + 5)"
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
            </span>
            <tr v-if="visibleSections(section.header)">
              <td
                colspan="2"
                class="text-center bold clickable moreLess"
                @click.stop="showLess(section.header)"
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
    </span>
  </span>
</template>

<script>
export default {
    props: {
        exampleSections: Array,
        loaded: Boolean,
    },
    data: () => ({
        openSections: [],
        selectedKey: null,
        selectedSection: null,
    }),
    computed: {},
    methods: {
        preview: function (key, section, itemId, group) {
            this.selectedKey = key;
            this.selectedSection = section;
            this.$emit("preview", itemId, group);
        },
        download: function (itemId) {
            this.$store.dispatch("loadDataItem", itemId).then(() => {
                var result = this.$store.getters.dataItemById(itemId);
                var fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(result.data, null, 2)]));
                var fileLink = document.createElement("a");

                fileLink.href = fileURL;
                fileLink.setAttribute("download", `data_item_${itemId}.json`);
                document.body.appendChild(fileLink);

                fileLink.click();

                this.$alert(this.$t("examples.download.success"), null, "success");
            });
        },
        copyToClipboard: function (itemId) {
            this.$store.dispatch("loadDataItem", itemId).finally(() => {
                if (this.$store.getters.dataItemJSONLines(itemId) < 3000) {
                    this.$clipboard(this.$store.getters.dataItemJSON(itemId));
                    this.$alert(this.$t("examples.copyToClipboard.success"), null, "success");
                } else {
                    this.$alert(this.$t("examples.copyToClipboard.failure"), null, "error");
                }
            });
        },
        showMore: function (section) {
            this.openSections.push(section);
        },
        showLess: function (section) {
            this.openSections = this.openSections.filter((item) => item !== section);
        },
        visibleSections: function (section) {
            return this.openSections.includes(section);
        },
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";
@import "src/scss/variables";

.moreLess {
    padding-top: 25px;
}

.loader {
    font-size: 19px;
    font-weight: 700;
    padding: 40px;
}

.spinner {
    margin-bottom: 20px;
    font-size: 40px;
}

.disabled {
    cursor: not-allowed;
}

.examples_icon {
    color: $primary;
}

.prefix {
    color: $headings-light-color;
    font-family: $font-family-thin;
}
</style>
