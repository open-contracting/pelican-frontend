<template>
  <table class="data_table">
    <thead>
      <tr>
        <th @click="setSorting('path')">
          <SortButtons
            :label="$t('field.path')"
            :active="sortedBy == 'path'"
            :asc="isAscendingSorted"
            @asc="setSorting('path')"
            @desc="setSorting('path', false)"
          />
        </th>
        <th @click="setSorting('coverage')">
          <div class="d-flex justify-content-center">
            <SortButtons
              :label="$t('field.coverage')"
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
              :label="$t('field.quality')"
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
          v-slot="{ to }"
          :check="n"
        >
          <RouterLink
            class="check_link"
            :to="to"
          ><MarkedText :segments="highlightSearch(n.path)" /></RouterLink>
        </FieldCheckTableRow>
      </template>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import { useDatasetStore } from "@/stores/dataset.js";
import { useUiStore } from "@/stores/ui.js";
import type { FieldLevelCheck } from "@/types.js";
import FieldCheckTableRow from "./FieldCheckTableRow.vue";
import MarkedText from "./MarkedText.vue";
import SortButtons from "./SortButtons.vue";

const props = defineProps<{
  filter: (check: FieldLevelCheck) => boolean;
}>();
const datasetStore = useDatasetStore();
const ui = useUiStore();

const { sorted, setSorting, highlightSearch, isPathSearched } = useFieldCheckSearch();

const stats = computed(() => datasetStore.fieldLevelStats);
const sortedBy = computed(() => {
  const value = ui.fieldCheckSorting?.by;
  return value == null ? "processingOrder" : value;
});
const isAscendingSorted = computed(() => {
  const value = ui.fieldCheckSorting?.asc;
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

function isSearched(check: FieldLevelCheck | undefined) {
  return check && isPathSearched(check.path);
}

// Field.vue calls resetSorting() through a template ref.
defineExpose({ resetSorting });
</script>

