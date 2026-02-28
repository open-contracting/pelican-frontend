<template>
  <span>
    <span v-if="!loaded">
      <div class="result_box loader text-center">
        <div class="spinner">
          <BSpinner
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
                class="col-1 text-start"
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
              <td class="col-9 text-start numeric">
                <span class="check_name">{{ item.ocid }}</span>
              </td>
              <td class="clickable">
                <span
                  v-if="index != selectedKey || selectedSection != section.header"
                  :title="$t('examples.preview.tooltip')"
                >
                  <FontAwesomeIcon
                    class="examples_icon"
                    :icon="['far', 'eye']"
                    @click.stop.prevent="preview(index, section.header, item.item_id, section.group)"
                  />
                </span>
                <span v-if="index == selectedKey && selectedSection == section.header">
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
            <tr v-if="!visibleSections(section.header) && section.examples.length > 5">
              <td
                colspan="2"
                class="text-center bold clickable moreLess"
                @click.stop="showMore(section.header)"
              >
                <a>
                  <FontAwesomeIcon icon="chevron-down" />
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
                <td class="col-9 text-start numeric">
                  <span class="check_name">{{ item.ocid }}</span>
                </td>
                <td class="clickable">
                  <span
                    v-if="index + 5 != selectedKey || selectedSection != section.header"
                    :title="$t('examples.preview.tooltip')"
                  >
                    <FontAwesomeIcon
                      class="examples_icon"
                      :icon="['far', 'eye']"
                      @click.stop.prevent="preview(index + 5, section.header, item.item_id, section.group)"
                    />
                  </span>
                  <span v-if="index + 5 == selectedKey && selectedSection == section.header">
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
            </span>
            <tr v-if="visibleSections(section.header)">
              <td
                colspan="2"
                class="text-center bold clickable moreLess"
                @click.stop="showLess(section.header)"
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
    </span>
  </span>
</template>

<script setup>
import { BSpinner } from "bootstrap-vue-next";
import { ref } from "vue";
import { useDataItem } from "@/composables/useDataItem.js";

defineProps({
    exampleSections: Array,
    loaded: Boolean,
});

const emit = defineEmits(["preview"]);

const { download, copyToClipboard } = useDataItem();

const openSections = ref([]);
const selectedKey = ref(null);
const selectedSection = ref(null);

function preview(key, section, itemId, group) {
    selectedKey.value = key;
    selectedSection.value = section;
    emit("preview", itemId, group);
}

function showMore(section) {
    openSections.value.push(section);
}

function showLess(section) {
    openSections.value = openSections.value.filter((item) => item !== section);
}

function visibleSections(section) {
    return openSections.value.includes(section);
}
</script>

<style scoped lang="scss">
@import "@/scss/main";
@import "@/scss/variables";

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
