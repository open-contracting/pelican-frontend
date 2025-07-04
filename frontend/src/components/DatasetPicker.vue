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
        <div class="th col align-self-center text-left">{{ $t("dataset.timeVariance") }}</div>
      </div>

      <template v-for="(item, index) in datasets">
        <DatasetPickerRow
          v-if="isSearched(item.name)"
          :key="index"
          :dataset="item"
          :depth="0"
          @dataset-filter="showFilter($event)"
          @dataset-report="showReport($event)"
        />
      </template>
    </div>
    <b-modal
      id="filter-modal"
      ref="filter-modal"
      size="lg"
      hide-footer
      :title="$t('datasetFilter.headline')"
      static
      lazy
    >
      <DatasetFilterModal :dataset="filteredDataset" />
    </b-modal>
    <b-modal
      id="report-modal"
      ref="report-modal"
      size="lg"
      hide-footer
      :title="$t('datasetReport.headline')"
      static
      lazy
    >
      <DatasetReportModal
        :dataset="reportDataset"
        @close="hideReportModal"
      />
    </b-modal>
  </span>
  <span v-else>
    <Loader />
  </span>
</template>

<script>
const axios = require("axios");
import DatasetFilterModal from "@/components/DatasetFilterModal.vue";
import DatasetPickerRow from "@/components/DatasetPickerRow.vue";
import DatasetReportModal from "@/components/DatasetReportModal.vue";
import Loader from "@/components/Loader.vue";
import SearchInput from "@/components/SearchInput.vue";
import SortButtons from "@/components/SortButtons.vue";
import { CONFIG } from "@/config.js";
import sortMixins from "@/plugins/sortMixins.js";
import stateMixin from "@/plugins/stateMixins.js";

export default {
    components: {
        Loader,
        SortButtons,
        SearchInput,
        DatasetPickerRow,
        DatasetFilterModal,
        DatasetReportModal,
    },
    mixins: [stateMixin, sortMixins],
    data: () => ({
        datasets: [],
        loading: false,
        filteredDataset: null,
        reportDataset: null,
    }),
    computed: {
        search: function () {
            return this.$store.getters.datasetSearch;
        },
        phases: () => ["PLANNED", "CONTRACTING_PROCESS", "DATASET", "TIME_VARIANCE", "CHECKED"],
        states: () => ["WAITING", "IN_PROGRESS", "OK", "FAILED"],
        sortedBy: function () {
            const value = this.$store.getters.datasetSortedBy;
            return value == null ? "created" : value;
        },
        isAscendingSorted: function () {
            const value = this.$store.getters.datasetSortedAscending;
            return value == null ? false : value;
        },
    },
    mounted() {
        const buildDatasetsTree = (datasets, parent_id) => {
            const result = [];
            for (const item of datasets) {
                if (item.parent_id === parent_id) {
                    item.filtered_children = buildDatasetsTree(datasets, item.id);
                    result.push(item);
                }
            }

            return result;
        };
        axios
            .get(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}`)
            .then((response) => {
                this.datasets = buildDatasetsTree(response.data, null);
                for (const item of this.datasets) {
                    item.ancestor_name = item.ancestor_id && this.datasets.find((e) => e.id === item.ancestor_id).name;
                }
                this.sortBy(this.sortedBy, this.isAscendingSorted);
            })
            .catch((error) => {
                throw new Error(error);
            });
    },
    methods: {
        showFilter: function (dataset) {
            this.filteredDataset = dataset;
            this.$bvModal.show("filter-modal");
        },
        showReport: function (dataset) {
            this.reportDataset = dataset;
            this.$bvModal.show("report-modal");
        },
        isSearched: function (name) {
            return !this.search || name.toLowerCase().includes(this.search.toLowerCase());
        },
        sortBy: function (by, asc = true) {
            if (!this.datasets) {
                return;
            }

            let comp;
            if (by === "created") {
                comp = (a, b) => a.created.localeCompare(b.created);
            } else if (by === "name") {
                comp = (a, b) => a.name.localeCompare(b.name);
            } else if (by === "size") {
                comp = (a, b) =>
                    this.compareNumbers(
                        a.meta.compiled_releases?.total_unique_ocids || -1,
                        b.meta.compiled_releases?.total_unique_ocids || -1,
                    );
            } else if (by === "collection_id") {
                comp = (a, b) =>
                    this.compareNumbers(
                        a.meta.kingfisher_metadata?.collection_id || -1,
                        b.meta.kingfisher_metadata?.collection_id || -1,
                    );
            } else if (by === "phase") {
                comp = (a, b) => {
                    if (a.phase === b.phase) {
                        if (a.state === b.state) {
                            return this.compareNumbers(a.id, b.id);
                        }
                        return this.compareNumbers(this.states.indexOf(a.state), this.states.indexOf(b.state));
                    }
                    return this.compareNumbers(this.phases.indexOf(a.phase), this.phases.indexOf(b.phase));
                };
            } else {
                throw new Error(`Unknown sorting method ${by}`);
            }

            this.sort(this.datasets, comp, asc);
            this.$store.commit("setDatasetSorting", { by: by, asc: asc });
        },
        hideReportModal: function () {
            this.$bvModal.hide("report-modal");
        },
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

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
