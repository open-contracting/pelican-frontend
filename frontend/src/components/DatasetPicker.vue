<template>
    <span v-if="!loading">        
        <b-container class="px-0">
            <b-row class="action_bar no-gutters">
                <b-col class="col-4 text-left">
                    <b-input-group class="search_input">
                        <template v-slot:prepend>
                            <b-input-group-text>
                                <font-awesome-icon icon="search"/>
                            </b-input-group-text>
                        </template>
                        <b-form-input v-model="search" :placeholder="$t('dataset.search')" />
                    </b-input-group>
                </b-col>
            </b-row>
        </b-container>

        <table class="table table-hover table-borderless container">
            <thead>
                <tr class="d-flex">
                    <th class="col-4 align-self-center clickable" @click="sortBy('id')">
                        <SortButtons :label="$t('dataset.id')" :active="sortedBy == 'id'" :asc="isAscendingSorted"
                            :on-asc="() => sortBy('id')" :on-desc="() => sortBy('id', false)" />
                    </th>
                    <th class="col-1 align-self-center clickable" @click="sortBy('size')">
                        <SortButtons :label="$t('dataset.size')" :active="sortedBy == 'size'" :asc="isAscendingSorted"
                            :on-asc="() => sortBy('size')" :on-desc="() => sortBy('size', false)" />
                    <th class="col-3 align-self-center clickable" @click="sortBy('phase')">
                        <SortButtons :label="$t('dataset.phase')" :active="sortedBy == 'phase'" :asc="isAscendingSorted"
                            :on-asc="() => sortBy('phase')" :on-desc="() => sortBy('phase', false)" />
                    </th>
                    <th class="col align-self-center clickable" @click="sortBy('created')">
                        <SortButtons :active="sortedBy == 'created'" :asc="isAscendingSorted"
                            :on-asc="() => sortBy('created')" :on-desc="() => sortBy('created', false)">
                            <span class="created">{{ $t("created") }}</span>
                            <br/>
                            <span class="modified">{{ $t("modified") }}</span>
                        </SortButtons>                        
                    </th>
                    <th class="col">&nbsp;</th>
                </tr>
            </thead>

            <tbody>
                <template v-for="(item, index) in datasets">
                    <tr v-if="isSearched(item.name)" v-bind:key="index" @click="setDataset(item)" class="clickable d-flex align-items-center">
                        <td class="col-4">{{ item.name }}</td>
                        <td class="col-1 numeric">{{ item.size | formatNumber }}</td>
                        <td class="col-3 phase_cell">
                            <!-- <ProgressBar v-if="item.state == 'FAILED'" :failed="getDatasetProgress(item)" />
                            <ProgressBar v-else-if="item.phase == 'CHECKED' && item.state == 'OK'" :ok="100" />
                            <ProgressBar v-else :value="getDatasetProgress(item)" /> -->

                            <template v-if="item.phase == 'CHECKED' && item.state == 'OK'">
                                <font-awesome-icon :icon="['far', 'check-circle']" class="text-success"/> {{ item.phase }}
                            </template>
                            <template v-else-if="item.state == 'FAILED'">
                                <font-awesome-icon :icon="['far', 'times-circle']" class="text-danger"/> {{ item.phase }}
                            </template>
                            <template v-else>
                                <b-row class="progress_label">
                                    <b-col v-for="p in phases" :key="p">
                                        <template v-if="p == item.phase">
                                            <font-awesome-icon v-if="item.state == 'FAILED'" icon="exclamation-triangle" class="state-failed" />
                                            {{ p }}
                                        </template>
                                    </b-col>
                                </b-row>

                                <ProgressBar  :value="getDatasetProgress(item)" />
                            </template>
                        </td>
                        <td class="col numeric text-right">
                            <span class="created">{{ item.created }}</span><br/>
                            <span class="modified">{{ item.modified }}</span>
                        </td>
                        <td class="col text-right">
                            <button v-if="item.ancestor_id" class="btn btn-sm btn-outline-primary time_varinace"
                                @click.stop="setDataset(item, {name: 'time'})"
                                :title="getDatasetName(item.ancestor_id)"
                            >
                                <div class="d-flex align-items-center">
                                    <font-awesome-icon icon="history"/><span class="label">{{ getDatasetName(item.ancestor_id) }}</span>
                                </div>
                            </button>
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
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
import searchFieldMixins from "@/plugins/searchFieldMixins.js";

