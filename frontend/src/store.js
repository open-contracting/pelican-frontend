import Vue from "vue";
import Vuex from "vuex";
const axios = require("axios");
import { CONFIG } from "./config.js";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        dataset: null,
        resourceLevelStats: null,
        resourceCheckExamples: null,
        datasetLevelStats: null,
        dataItems: [],
        fieldLevelStats: null,
        timeVarianceLevelStats: null,
        fieldCheckLayout: "table",
        fieldCheckExpandedNodes: [],
        fieldCheckSorting: null,
        fieldCheckSearch: null,
        datasetSearch: null,
        datasetSorting: null,

        resourceCheckExpandedNodes: [],
        insufficientShown: true
    },
    getters: {
        insufficientShown: state => {
            return state.insufficientShown;
        },
        dataset: state => {
            return state.dataset;
        },
        datasetId: state => {
            return state.dataset ? state.dataset.id : null;
        },
        resourceLevelStats: state => {
            return state.resourceLevelStats;
        },
        datasetLevelStats: state => {
            return state.datasetLevelStats;
        },
        timeVarianceLevelStats: state => {
            return state.timeVarianceLevelStats;
        },
        resourceLevelStatsBySection: state => sectionName => {
            if (state.resourceLevelStats != null) {
                return state.resourceLevelStats.filter(item =>
                    item.name.startsWith(sectionName)
                );
            }

            return [];
        },
        resourceLevelCheckByName: state => checkName => {
            if (state.resourceLevelStats != null) {
                return state.resourceLevelStats.find(
                    item => item.name === checkName
                );
            }

            return null;
        },
        datasetLevelCheckByName: state => checkName => {
            if (state.datasetLevelStats) {
                return state.datasetLevelStats.find(
                    item => item.name === checkName
                );
            }

            return null;
        },
        dataItemById: state => itemId => {
            if (state.dataItems) {
                var dataItem = state.dataItems.find(item => item.id === itemId);
                if (dataItem != null) {
                    return dataItem;
                }
            }

            return null;
        },
        dataItemJSONLines: state => itemId => {
            if (state.dataItems) {
                var dataItem = state.dataItems.find(item => item.id === itemId);
                if (dataItem != null) {
                    return JSON.stringify(dataItem["data"], null, 4).split("\n").length;
                }
            }

            return null;
        },
        dataItemJSON: state => itemId => {
            if (state.dataItems) {
                var dataItem = state.dataItems.find(item => item.id === itemId);
                if (dataItem != null) {
                    return JSON.stringify(dataItem["data"], null, 4);
                }
            }

            return null;
        },
        fieldLevelStats: state => {
            return state.fieldLevelStats;
        },
        fieldLevelCheckByPath: state => path => {
            if (state.fieldLevelStats != null) {
                return state.fieldLevelStats.find(item => item.path === path);
            }

            return null;
        },
        fieldCheckLayout: function(state) {
            return state.fieldCheckLayout;
        },
        isFieldCheckExpanded: state => path => {
            if (state.fieldCheckExpandedNodes != null) {
                return state.fieldCheckExpandedNodes.includes(path);
            }

            return false;
        },
        timeVarianceLevelCheckByName: state => checkName => {
            if (state.timeVarianceLevelStats) {
                return state.timeVarianceLevelStats.find(
                    item => item.name === checkName
                );
            }

            return null;
        },
        fieldCheckSortedBy: state => {
            return state.fieldCheckSorting != null ?
                state.fieldCheckSorting.by :
                null;
        },
        fieldCheckSortedAscending: state => {
            return state.fieldCheckSorting != null ?
                state.fieldCheckSorting.asc :
                null;
        },
        fieldCheckSearch: state => {
            return state.fieldCheckSearch;
        },
        datasetSearch: state => {
            return state.datasetSearch;
        },
        datasetSortedBy: state => {
            return state.datasetSorting != null ?
                state.datasetSorting.by :
                null;
        },
        datasetSortedAscending: state => {
            return state.datasetSorting != null ?
                state.datasetSorting.asc :
                null;
        },
        isResourceCheckExpanded: state => section => {
            if (state.resourceCheckExpandedNodes != null) {
                return state.resourceCheckExpandedNodes.includes(section);
            }

            return false;
        },
        extensionDataByName: state => extensionName => {
            return state.dataset.meta.collection_metadata.extensions.find(item =>
                item.name.hasOwnProperty('en') ? item.name['en'] == extensionName : item.name == extensionName
            )
        }
    },
    mutations: {
        setInsufficientShown(state, newInsufficientShown) {
            state.insufficientShown = newInsufficientShown;
        },
        setDataset(state, newDataset) {
            state.dataset = newDataset;
        },
        setResourceLevelStats(state, stats) {
            state.resourceLevelStats = stats;
        },
        setResourceLevelCheckDetail(state, { name, data }) {
            var updatedStats = [];
            updatedStats = updatedStats.concat(state.resourceLevelStats);
            updatedStats.forEach(function(item, i) {
                if (item.name == name) Object.assign(updatedStats[i], data);
            });
            state.resourceLevelStats = updatedStats;
        },
        setDatasetLevelStats(state, stats) {
            state.datasetLevelStats = stats;
        },
        addDataItem(state, item) {
            state.dataItems.push(item);
        },
        setFieldLevelStats(state, stats) {
            state.fieldLevelStats = stats;
        },
        setFieldLevelCheckDetail(state, { path, data }) {
            var updatedStats = [];
            updatedStats = updatedStats.concat(state.fieldLevelStats);

            updatedStats.forEach(function(item, i) {
                if (item.path == path) Object.assign(updatedStats[i], data);
            });

            state.fieldLevelStats = updatedStats;
        },
        setFieldCheckLayout(state, layout) {
            state.fieldCheckLayout = layout;
        },
        addFieldCheckExpandedNode(state, path) {
            if (!state.fieldCheckExpandedNodes.includes(path)) {
                state.fieldCheckExpandedNodes.push(path);
            }
        },
        setFieldCheckExpandedNodes(state, nodes) {
            state.fieldCheckExpandedNodes = nodes;
        },
        removeFieldCheckExpandedNode(state, path) {
            state.fieldCheckExpandedNodes = state.fieldCheckExpandedNodes.filter(
                v => !v.startsWith(path)
            );
        },
        setTimeVarianceLevelStats(state, stats) {
            state.timeVarianceLevelStats = stats;
        },
        collapseAllFieldCheckExpandedNodes(state) {
            state.fieldCheckExpandedNodes = [];
        },
        setFieldCheckSorting(state, sorting) {
            state.fieldCheckSorting = sorting;
        },
        resetFieldCheckSorting(state) {
            state.fieldCheckSorting = null;
        },
        setFieldCheckSearch(state, search) {
            state.fieldCheckSearch = search;
        },
        setDatasetSearch(state, search) {
            state.datasetSearch = search;
        },
        setDatasetSorting(state, sorting) {
            state.datasetSorting = sorting;
        },
        resetDatasetSorting(state) {
            state.datasetSorting = null;
        },
        addResourceCheckExpandedNode(state, section) {
            if (!state.resourceCheckExpandedNodes.includes(section)) {
                state.resourceCheckExpandedNodes.push(section);
            }
        },
        removeResourceCheckExpandedNode(state, section) {
            state.resourceCheckExpandedNodes = state.resourceCheckExpandedNodes.filter(
                v => !v.startsWith(section)
            );
        },
    },
    actions: {
        updateDataset({ dispatch, commit }, newDataset) {
            dispatch("resetDatasetEnv");
            commit("setDataset", newDataset);
            dispatch("loadResourceLevelStats");
            dispatch("loadDatasetLevelStats");
            dispatch("loadFieldLevelStats");
            dispatch("loadTimeVarianceLevelStats");
        },
        loadDataset({ dispatch, commit }, datasetId) {
            var url =
                CONFIG.apiBaseUrl +
                CONFIG.apiEndpoints.dataset +
                "/" +
                datasetId;

            return new Promise(resolve => {
                axios
                    .get(url)
                    .then(response => {
                        dispatch("resetDatasetEnv");
                        commit("setDataset", response["data"]);
                        Promise.all([
                            dispatch("loadResourceLevelStats"),
                            dispatch("loadDatasetLevelStats"),
                            dispatch("loadTimeVarianceLevelStats"),
                            dispatch("loadFieldLevelStats")
                        ]).then(() => {
                            resolve();
                        });
                    })
                    .catch(function(error) {
                        throw new Error(error);
                    });
            });
        },
        loadResourceLevelStats({ commit, state }) {
            return new Promise(resolve => {
                commit("setResourceLevelStats", null);
                var url =
                    CONFIG.apiBaseUrl +
                    CONFIG.apiEndpoints.resourceLevelStats +
                    "/" +
                    state.dataset.id;
                axios
                    .get(url)
                    .then(function(response) {
                        var data = [];
                        for (var key in response["data"]) {
                            response["data"][key]["name"] = key;
                            data.push(response["data"][key]);
                        }
                        commit("setResourceLevelStats", data);
                        resolve();
                    })
                    .catch(function(error) {
                        throw new Error(error);
                    });
            });
        },
        loadResourceLevelCheckDetail({ commit, state, getters }, checkName) {
            return new Promise(resolve => {
                var checkDetail = getters.resourceLevelCheckByName(checkName);

                if (checkDetail != null && !checkDetail.examplesLoaded) {
                    if (state.dataset != null && checkName != null) {
                        var url =
                            CONFIG.apiBaseUrl +
                            CONFIG.apiEndpoints.resourceLevelCheckDetail +
                            "/" +
                            state.dataset.id +
                            "/" +
                            checkName;
                        axios
                            .get(url)
                            .then(function(response) {
                                response["data"]["examples_filled"] = true;
                                commit("setResourceLevelCheckDetail", {
                                    name: checkName,
                                    data: response["data"]
                                });
                                resolve();
                            })
                            .catch(function(error) {
                                throw new Error(error);
                            });
                    }
                }
            });
        },
        loadDatasetLevelStats({ commit, state }) {
            return new Promise(resolve => {
                commit("setDatasetLevelStats", null);
                var url =
                    CONFIG.apiBaseUrl +
                    CONFIG.apiEndpoints.datasetLevelStats +
                    "/" +
                    state.dataset.id;
                axios
                    .get(url)
                    .then(function(response) {
                        var data = [];
                        for (var key in response["data"]) {
                            response["data"][key]["name"] = key;
                            data.push(response["data"][key]);
                        }
                        commit("setDatasetLevelStats", data);
                        resolve();
                    })
                    .catch(function(error) {
                        throw new Error(error);
                    });
            });
        },
        loadDataItem({ commit, state }, itemId) {
            return new Promise(resolve => {
                var dataItem = null;
                if (state.dataItems) {
                    dataItem = state.dataItems.find(item => item.id === itemId);
                }
                if (dataItem == null) {
                    var url =
                        CONFIG.apiBaseUrl +
                        CONFIG.apiEndpoints.dataItem +
                        "/" +
                        itemId;
                    axios
                        .get(url)
                        .then(function(response) {
                            commit("addDataItem", response["data"]);
                            resolve();
                        })
                        .catch(function(error) {
                            throw new Error(error);
                        });
                } else {
                    resolve();
                }
            });
        },
        loadFieldLevelStats({ commit, state }) {
            return new Promise(resolve => {
                commit("setFieldLevelStats", null);

                var url =
                    CONFIG.apiBaseUrl +
                    CONFIG.apiEndpoints.fieldStats +
                    "/" +
                    state.dataset.id;

                var okShare = function(item) {
                    var result = (item.passed_count / item.total_count) * 100;
                    return isNaN(result) ? 0 : result;
                };

                var failedShare = function(item) {
                    var result = (item.failed_count / item.total_count) * 100;
                    return isNaN(result) ? 0 : result;
                };

                axios
                    .get(url)
                    .then(function(response) {
                        var data = [];
                        for (var key in response["data"]) {
                            var item = response["data"][key];
                            data.push(
                                Object.assign({}, item, {
                                    path: key,
                                    coverageOkShare: okShare(item.coverage),
                                    coverageFailedShare: failedShare(item.coverage),
                                    qualityOkShare: okShare(item.quality),
                                    qualityFailedShare: failedShare(item.quality)
                                })
                            );
                            resolve();
                        }

                        commit("setFieldLevelStats", data);
                        commit("resetFieldCheckSorting");
                    })
                    .catch(function(error) {
                        throw new Error(error);
                    });
            });
        },
        loadFieldLevelCheckDetail({ commit, state, getters }, path) {
            var checkDetail = getters.fieldLevelCheckByPath(path);

            if (
                checkDetail == null ||
                (checkDetail != null && !checkDetail.examplesLoaded)
            ) {
                if (state.dataset != null && path != null) {
                    var url =
                        CONFIG.apiBaseUrl +
                        CONFIG.apiEndpoints.fieldDetail +
                        "/" +
                        state.dataset.id +
                        "/" +
                        path;

                    var aaa = path;
                    axios
                        .get(url)
                        .then(function(response) {
                            response["data"]["examples_filled"] = true;
                            commit("setFieldLevelCheckDetail", {
                                path: aaa,
                                data: response["data"]
                            });
                        })
                        .catch(function(error) {
                            throw new Error(error);
                        });
                }
            }
        },
        loadTimeVarianceLevelStats({ commit, state }) {
            return new Promise(resolve => {
                commit("setTimeVarianceLevelStats", null);
                var url =
                    CONFIG.apiBaseUrl +
                    CONFIG.apiEndpoints.timeVarianceLevelStats +
                    "/" +
                    state.dataset.id;
                axios
                    .get(url)
                    .then(function(response) {
                        var data = [];
                        for (var key in response["data"]) {
                            response["data"][key]["name"] = key;
                            data.push(response["data"][key]);
                        }
                        commit("setTimeVarianceLevelStats", data);
                        resolve();
                    })
                    .catch(function(error) {
                        throw new Error(error);
                    });
            });
        },
        resetDatasetEnv({ commit }) {
            commit("setFieldLevelStats", null);
            commit("setDatasetLevelStats", null);
            commit("setResourceLevelStats", null);
            commit("resetFieldCheckSorting");
            commit("setFieldCheckSearch", null);
            commit("collapseAllFieldCheckExpandedNodes");
            commit("setFieldCheckLayout", "table");
        },
        setExpandedNodesForSearch({ getters, commit }) {
            var isPathSearched = function(path) {
                if (getters.fieldCheckSearch && path) {
                    var search_lc = getters.fieldCheckSearch.toLowerCase();
                    var path_lc = path.toLowerCase();
                    return path_lc.includes(search_lc);
                }

                return false;
            };

            if (getters.fieldLevelStats) {
                commit("collapseAllFieldCheckExpandedNodes");

                if (getters.fieldCheckSearch) {
                    var nodes = [];
                    var remaining = [];
                    // select paths that match the search
                    getters.fieldLevelStats.forEach(n => {
                        if (isPathSearched(n.path)) {
                            nodes.push(n.path);
                        } else {
                            remaining.push(n.path);
                        }
                    });

                    // add parents
                    remaining.forEach(n => {
                        if (nodes.some(m => m.startsWith(n + "."))) {
                            nodes.push(n);
                        }
                    });

                    // collapse matched nodes without matching child
                    var matched = [...nodes];
                    nodes = nodes.filter(n => {
                        // keep parent without match
                        if (!isPathSearched(n)) {
                            return true;
                        }

                        return matched.some(m => {
                            return (
                                m.startsWith(n + ".") &&
                                isPathSearched(m.substr(n.length))
                            );
                        });
                    });

                    commit("setFieldCheckExpandedNodes", nodes);
                }
            }
        }
    }
});