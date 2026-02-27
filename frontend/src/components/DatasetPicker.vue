<template>
  <span v-if="!loading">
    <div class="picker_table">
      <div class="row">
        <div class="search_input col col-12 col-md-4">
          <SearchInput
            :placeholder="$t('dataset.search')"
            :preset="search"
            :on-update="search => $store.commit('setDatasetSearch', search)"
          />
        </div>
      </div>
      <div class="thr row">
        <div
          class="th col-4 align-self-center clickable"
          @click="sortBy('name')"
        >
          <SortButtons
            :label="$t('dataset.name')"
            :active="sortedBy == 'name'"
            :asc="isAscendingSorted"
            :on-asc="() => sortBy('name')"
            :on-desc="() => sortBy('name', false)"
          />
        </div>
        <div
          class="th col-1 align-self-center clickable"
          @click="sortBy('size')"
        >
          <SortButtons
            :label="$t('dataset.size')"
            :active="sortedBy == 'size'"
            :asc="isAscendingSorted"
            :on-asc="() => sortBy('size')"
            :on-desc="() => sortBy('size', false)"
          />
        </div>
        <div
          class="th col-1 align-self-center clickable"
          @click="sortBy('collection_id')"
        >
          <SortButtons
            :label="$t('kingfisherId')"
            :active="sortedBy == 'collection_id'"
            :asc="isAscendingSorted"
            :on-asc="() => sortBy('collection_id')"
            :on-desc="() => sortBy('collection_id', false)"
          />
        </div>
        <div
          class="th col-1 align-self-center clickable"
          @click="sortBy('phase')"
        >
          <SortButtons
            :label="$t('dataset.phase')"
            :active="sortedBy == 'phase'"
            :asc="isAscendingSorted"
            :on-asc="() => sortBy('phase')"
            :on-desc="() => sortBy('phase', false)"
          />
        </div>
        <div
          class="th col align-self-center clickable"
          @click="sortBy('created')"
        >
          <SortButtons
            :active="sortedBy == 'created'"
            :asc="isAscendingSorted"
            :on-asc="() => sortBy('created')"
            :on-desc="() => sortBy('created', false)"
          >
            <span class="created">{{ $t("created") }}</span>
            <br>
            <span class="modified">{{ $t("modified") }}</span>
          </SortButtons>
        </div>
        <div class="th col align-self-center text-start">{{ $t("dataset.timeVariance") }}</div>
      </div>

      <template v-for="(item, index) in datasets" :key="index">
        <DatasetPickerRow
          v-if="isSearched(item.name)"
          :dataset="item"
          :depth="0"
          @dataset-filter="showFilter($event)"
          @dataset-report="showReport($event)"
        />
      </template>
    </div>
    <BModal
      id="filter-modal"
      ref="filter-modal"
      size="lg"
      no-footer
      :title="$t('datasetFilter.headline')"
      teleport-disabled
      lazy
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
    >
      <DatasetReportModal
        :dataset="reportDataset"
        @close="hideReportModal"
      />
    </BModal>
  </span>
  <span v-else>
    <Loader />
  </span>
</template>

<script setup>
import axios from "axios";
import { BModal } from "bootstrap-vue-next";
import { computed, onMounted, ref, useTemplateRef } from "vue";
import { useStore } from "vuex";
import { CONFIG, PHASES, STATES } from "@/config.js";
import DatasetFilterModal from "./DatasetFilterModal.vue";
import DatasetPickerRow from "./DatasetPickerRow.vue";
import DatasetReportModal from "./DatasetReportModal.vue";
import Loader from "./Loader.vue";
import SearchInput from "./SearchInput.vue";
import SortButtons from "./SortButtons.vue";

const store = useStore();

const datasets = ref([]);
const loading = ref(false);
const filteredDataset = ref(null);
const reportDataset = ref(null);

const filterModal = useTemplateRef("filter-modal");
const reportModal = useTemplateRef("report-modal");

const search = computed(() => store.getters.datasetSearch);
const sortedBy = computed(() => {
    const value = store.getters.datasetSortedBy;
    return value == null ? "created" : value;
});
const isAscendingSorted = computed(() => {
    const value = store.getters.datasetSortedAscending;
    return value == null ? false : value;
});

function showFilter(dataset) {
    filteredDataset.value = dataset;
    filterModal.value.show();
}

function showReport(dataset) {
    reportDataset.value = dataset;
    reportModal.value.show();
}

function hideFilterModal() {
    filterModal.value.hide();
}

function hideReportModal() {
    reportModal.value.hide();
}

function isSearched(name) {
    return !search.value || name.toLowerCase().includes(search.value.toLowerCase());
}

function sortBy(by, asc = true) {
    if (!datasets.value) {
        return;
    }

    let comp;
    if (by === "created") {
        comp = (a, b) => a.created.localeCompare(b.created);
    } else if (by === "name") {
        comp = (a, b) => a.name.localeCompare(b.name);
    } else if (by === "size") {
        comp = (a, b) =>
            (a.meta.compiled_releases?.total_unique_ocids || -1) -
            (b.meta.compiled_releases?.total_unique_ocids || -1);
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
    store.commit("setDatasetSorting", { by: by, asc: asc });
}

onMounted(() => {
    const buildDatasetsTree = (allDatasets, parent_id) => {
        const result = [];
        for (const item of allDatasets) {
            if (item.parent_id === parent_id) {
                item.filtered_children = buildDatasetsTree(allDatasets, item.id);
                result.push(item);
            }
        }
        return result;
    };

    axios
        .get(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}`)
        .then((response) => {
            datasets.value = buildDatasetsTree(response.data, null);
            for (const item of datasets.value) {
                item.ancestor_name = item.ancestor_id && datasets.value.find((e) => e.id === item.ancestor_id)?.name;
            }
            sortBy(sortedBy.value, isAscendingSorted.value);
        })
        .catch((error) => {
            throw new Error(error);
        });
});
</script>

<style scoped lang="scss">
@import "@/scss/main";

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

.th {
    .modified {
        font-family: $font-family-thin;
        color: $headings_light_color;
    }
}

.td {
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
