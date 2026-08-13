<template>
  <dashboard>
    <h2>{{ $t("field.title") }}</h2>
    <div
      id="field_description"
      class="description"
      v-html="$t('field.description')"
    />

    <div class="checked_fields_box">
      <div class="checked_fields_icon">
        <FontAwesomeIcon
          :icon="['fas', 'hand-point-right']"
          :style="{ color: '#FDC926' }"
        />
      </div>
      <div class="checked_fields_text">
        {{ $t("field.checkedFields") }}
      </div>
    </div>

    <h4 class="sub_headline">
      {{ $t("field.all") }}
    </h4>

    <BRow
      class="action_bar"
      align-v="center"
    >
      <BCol class="text-start">
        <SearchInput
          :placeholder="$t('field.search')"
          :preset="search"
          :on-update="search => $store.commit('setFieldCheckSearch', search)"
        />
      </BCol>
      <BCol class="text-end">
        <BButtonGroup v-if="layout == 'table'">
          <button
            :class="['btn', 'reset-table-sorting']"
            :title="$t('field.resetTableSorting')"
            @click="resetTableSorting()"
          >
            <FontAwesomeIcon icon="sort-numeric-down" />
          </button>
        </BButtonGroup>

        <BButtonGroup>
          <button
            :class="['btn', { active: layout == 'table' }]"
            :title="$t('field.tableLayout')"
            @click="$store.commit('setFieldCheckLayout', 'table')"
          >
            <FontAwesomeIcon icon="bars" />
          </button>
          <button
            :class="['btn', { active: layout == 'tree' }]"
            :title="$t('field.treeLayout')"
            @click="$store.commit('setFieldCheckLayout', 'tree')"
          >
            <FontAwesomeIcon icon="align-right" />
          </button>
        </BButtonGroup>
        <FilterDropdown
          :filter-names="filterNames"
          :start-index="filterIndex"
          @newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
        />
      </BCol>
    </BRow>

    <div class="field_result_box">
      <FieldCheckTable
        v-if="layout == 'table'"
        ref="field-check-table"
        :filter="filters[filterIndex]"
      />
      <FieldCheckTree
        v-else-if="layout == 'tree'"
        :filter="filters[filterIndex]"
      />
    </div>
  </dashboard>
</template>

<script setup>
import { BButtonGroup, BCol, BRow } from "bootstrap-vue-next";
import { computed, onBeforeMount, ref, useTemplateRef, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import FieldCheckTable from "@/components/FieldCheckTable.vue";
import FieldCheckTree from "@/components/FieldCheckTree.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";
import SearchInput from "@/components/SearchInput.vue";
import Dashboard from "./layouts/Dashboard.vue";

const store = useStore();
const { t } = useI18n();

const fieldCheckTableRef = useTemplateRef("field-check-table");

const filterIndex = ref(0);

const filterNames = [
    t("field.filterDropdown.all"),
    t("field.filterDropdown.coverageFailedOnly"),
    t("field.filterDropdown.qualityFailedOnly"),
    t("field.filterDropdown.passedOnly"),
];

const filters = [
    () => true,
    (item) => item.coverage.failed_count > 0,
    (item) => item.quality.failed_count > 0,
    (item) => item.coverage.failed_count === 0 && item.quality.failed_count === 0 && item.coverage.passed_count > 0,
];

const layout = computed(() => store.getters.fieldCheckLayout);
const search = computed(() => store.getters.fieldCheckSearch);

watch(filterIndex, (newFilterIndex) => {
    store.commit("setFieldLevelFilterIndex", newFilterIndex);
});

onBeforeMount(() => {
    filterIndex.value = store.getters.fieldLevelFilterIndex;
});

function resetTableSorting() {
    fieldCheckTableRef.value.resetSorting();
}
</script>

<style lang="scss">
@import "@/scss/_variables";
@import "@/scss/main";

.sub_headline {
    margin-bottom: 0px;
}

#field_description {
    margin-bottom: 30px;
}

.checked_fields_box {
    margin-bottom: 30px;
    width: 100%;
}

.checked_fields_box .checked_fields_icon {
    background-color: #dde0f6;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    border: 0;
    padding: 15px;
    padding-right: 5px;
    float: left;
}

.checked_fields_box .checked_fields_text {
    background-color: #dde0f6;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    border: 0;
    padding-top: 16px;
    padding-bottom: 14px;
    padding-right: 15px;
    vertical-align: -1px;
    color: $text-color;
    overflow: auto;
}

.field_result_box {
    background-color: white;
    border-radius: 10px;
    padding: 40px;
    box-shadow: 0 2px 18px 6px rgba(0, 0, 0, 0.06);
    border: 0;
}

mark {
    background-color: $primary !important;
}

.action_bar {
    margin-bottom: 5px;

    .btn-group {
        margin-left: 15px;
    }

    button {
        background-color: transparent;
        border-color: $text-color;
        color: $text-color;

        &:hover,
        &.active {
            border-color: $primary;
            color: $primary;
        }
    }
}
</style>
