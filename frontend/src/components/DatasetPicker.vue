<template>
  <div class="picker_table">
    <div class="row">
      <div class="search_input col col-12 col-md-4">
        <SearchInput
          :placeholder="$t('dataset.search')"
          :preset="search"
          @search="ui.datasetSearch = $event"
        />
      </div>
    </div>
    <table class="data_table">
      <colgroup>
        <col style="width: 33.3333%">
        <col style="width: 8.3333%">
        <col style="width: 8.3333%">
        <col style="width: 8.3333%">
        <col style="width: 20.8333%">
        <col style="width: 20.8333%">
      </colgroup>
      <thead>
        <tr>
          <th
            class="clickable"
            @click="sortBy('name')"
          >
            <SortButtons
              :label="$t('dataset.name')"
              :active="sortedBy == 'name'"
              :asc="isAscendingSorted"
              @asc="sortBy('name')"
              @desc="sortBy('name', false)"
            />
          </th>
          <th
            class="clickable"
            @click="sortBy('size')"
          >
            <SortButtons
              :label="$t('dataset.size')"
              :active="sortedBy == 'size'"
              :asc="isAscendingSorted"
              @asc="sortBy('size')"
              @desc="sortBy('size', false)"
            />
          </th>
          <th
            class="clickable"
            @click="sortBy('collection_id')"
          >
            <SortButtons
              :label="$t('kingfisherId')"
              :active="sortedBy == 'collection_id'"
              :asc="isAscendingSorted"
              @asc="sortBy('collection_id')"
              @desc="sortBy('collection_id', false)"
            />
          </th>
          <th
            class="clickable"
            @click="sortBy('phase')"
          >
            <SortButtons
              :label="$t('dataset.phase')"
              :active="sortedBy == 'phase'"
              :asc="isAscendingSorted"
              @asc="sortBy('phase')"
              @desc="sortBy('phase', false)"
            />
          </th>
          <th
            class="clickable"
            @click="sortBy('created')"
          >
            <SortButtons
              :active="sortedBy == 'created'"
              :asc="isAscendingSorted"
              @asc="sortBy('created')"
              @desc="sortBy('created', false)"
            >
              <span class="created">{{ $t("created") }}</span>
              <br>
              <span class="modified">{{ $t("modified") }}</span>
            </SortButtons>
          </th>
          <th class="text-start">{{ $t("dataset.timeVariance") }}</th>
        </tr>
      </thead>

      <tbody>
        <tr v-if="isEmpty">
          <td colspan="6">{{ $t("dataset.empty") }}</td>
        </tr>
        <template v-for="(item, index) in sortedDatasets" :key="index">
          <DatasetPickerRow
            v-if="isSearched(item.name)"
            :dataset="item"
            :depth="0"
            @dataset-filter="showFilter($event)"
            @dataset-report="showReport($event)"
          />
        </template>
      </tbody>
    </table>
  </div>
  <BModal
    id="filter-modal"
    ref="filter-modal"
    size="lg"
    no-footer
    :title="$t('datasetFilter.headline')"
    teleport-disabled
    lazy
    unmount-lazy
  >
    <DatasetFilterModal
      :dataset="filteredDataset"
      @close="hideFilterModal"
    />
  </BModal>
  <BModal
    id="report-modal"
    ref="report-modal"
    size="lg"
    no-footer
    :title="$t('datasetReport.headline')"
    teleport-disabled
    lazy
    unmount-lazy
  >
    <DatasetReportModal
      :dataset="reportDataset"
      @close="hideReportModal"
    />
  </BModal>
</template>

<script setup lang="ts">
import { BModal } from "bootstrap-vue-next";
import { computed, onMounted, ref, useTemplateRef } from "vue";
import api from "@/api.js";
import { CONFIG, PHASES, STATES } from "@/config.js";
import { useUiStore } from "@/stores/ui.js";
import type { Dataset, DatasetNode } from "@/types.js";
import DatasetFilterModal from "./DatasetFilterModal.vue";
import DatasetPickerRow from "./DatasetPickerRow.vue";
import DatasetReportModal from "./DatasetReportModal.vue";
import SearchInput from "./SearchInput.vue";
import SortButtons from "./SortButtons.vue";

const ui = useUiStore();

const datasets = ref<DatasetNode[]>([]);
const isEmpty = ref(false);
const filteredDataset = ref<DatasetNode | null>(null);
const reportDataset = ref<DatasetNode | null>(null);