export default {
    mixins: [stateMixin, sortMixins, searchFieldMixins],
    data: function() {
        return {
            datasets: [],
            loading: false,
            afterUpdateRoute: {name: "overview"}
        };
    },
    components: {
        Loader,
        ProgressBar,
        SortButtons
    },
    computed: {
        phases: function() {
            return ['PLANNED','CONTRACTING_PROCESS','DATASET','TIME_VARIANCE','CHECKED']
        },
        states: function() {
            return ['WAITING', 'IN_PROGRESS', 'OK', 'FAILED']
        },
        sortedBy: function() {
            var value = this.$store.getters.datasetSortedBy
            return value == null ? this.defaultSorting.by : value
        },
        isAscendingSorted: function() {
            var value = this.$store.getters.datasetSortedAscending
            return value == null ? this.defaultSorting.asc : value
        },
        defaultSorting: function() {
            return {by: "created", asc: false}
        }
    },
    methods: {
        searchGetter: function() {
            return this.$store.getters.datasetSearch
        },
        searchSetter: function() {
            this.$store.commit("setDatasetSearch", this.search)
        },
        isSearched: function(name) {
            return !this.search || name.toLowerCase().includes(this.search.toLowerCase())
        },
        setDataset: function(dataset, route = {name: "overview"}) {
            this.loading = true;
            this.afterUpdateRoute = route
            if (this.$store.getters.datasetId != dataset.id) {
                this.$store.dispatch("updateDataset", dataset);
            } else {
                this.$router.push(this.afterUpdateRoute);
            }
        },
        getDatasetName: function(id) {
            if (this.datasets) {
                var ds = this.datasets.find(n => n.id == id)
                if (ds) {
                    return ds.name
                }
            }

            return null
        },
        getDatasetProgress: function(dataset) {
            return (this.phases.indexOf(dataset.phase) + 1) * 20
        },
        sortBy: function(by, asc = true) {
            if (!this.datasets) {
                return
            }

            var comp;
            if (by == "created") {
                comp = (a, b) => a.created.localeCompare(b.created)
            } else if (by == 'id') {
                comp = (a, b) => a.id.localeCompare(b.id)
            } else if (by == 'size') {
                comp = (a, b) => this.compareNumbers(a.size, b.size)
            } else if (by == 'phase') {
                comp = (a, b) => {
                    if (a.phase == b.phase) {
                        if (a.state == b.state) {
                            return a.id.localeCompare(b.id);
                        } else {
                            return this.compareNumbers(this.states.indexOf(a.state), this.states.indexOf(b.state))
                        }
                    } else {
                        return this.compareNumbers(this.phases.indexOf(a.phase), this.phases.indexOf(b.phase))
                    }                    
                }
            } else {
                throw new Error("Uknown sorting method " + by);
            }

            this.sort(this.datasets, comp, asc)
            this.$store.commit('setDatasetSorting', {by: by, asc: asc})
        }
    },
    mounted() {
        var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.dataset;
            var self = this;
            axios
                .get(url)
                .then(response => {
                    this.datasets = response["data"]["objects"]
                    this.sortBy(this.sortedBy, this.isAscendingSorted)
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
@import "src/scss/variables";

table {
    tbody {
        tr {
            border-bottom: 1px solid $na_light_color;
        }
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

        &:nth-of-type(2), &:nth-of-type(4), &:nth-of-type(5) {
            white-space: nowrap;
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

    .btn.time_varinace {
        font-family: $font-family-thin;

        .label {
            max-width: 100px;
            display: inline-block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            margin-left: 4px;
        }
    }
}

.action_bar {
    margin-top: 15px;
    margin-bottom: 15px;

    .search_input {
        .input-group-text {
            background-color: transparent;
            border-right: none;
        }
        input {
            background-color: transparent;
            border-left: none;
        }
    }
}
</style>