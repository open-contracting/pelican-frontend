<template>
    <span v-if="!loading">
        <div class="picker_table">
            <div class="row">
                <div class="search_input col col-12 col-md-4">
                    <SearchInput :placeholder="$t('dataset.search')" :preset="search" :on-update="(search) => $store.commit('setDatasetSearch', search)" />
                </div>
            </div>
            <div class="row">
                <div class="th col-4 align-self-center clickable" @click="sortBy('id')">
                    <SortButtons
                        :label="$t('dataset.id')"
                        :active="sortedBy == 'id'"
                        :asc="isAscendingSorted"
                        :on-asc="() => sortBy('id')"
                        :on-desc="() => sortBy('id', false)"
                    />
                </div>
                <div class="th col-1 align-self-center clickable" @click="sortBy('size')">
                    <SortButtons
                        :label="$t('dataset.size')"
                        :active="sortedBy == 'size'"
                        :asc="isAscendingSorted"
                        :on-asc="() => sortBy('size')"
                        :on-desc="() => sortBy('size', false)"
                    />
                </div>
                <div class="th col-2 align-self-center clickable" @click="sortBy('phase')">
                    <SortButtons
                        :label="$t('dataset.phase')"
                        :active="sortedBy == 'phase'"
                        :asc="isAscendingSorted"
                        :on-asc="() => sortBy('phase')"
                        :on-desc="() => sortBy('phase', false)"
                    />
                </div>
                <div class="th col align-self-center clickable" @click="sortBy('created')">
                    <SortButtons
                        :active="sortedBy == 'created'"
                        :asc="isAscendingSorted"
                        :on-asc="() => sortBy('created')"
                        :on-desc="() => sortBy('created', false)"
                    >
                        <span class="created">{{ $t("created") }}</span>
                        <br />
                        <span class="modified">{{ $t("modified") }}</span>
                    </SortButtons>
                </div>
                <div class="td col align-self-center text-left">{{ $t('dataset.timeVariance')}}</div>
            </div>

            <template v-for="(item, index) in datasets">
                <div
                    v-if="isSearched(item.name)"
                    v-bind:key="index"
                    @click="setDataset(item)"
                    :class="['row','tr', 'clickable', 'align-items-center', {disabled: !isDatasetImported(item)}]"
                >
                    <div class="td col-4">
                        {{ item.name }}
                        <span class="dataset_id">( {{ item.id }} )</span>
                    </div>
                    <div class="td col-1 numeric">{{ item.size | formatNumber }}</div>
                    <div class="td col-2 phase_cell">
                        <template v-if="item.phase == 'CHECKED' && item.state == 'OK'">
                            <font-awesome-icon :icon="['far', 'check-circle']" class="text-success" />
                            {{ item.phase }}
                        </template>
                        <template v-else-if="item.state == 'FAILED'">
                            <font-awesome-icon :icon="['far', 'times-circle']" class="text-danger" />
                            {{ item.phase }}
                        </template>
                        <template v-else>
                            <b-row class="progress_label no-gutters">
                                <b-col v-for="p in phases" :key="p">
                                    <template v-if="p == item.phase">{{ p }}</template>
                                </b-col>
                            </b-row>

                            <ProgressBar :value="getDatasetProgress(item)" />
                        </template>
                    </div>
                    <div class="td col numeric">
                        <span class="created">{{ item.created }}</span>
                        <br />
                        <span class="modified">{{ item.modified }}</span>
                    </div>
                    <div class="td col">
                        <b-link
                            v-if="item.ancestor_id"
                            class="time_varinace break_word"
                            @click.stop="setDataset(item, {name: 'time'})"
                            :title="getDatasetName(item.ancestor_id)"
                        >
                            <font-awesome-icon icon="history" />
                            {{ getDatasetName(item.ancestor_id) }}
                        </b-link>
                    </div>
                </div>
            </template>
        </div>
    </span>
    <span v-else>
        <Loader></Loader>
    </span>
</template>

