<template>
  <div>
    <div class="thr row">
      <div
        class="th col col-4"
        @click="sortByPath(tableData)"
      >
        <SortButtons
          :label="$t('field.table.head.object')"
          :active="sortedBy == 'path'"
          :asc="isAscendingSorted"
          :on-asc="() => sortByPath(tableData)"
          :on-desc="() => sortByPath(tableData, false)"
        />
      </div>
      <div
        class="th col col-4 justify-content-center d-flex"
        @click="sortByCoverage(tableData)"
      >
        <SortButtons
          :label="$t('field.table.head.coverage')"
          :active="sortedBy == 'coverage'"
          :asc="isAscendingSorted"
          :on-asc="() => sortByCoverage(tableData)"
          :on-desc="() => sortByCoverage(tableData, false)"
        />
      </div>
      <div
        class="th col col-4 justify-content-center d-flex"
        @click="sortByQuality(tableData)"
      >
        <SortButtons
          :label="$t('field.table.head.quality')"
          :active="sortedBy == 'quality'"
          :asc="isAscendingSorted"
          :on-asc="() => sortByQuality(tableData)"
          :on-desc="() => sortByQuality(tableData, false)"
        />
      </div>
    </div>

    <template v-for="n in tableData" :key="n.path">
      <FieldCheckTableRow
        v-if="isSearched(n)"
        :check="n"
      >
        <span v-html="highlightSearch(n.path)" />
        <template v-if="hasHidden(n)">
          <div>
            <span
              class="hide_button"
              @click.stop="switchHidden(n)"
            >
              <FontAwesomeIcon
                icon="eye-slash"
                class="hidden_icon"
              />
              <i>{{ $t("field.hidden", { n: n._hidden.length }) }}</i>
            </span>
          </div>
        </template>
      </FieldCheckTableRow>
      <template v-for="h in n._hidden" :key="h.path">
        <FieldCheckTableRow
          v-if="isSearched(h)"
          :check="h"
          :class="['hidden_row', { hidden: isHidden(n) }]"
        >
          <span v-html="highlightSearch(h.path)" />
        </FieldCheckTableRow>
      </template>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import FieldCheckTableRow from "./FieldCheckTableRow.vue";
import SortButtons from "./SortButtons.vue";

const props = defineProps(["filter"]);
const store = useStore();

const { sortBy, sortByPath, sortByCoverage, sortByQuality, sortByProcessingOrder, highlightSearch, isPathSearched } =
    useFieldCheckSearch();

const showHidden = ref({});

const stats = computed(() => store.getters.fieldLevelStats);
const sortedBy = computed(() => {
    const value = store.getters.fieldCheckSortedBy;
    return value == null ? "processingOrder" : value;
});
const isAscendingSorted = computed(() => {
    const value = store.getters.fieldCheckSortedAscending;
    return value == null ? true : value;
});
const tableData = computed(() => {
    if (!stats.value) {
        return [];
    }
    const data = [];

    sortBy(stats.value, "path");

    for (const n of stats.value) {
        if (n.coverage.total_count && props.filter(n)) {
            data.push(n);
        }
    }

    return data;
});

function hasHidden(check) {
    return "_hidden" in check && check._hidden.length > 0;
}

function switchHidden(check) {
    showHidden.value[check.path] = !showHidden.value[check.path];
}

function isHidden(check) {
    return !showHidden.value[check.path];
}

function resetSorting() {
    sortByProcessingOrder(tableData.value);
}

function isSearched(check) {
    return check && isPathSearched(check.path);
}

onMounted(() => {
    sortBy(tableData.value, sortedBy.value, isAscendingSorted.value);
});
</script>

<style scoped lang="scss">
@import "@/scss/main";
.hide_button {
    color: $na_color;
    font-size: 10px;
}

.hide_button:hover {
    color: $text-color;
}

.hidden_icon {
    position: relative;
    top: -1px;
}

.hidden {
    display: none !important;
}

.hidden_row {
    color: $na_color;
    border-left: 2px solid $na_light_color;
    background-color: #f9f9f9;
}
</style>
