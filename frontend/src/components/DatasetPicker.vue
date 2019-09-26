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
                        <b-form-input v-model="search" :placeholder="$t('field.search')" />
                    </b-input-group>
                </b-col>
            </b-row>
        </b-container>

        <table class="table table-hover table-borderless container">
            <thead>
                <tr class="d-flex">
                    <th class="col-4">{{ $t("dataset.id") }}</th>
                    <th class="col-1">{{ $t("dataset.size") }}</th>
                    <th class="col-3">{{ $t("dataset.phase") }}</th>
                    <th class="col">
                        <span class="created">{{ $t("created") }}</span>
                        <br/>
                        <span class="modified">{{ $t("modified") }}</span>
                    </th>
                    <th class="col">&nbsp;</th>
                </tr>
            </thead>

            <tbody>
                <template v-for="(item, index) in datasets">
                    <tr v-if="isSearched(item.name)" v-bind:key="index" @click="setDataset(item)" class="clickable d-flex align-items-center">
                        <td class="col-4">{{ item.name }}</td>
                        <td class="col-1 text-right numeric">{{ item.size | formatNumber }}</td>
                        <td class="col-3">
                            {{ item.phase }}
                            <font-awesome-icon v-if="item.state == 'FAILED'" icon="exclamation-triangle" class="state-in-failed" size="2x" title="FAILED"/>
                            <ProgressBar v-else :value="getDatasetProgress(item)" />
                            <!-- <font-awesome-icon v-if="item.state == 'WAITING'" icon="history" class="state-waiting" size="2x" title="WAITING"/>
                            <font-awesome-icon v-if="item.state == 'IN_PROGRESS'" icon="cogs" class="state-in-progress" size="2x" title="IN_PROGRESS"/>
                            <font-awesome-icon v-if="item.state == 'OK'" :icon="['far', 'check-square']" class="state-in-progress" size="2x" title="OK"/>
                            -->
                        </td>
                        <td class="col numeric text-right mx-auto">
                            <span class="created">{{ item.created }}</span><br/>
                            <span class="modified">{{ item.modified }}</span>
                        </td>
                        <td class="col">
                            <button v-if="item.ancestor_id" class="btn btn-primary" @click.stop="setDataset(item, {name: 'time'})">
                                <font-awesome-icon icon="history"/> {{ getDatasetName(item.ancestor_id) }}
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
        ProgressBar
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
        getDatasetProgress: function(ds) {
            if (ds.state == "WAITING") {
                return 0
            } else if (ds.state == "IN_PROGRESS") {
                return 50
            } else if (ds.state == "OK") {
                return 100
            } else {
                return 0
            }
        }
    },
    mounted() {
        var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.dataset;
            var self = this;
            axios
                .get(url)
                .then(function(response) {
                    // desc sort by created timestamp
                    self.datasets = response["data"]["objects"]
                    self.sort(self.datasets, (a, b) => a.created.localeCompare(b.created), false)
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
        white-space: nowrap;

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