<script>
const axios = require("axios");
import { CONFIG } from "@/config.js";
import Loader from "@/components/Loader.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import SortButtons from "@/components/SortButtons.vue";
import stateMixin from "@/plugins/stateMixins.js";
import sortMixins from "@/plugins/sortMixins.js";
import SearchInput from "@/components/SearchInput.vue";

export default {
    mixins: [stateMixin, sortMixins],
    data: function() {
        return {
            datasets: [],
            loading: false,
            afterUpdateRoute: { name: "overview" }
        };
    },
    components: {
        Loader,
        ProgressBar,
        SortButtons,
        SearchInput
    },
    computed: {
        search: function() {
            return this.$store.getters.datasetSearch;
        },
        phases: function() {
            return [
                "PLANNED",
                "CONTRACTING_PROCESS",
                "DATASET",
                "TIME_VARIANCE",
                "CHECKED"
            ];
        },
        states: function() {
            return ["WAITING", "IN_PROGRESS", "OK", "FAILED"];
        },
        sortedBy: function() {
            var value = this.$store.getters.datasetSortedBy;
            return value == null ? this.defaultSorting.by : value;
        },
        isAscendingSorted: function() {
            var value = this.$store.getters.datasetSortedAscending;
            return value == null ? this.defaultSorting.asc : value;
        },
        defaultSorting: function() {
            return { by: "created", asc: false };
        }
    },
    methods: {
        isSearched: function(name) {
            return (
                !this.search ||
                name.toLowerCase().includes(this.search.toLowerCase())
            );
        },
        setDataset: function(dataset, route = { name: "overview" }) {
            if (!this.isDatasetImported(dataset)) {
                return;
            }

            this.loading = true;
            this.afterUpdateRoute = route;
            if (this.$store.getters.datasetId != dataset.id) {
                this.$store.dispatch("updateDataset", dataset);
            } else {
                this.$router.push(this.afterUpdateRoute);
            }
        },
        getDatasetName: function(id) {
            if (this.datasets) {
                var ds = this.datasets.find(n => n.id == id);
                if (ds) {
                    return ds.name;
                }
            }

            return null;
        },
        getDatasetProgress: function(dataset) {
            return (this.phases.indexOf(dataset.phase) + 1) * 20;
        },
        sortBy: function(by, asc = true) {
            if (!this.datasets) {
                return;
            }

            var comp;
            if (by == "created") {
                comp = (a, b) => a.created.localeCompare(b.created);
            } else if (by == "id") {
                comp = (a, b) => a.id.localeCompare(b.id);
            } else if (by == "size") {
                comp = (a, b) => this.compareNumbers(a.size, b.size);
            } else if (by == "phase") {
                comp = (a, b) => {
                    if (a.phase == b.phase) {
                        if (a.state == b.state) {
                            return a.id.localeCompare(b.id);
                        } else {
                            return this.compareNumbers(
                                this.states.indexOf(a.state),
                                this.states.indexOf(b.state)
                            );
                        }
                    } else {
                        return this.compareNumbers(
                            this.phases.indexOf(a.phase),
                            this.phases.indexOf(b.phase)
                        );
                    }
                };
            } else {
                throw new Error("Uknown sorting method " + by);
            }

            this.sort(this.datasets, comp, asc);
            this.$store.commit("setDatasetSorting", { by: by, asc: asc });
        },
        isDatasetImported: function(dataset) {
            return dataset.phase == "CHECKED" && dataset.state == "OK";
        }
    },
    mounted() {
        var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.dataset;
        axios
            .get(url)
            .then(response => {
                this.datasets = response["data"]["objects"];
                this.sortBy(this.sortedBy, this.isAscendingSorted);
            })
            .catch(function(error) {
                throw new Error(error);
            });
    },
    watch: {
        atLeastOneLoaded: function(newValue) {
            if (newValue) {
                this.$router.push(this.afterUpdateRoute);
            }
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.picker_table {
    padding: 30px;
}

.search_input {
    margin-bottom: 20px;
}

.tr {
    &.disabled {
        cursor: not-allowed;

        a {
            cursor: not-allowed;
            &:hover {
                text-decoration: none;
            }
        }
    }
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

.time_varinace {
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