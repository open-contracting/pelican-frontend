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
        fieldLevelFilterIndex: 0,
        fieldLevelFilter: () => true,
        resourceLevelFilterIndex: 0,
        datasetLevelFilterIndex: 0,
        timeLevelFilterIndex: 0,
    },
    getters: {
        fieldLevelFilterIndex: (state) => {
            return state.fieldLevelFilterIndex;
        },
        fieldLevelFilter: (state) => {
            return state.fieldLevelFilter;
        },
        resourceLevelFilterIndex: (state) => {
            return state.resourceLevelFilterIndex;
        },
        datasetLevelFilterIndex: (state) => {
            return state.datasetLevelFilterIndex;
        },
        timeLevelFilterIndex: (state) => {
            return state.timeLevelFilterIndex;
        },
        settings: (state) => {
            return state.settings;
        },
        dataset: (state) => {
            return state.dataset;
        },
        datasetId: (state) => {
            // "[vue-router] missing param for named route "overview": Expected "datasetId" to be defined"
            // When refreshing a subpage, state.dataset is not set by setDataset() until loadDataset() is called.
            return state.dataset?.id;
        },
        resourceLevelStats: (state) => {
            return state.resourceLevelStats;
        },
        datasetLevelStats: (state) => {
            return state.datasetLevelStats;
        },
        timeVarianceLevelStats: (state) => {
            return state.timeVarianceLevelStats;
        },
        resourceLevelStatsBySection: (state) => (sectionName) => {
            if (state.resourceLevelStats != null) {
                return state.resourceLevelStats.filter((item) => item.name.startsWith(sectionName));
            }

            return [];
        },
        resourceLevelCheckByName: (state) => (checkName) => {
            return state.resourceLevelStats?.find((item) => item.name === checkName);
        },
        datasetLevelCheckByName: (state) => (checkName) => {
            return state.datasetLevelStats?.find((item) => item.name === checkName);
        },
        dataItemById: (state) => (itemId) => {
            return state.dataItems?.find((item) => item.id === itemId);
        },
        dataItemJSONLines: (state) => (itemId) => {
            const dataItem = state.dataItems?.find((item) => item.id === itemId);
            if (dataItem) {
                return JSON.stringify(dataItem.data, null, 2).split("\n").length;
            }
            return null;
        },
        dataItemJSON: (state) => (itemId) => {
            const dataItem = state.dataItems?.find((item) => item.id === itemId);
            if (dataItem) {
                return JSON.stringify(dataItem.data, null, 2);
            }
            return null;
        },
        fieldLevelStats: (state) => {
            return state.fieldLevelStats;
        },
        fieldLevelCheckByPath: (state) => (path) => {
            return state.fieldLevelStats?.find((item) => item.path === path);
        },
        fieldCheckLayout: (state) => state.fieldCheckLayout,
        isFieldCheckExpanded: (state) => (path) => {
            return !!state.fieldCheckExpandedNodes?.includes(path);
        },
        timeVarianceLevelCheckByName: (state) => (checkName) => {
            return state.timeVarianceLevelStats?.find((item) => item.name === checkName);
        },
        fieldCheckSortedBy: (state) => {
            return state.fieldCheckSorting?.by;
        },
        fieldCheckSortedAscending: (state) => {
            return state.fieldCheckSorting?.asc;
        },
        fieldCheckSearch: (state) => {
            return state.fieldCheckSearch;
        },
        datasetSearch: (state) => {
            return state.datasetSearch;
        },
        datasetSortedBy: (state) => {
            return state.datasetSorting?.by;
        },
        datasetSortedAscending: (state) => {
            return state.datasetSorting?.asc;
        },
        isResourceCheckExpanded: (state) => (section) => {
            return !!state.resourceCheckExpandedNodes?.includes(section);
        },
    },
    mutations: {
        setFieldLevelFilterIndex(state, newFieldLevelFilterIndex) {
            state.fieldLevelFilterIndex = newFieldLevelFilterIndex;
        },
        setFieldLevelFilter(state, newFieldLevelFilter) {
            state.fieldLevelFilter = newFieldLevelFilter;
        },
        setResourceLevelFilterIndex(state, newResourceLevelFilterIndex) {
            state.resourceLevelFilterIndex = newResourceLevelFilterIndex;
        },
        setDatasetLevelFilterIndex(state, newDatasetLevelFilterIndex) {
            state.datasetLevelFilterIndex = newDatasetLevelFilterIndex;
        },
        setTimeLevelFilterIndex(state, newTimeLevelFilterIndex) {
            state.timeLevelFilterIndex = newTimeLevelFilterIndex;
        },
        setSettings(state, settings) {
            state.settings = settings;
        },
        setDataset(state, newDataset) {
            state.dataset = newDataset;
        },
        setResourceLevelStats(state, stats) {
            state.resourceLevelStats = stats;
        },
        setResourceLevelCheckDetail(state, { name, data }) {
            let updatedStats = [];
            updatedStats = updatedStats.concat(state.resourceLevelStats);
            updatedStats.forEach((item, i) => {
                if (item.name === name) Object.assign(updatedStats[i], data);
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
            let updatedStats = [];
            updatedStats = updatedStats.concat(state.fieldLevelStats);

            updatedStats.forEach((item, i) => {
                if (item.path === path) Object.assign(updatedStats[i], data);
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
            state.fieldCheckExpandedNodes = state.fieldCheckExpandedNodes.filter((v) => !v.startsWith(path));
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
            state.resourceCheckExpandedNodes = state.resourceCheckExpandedNodes.filter((v) => !v.startsWith(section));
        },
    },
    actions: {
        loadSettings({ commit }) {
            return new Promise((resolve) => {
                axios
                    .get(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.settings}`)
                    .then((response) => {
                        commit("setSettings", response.data);
                        resolve();
                    })
                    .catch((error) => {
                        throw new Error(error);
                    });
            });
        },
        loadDataset({ dispatch, commit }, datasetId) {
            return new Promise((resolve) => {
                axios
                    .get(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}${datasetId}`)
                    .then((response) => {
                        dispatch("resetDatasetEnv");
                        commit("setDataset", response.data);
                        Promise.all([
                            dispatch("loadResourceLevelStats"),
                            dispatch("loadDatasetLevelStats"),
                            dispatch("loadTimeVarianceLevelStats"),
                            dispatch("loadFieldLevelStats"),
                        ]).then(() => {
                            resolve();
                        });
                    })
                    .catch((error) => {
                        throw new Error(error);
                    });
            });
        },
        loadResourceLevelStats({ commit, state }) {
            return new Promise((resolve) => {
                commit("setResourceLevelStats", null);
                const formatted = CONFIG.apiEndpoints.resourceLevelReport.replace(/{id}/g, state.dataset.id);
                axios
                    .get(`${CONFIG.apiBaseUrl}${formatted}`)
                    .then((response) => {
                        const data = [];
                        for (const key in response.data) {
                            response.data[key].name = key;
                            data.push(response.data[key]);
                        }
                        commit("setResourceLevelStats", data);
                        resolve();
                    })
                    .catch((error) => {
                        throw new Error(error);
                    });
            });
        },
        loadResourceLevelCheckDetail({ commit, state, getters }, checkName) {
            return new Promise((resolve) => {
                const checkDetail = getters.resourceLevelCheckByName(checkName);

                if (checkDetail != null && !checkDetail.examplesLoaded) {
                    if (state.dataset != null && checkName != null) {
                        const formatted = CONFIG.apiEndpoints.resourceLevelDetail
                            .replace(/{id}/g, state.dataset.id)
                            .replace(/{name}/g, checkName);
                        axios
                            .get(`${CONFIG.apiBaseUrl}${formatted}`)
                            .then((response) => {
                                response.data.examples_filled = true;
                                commit("setResourceLevelCheckDetail", {
                                    name: checkName,
                                    data: response.data,
                                });
                                resolve();
                            })
                            .catch((error) => {
                                throw new Error(error);
                            });
                    }
                }
            });
        },
        loadDatasetLevelStats({ commit, state }) {
            return new Promise((resolve) => {
                commit("setDatasetLevelStats", null);
                const formatted = CONFIG.apiEndpoints.datasetLevelReport.replace(/{id}/g, state.dataset.id);
                axios
                    .get(`${CONFIG.apiBaseUrl}${formatted}`)
                    .then((response) => {
                        const data = [];
                        for (const key in response.data) {
                            response.data[key].name = key;
                            data.push(response.data[key]);
                        }
                        commit("setDatasetLevelStats", data);
                        resolve();
                    })
                    .catch((error) => {
                        throw new Error(error);
                    });
            });
        },
        loadDataItem({ commit, state }, itemId) {
            return new Promise((resolve, reject) => {
                let dataItem = null;
                if (state.dataItems) {
                    dataItem = state.dataItems.find((item) => item.id === itemId);
                }
                if (dataItem == null) {
                    const formatted = CONFIG.apiEndpoints.dataItem.replace(/{id}/g, itemId);
                    axios
                        .get(`${CONFIG.apiBaseUrl}${formatted}`)
                        .then((response) => {
                            commit("addDataItem", response.data);
                            resolve();
                        })
                        .catch((error) => {
                            reject(error);
                        });
                } else {
                    resolve();
                }
            });
        },
        loadFieldLevelStats({ commit, state }) {
            return new Promise((resolve) => {
                commit("setFieldLevelStats", null);

                const okShare = (item) => {
                    const result = (item.passed_count / item.total_count) * 100;
                    return Number.isNaN(result) ? 0 : result;
                };

                const failedShare = (item) => {
                    const result = (item.failed_count / item.total_count) * 100;
                    return Number.isNaN(result) ? 0 : result;
                };

                const formatted = CONFIG.apiEndpoints.fieldLevelReport.replace(/{id}/g, state.dataset.id);
                axios
                    .get(`${CONFIG.apiBaseUrl}${formatted}`)
                    .then((response) => {
                        const data = [];
                        for (const key in response.data) {
                            const item = response.data[key];
                            data.push(
                                Object.assign({}, item, {
                                    path: key,
                                    coverageOkShare: okShare(item.coverage),
                                    coverageFailedShare: failedShare(item.coverage),
                                    qualityOkShare: okShare(item.quality),
                                    qualityFailedShare: failedShare(item.quality),
                                }),
                            );
                            resolve();
                        }

                        commit("setFieldLevelStats", data);
                        commit("resetFieldCheckSorting");
                    })
                    .catch((error) => {
                        throw new Error(error);
                    });
            });
        },
        loadFieldLevelCheckDetail({ commit, state, getters }, path) {
            const checkDetail = getters.fieldLevelCheckByPath(path);

            if (checkDetail == null || (checkDetail != null && !checkDetail.examplesLoaded)) {
                if (state.dataset != null && path != null) {
                    const formatted = CONFIG.apiEndpoints.fieldLevelDetail
                        .replace(/{id}/g, state.dataset.id)
                        .replace(/{name}/g, path);
                    axios
                        .get(`${CONFIG.apiBaseUrl}${formatted}`)
                        .then((response) => {
                            response.data.examples_filled = true;
                            commit("setFieldLevelCheckDetail", {
                                path: path,
                                data: response.data,
                            });
                        })
                        .catch((error) => {
                            throw new Error(error);
                        });
                }
            }
        },
        loadTimeVarianceLevelStats({ commit, state }) {
            return new Promise((resolve) => {
                commit("setTimeVarianceLevelStats", null);
                const formatted = CONFIG.apiEndpoints.timeVarianceLevelReport.replace(/{id}/g, state.dataset.id);
                axios
                    .get(`${CONFIG.apiBaseUrl}${formatted}`)
                    .then((response) => {
                        const data = [];
                        for (const key in response.data) {
                            response.data[key].name = key;
                            data.push(response.data[key]);
                        }
                        commit("setTimeVarianceLevelStats", data);
                        resolve();
                    })
                    .catch((error) => {
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
            const isPathSearched = (path) => {
                return !!path?.toLowerCase().includes(getters.fieldCheckSearch.toLowerCase());
            };

            if (getters.fieldLevelStats) {
                commit("collapseAllFieldCheckExpandedNodes");

                if (getters.fieldCheckSearch) {
                    let nodes = [];
                    const remaining = [];
                    // select paths that match the search
                    for (const n of getters.fieldLevelStats) {
                        if (isPathSearched(n.path)) {
                            nodes.push(n.path);
                        } else {
                            remaining.push(n.path);
                        }
                    }

                    // add parents
                    for (const n of remaining) {
                        if (nodes.some((m) => m.startsWith(`${n}.`))) {
                            nodes.push(n);
                        }
                    }

                    // collapse matched nodes without matching child
                    const matched = [...nodes];
                    nodes = nodes.filter((n) => {
                        return (
                            // keep parent without match
                            !isPathSearched(n) ||
                            matched.some((m) => {
                                return m.startsWith(`${n}.`) && isPathSearched(m.substr(n.length));
                            })
                        );
                    });

                    commit("setFieldCheckExpandedNodes", nodes);
                }
            }
        },
    },
});
