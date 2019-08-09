import Vue from 'vue'
import Vuex from 'vuex'
const axios = require('axios');
import {
    CONFIG
} from "./config.js";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        datasetId: null,
        resourceLevelStats: null,
    },
    getters: {
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
        }
    },
    mutations: {
        setDatasetId(state, newId) {
            state.datasetId = newId;
        },
        setResourceLevelStats(state, stats) {
            state.resourceLevelStats = stats;
        },
    },
    actions: {
        updateDatasetId({
            dispatch,
            commit
        }, newId) {
            commit("setDatasetId", newId);
            dispatch("loadResourceLevelStats");
        },
        loadResourceLevelStats({
            commit,
            state
        }) {
            var url = CONFIG.api.baseUrl + CONFIG.api.endpoints.resourceLevelStats + "/" + state.datasetId;
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
                    console.log(error);
                })
        }
    }
})