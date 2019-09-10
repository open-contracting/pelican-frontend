import Vue from 'vue'
import Vuex from 'vuex'
const axios = require('axios');
import {
    CONFIG
} from "./config.js";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        dataset: null,
        resourceLevelStats: null,
        resourceCheckExamples: null,
        datasetLevelStats: null,
        dataItems: [],
    },
    getters: {
        dataset: (state) => {
            return state.dataset;
        },
        datasetId: (state) => {
            return state.dataset ? state.dataset.id : null;
        },
        resourceLevelStats: (state) => {
            return state.resourceLevelStats;
        },
        datasetLevelStats: (state) => {
            return state.datasetLevelStats;
        },
        resourceLevelStatsBySection: (state) => (sectionName) => {
            if (state.resourceLevelStats) {
                return state.resourceLevelStats.filter(item => item.name.startsWith(sectionName));
            }

            return [];
        },
        resourceLevelCheckByName: (state) => (checkName) => {
            if (state.resourceLevelStats) {
                return state.resourceLevelStats.find(item => item.name === checkName);
            }

            return [];
        },
        datasetLevelCheckByName: (state) => (checkName) => {
            if (state.datasetLevelStats) {
                return state.datasetLevelStats.find(item => item.name === checkName);
            }

            return [];
        },
        dataItemById: (state) => (itemId) => {
            if (state.dataItems) {
                var dataItem = state.dataItems.find(item => item.id === itemId);
                if (dataItem != null) {
                    return dataItem;
                }
            }

            return null;
        }
    },
    mutations: {
        setDataset(state, newDataset) {
            state.dataset = newDataset;
        },
        setResourceLevelStats(state, stats) {
            state.resourceLevelStats = stats;
        },
        setResourceLevelCheckDetail(state, data) {
            state.resourceLevelStats.forEach(function (item, i) { if (item.name == data.name) state.resourceLevelStats[i] = data; });
            //state.resourceLevelStats = stats;
        },
        setDatasetLevelStats(state, stats) {
            state.datasetLevelStats = stats;
        },
        addDataItem(state, item) {
            state.dataItems.push(item);
        },
    },
    actions: {
        updateDataset({
            dispatch,
            commit
        }, newDataset) {
            commit("setDataset", newDataset);
            dispatch("loadResourceLevelStats");
            dispatch("loadDatasetLevelStats");
        },
        loadResourceLevelStats({
            commit,
            state
        }) {
            commit("setResourceLevelStats", null);
            var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.resourceLevelStats + "/" + state.dataset.id;
            axios.get(url)
                .then(function (response) {
                    var data = [];
                    for (var key in response["data"]) {
                        response["data"][key]["name"] = key;
                        data.push(response["data"][key]);
                    }
                    commit("setResourceLevelStats", data);
                })
                .catch(function (error) {
                    throw new Error(error);
                })
        },
        loadResourceLevelCheckDetail({
            commit,
            state
        }, checkName) {
            var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.resourceLevelCheckDetail + "/" + state.dataset.id + "/" + checkName;
            axios.get(url)
                .then(function (response) {
                    response["data"]["name"] = checkName;
                    commit("setResourceLevelCheckDetail", response["data"]);
                })
                .catch(function (error) {
                    throw new Error(error);
                })
        },
        loadDatasetLevelStats({
            commit,
            state
        }) {
            commit("setDatasetLevelStats", null);
            var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.datasetLevelStats + "/" + state.dataset.id;
            axios.get(url)
                .then(function (response) {
                    var data = [];
                    for (var key in response["data"]) {
                        response["data"][key]["name"] = key;
                        data.push(response["data"][key]);
                    }
                    commit("setDatasetLevelStats", data);
                })
                .catch(function (error) {
                    throw new Error(error);
                })
        },
        loadDataItem({
            commit,
            state
        }, itemId) {
            var dataItem = null;
            if (state.dataItems) {
                dataItem = state.dataItems.find(item => item.id === itemId);
            }
            if (dataItem == null) {
                var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.dataItem + "/" + itemId;
                axios.get(url)
                    .then(function (response) {
                        commit("addDataItem", response["data"]);
                    })
                    .catch(function (error) {
                        throw new Error(error);
                    })
            }
        },
    }
})