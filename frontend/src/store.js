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
        resourceLevelStats: state => {
            return state.resourceLevelStats;
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
                    commit("setResourceLevelStats", response["data"])
                })
                .catch(function (error) {
                    console.log(error);
                })
        }
    }
})