const filterModal = useTemplateRef<InstanceType<typeof BModal>>("filter-modal");
const reportModal = useTemplateRef<InstanceType<typeof BModal>>("report-modal");

const search = computed(() => ui.datasetSearch ?? undefined);
const sortedBy = computed(() => {
  const value = ui.datasetSorting?.by;
  return value == null ? "created" : value;
});
const isAscendingSorted = computed(() => {
  const value = ui.datasetSorting?.asc;
  return value == null ? false : value;
});

function showFilter(dataset: DatasetNode) {
  filteredDataset.value = dataset;
  filterModal.value?.show();
}

function showReport(dataset: DatasetNode) {
  reportDataset.value = dataset;
  reportModal.value?.show();
}

function hideFilterModal() {
  filterModal.value?.hide();
}

function hideReportModal() {
  reportModal.value?.hide();
}

function isSearched(name: string) {
  return !search.value || name.toLowerCase().includes(search.value.toLowerCase());
}

// A value missing from the list sorts last, rather than silently first.
function rank(values: readonly string[], value: string) {
  const index = values.indexOf(value);
  return index === -1 ? values.length : index;
}

function comparator(by: string): (a: DatasetNode, b: DatasetNode) => number {
  if (by === "created") {
    return (a, b) => (a.created ?? "").localeCompare(b.created ?? "");
  }
  if (by === "name") {
    return (a, b) => a.name.localeCompare(b.name);
  }
  if (by === "size") {
    // A dataset of 0 OCIDs has a size, unlike one whose metadata is not filled in yet.
    return (a, b) =>
      (a.meta.compiled_releases.total_unique_ocids ?? -1) - (b.meta.compiled_releases.total_unique_ocids ?? -1);
  }
  if (by === "collection_id") {
    return (a, b) =>
      (a.meta.kingfisher_metadata.collection_id ?? -1) - (b.meta.kingfisher_metadata.collection_id ?? -1);
  }
  if (by === "phase") {
    return (a, b) =>
      rank(PHASES, a.phase) - rank(PHASES, b.phase) || rank(STATES, a.state) - rank(STATES, b.state) || a.id - b.id;
  }
  throw new Error(`Unknown sorting method ${by}`);
}

const sortedDatasets = computed(() => {
  const compare = comparator(sortedBy.value);
  const direction = isAscendingSorted.value ? 1 : -1;
  return [...datasets.value].sort((a, b) => direction * compare(a, b));
});

function sortBy(by: string, asc = true) {
  ui.datasetSorting = { by, asc };
}

onMounted(() => {
  const buildDatasetsTree = (allDatasets: Dataset[], parentId: number | null): DatasetNode[] =>
    allDatasets
      .filter((item) => item.parent_id === parentId)
      .map((item) => ({ ...item, filtered_children: buildDatasetsTree(allDatasets, item.id) }));

  api
    .get<Dataset[]>(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}`)
    .then((data) => {
      const tree = buildDatasetsTree(data, null);
      for (const node of tree) {
        if (node.ancestor_id) {
          node.ancestor_name = data.find((item) => item.id === node.ancestor_id)?.name;
        }
      }

      datasets.value = tree;
      isEmpty.value = tree.length === 0;
    })
    .catch(() => {});
});
</script>

<style scoped lang="scss">

.form-control::placeholder {
    color: red;
}

.small_icon {
    position: relative;
    top: -1px;
}

.picker_table {
    padding: 30px;
}

.search_input {
    margin-bottom: 20px;
}

th {
    .modified {
        font-family: $font-family-thin;
        color: $headings_light_color;
    }
}

td {
    .created {
        font-weight: 700;
    }

    .modified {
        color: $headings_light_color;
    }

    &:nth-of-type(4) {
        white-space: nowrap;
    }

    .dataset_id {
        color: $na_color;
        font-family: $font-family-thin;
        font-size: 14px;
    }
}

.phase_cell {
    font-family: $font-family-thin;

    .progress_label {
        font-size: 11px;

        .col {
            white-space: nowrap;
        }

        .state-failed {
            color: $failed_color;
        }
    }
}

.time_variance {
    font-family: $font-family-thin;
    color: $primary;
    max-width: 110px;

    svg {
        margin-right: 4px;
    }
}

.action_bar {
    margin-top: 15px;
    margin-bottom: 15px;
}
</style>
