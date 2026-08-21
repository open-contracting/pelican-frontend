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
        <template v-for="(item, index) in datasets" :key="index">
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

function sortBy(by: string, asc = true) {
  if (!datasets.value) {
    return;
  }

  let comp: (a: DatasetNode, b: DatasetNode) => number;
  if (by === "created") {
    comp = (a, b) => (a.created ?? "").localeCompare(b.created ?? "");
  } else if (by === "name") {
    comp = (a, b) => a.name.localeCompare(b.name);
  } else if (by === "size") {
    comp = (a, b) =>
      (a.meta.compiled_releases?.total_unique_ocids || -1) - (b.meta.compiled_releases?.total_unique_ocids || -1);
  } else if (by === "collection_id") {
    comp = (a, b) =>
      (a.meta.kingfisher_metadata?.collection_id || -1) - (b.meta.kingfisher_metadata?.collection_id || -1);
  } else if (by === "phase") {
    comp = (a, b) => {
      if (a.phase === b.phase) {
        if (a.state === b.state) {
          return a.id - b.id;
        }
        return STATES.indexOf(a.state) - STATES.indexOf(b.state);
      }
      return PHASES.indexOf(a.phase) - PHASES.indexOf(b.phase);
    };
  } else {
    throw new Error(`Unknown sorting method ${by}`);
  }

  datasets.value.sort((a, b) => (asc ? comp(a, b) : comp(b, a)));
  ui.datasetSorting = { by: by, asc: asc };
}

onMounted(() => {
  const buildDatasetsTree = (allDatasets: DatasetNode[], parent_id: number | null) => {
    const result = [];
    for (const item of allDatasets) {
      if (item.parent_id === parent_id) {
        item.filtered_children = buildDatasetsTree(allDatasets, item.id);
        result.push(item);
      }
    }
    return result;
  };

  api
    .get<Dataset[]>(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}`)
    .then((data) => {
      datasets.value = buildDatasetsTree(data as DatasetNode[], null);
      for (const item of datasets.value) {
        if (item.ancestor_id) {
          item.ancestor_name = datasets.value.find((e) => e.id === item.ancestor_id)?.name;
        }
      }
      sortBy(sortedBy.value, isAscendingSorted.value);
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
