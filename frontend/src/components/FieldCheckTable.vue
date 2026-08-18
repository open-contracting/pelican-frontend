<template>
  <table class="data_table">
    <thead>
      <tr>
        <th @click="setSorting('path')">
          <SortButtons
            :label="$t('field.table.head.object')"
            :active="sortedBy == 'path'"
            :asc="isAscendingSorted"
            @asc="setSorting('path')"
            @desc="setSorting('path', false)"
          />
        </th>
        <th @click="setSorting('coverage')">
          <div class="d-flex justify-content-center">
            <SortButtons
              :label="$t('field.table.head.coverage')"
              :active="sortedBy == 'coverage'"
              :asc="isAscendingSorted"
              @asc="setSorting('coverage')"
              @desc="setSorting('coverage', false)"
            />
          </div>
        </th>
        <th @click="setSorting('quality')">
          <div class="d-flex justify-content-center">
            <SortButtons
              :label="$t('field.table.head.quality')"
              :active="sortedBy == 'quality'"
              :asc="isAscendingSorted"
              @asc="setSorting('quality')"
              @desc="setSorting('quality', false)"
            />
          </div>
        </th>
      </tr>
    </thead>

    <tbody>
      <template v-for="n in tableData" :key="n.path">
        <FieldCheckTableRow
          v-if="isSearched(n)"
          :check="n"
        >
          <span v-html="highlightSearch(n.path)" />
        </FieldCheckTableRow>
      </template>
    </tbody>
  </table>
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import FieldCheckTableRow from "./FieldCheckTableRow.vue";
import SortButtons from "./SortButtons.vue";

const props = defineProps(["filter"]);
const store = useStore();

const { sorted, setSorting, highlightSearch, isPathSearched } = useFieldCheckSearch();

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

  return sorted(
    stats.value.filter((n) => n.coverage.total_count && props.filter(n)),
    sortedBy.value,
    isAscendingSorted.value,
  );
});

function resetSorting() {
  setSorting("processingOrder");
}

function isSearched(check) {
  return check && isPathSearched(check.path);
}

// Field.vue calls resetSorting() through a template ref.
defineExpose({ resetSorting });
</script>

