<template>
    <span v-if="!loading">
        <table class="table table-hover container">
            <thead>
                <tr class="d-flex">
                    <th class="col-4">{{ $t("dataset.id") }}</th>
                    <th class="col-2 text-center">{{ $t("dataset.size") }}</th>
                    <th class="col-1 text-center">{{ $t("dataset.phase") }}</th>
                    <th class="col-3 text-center">
                        {{ $t("created") }}
                        /
                        {{ $t("modified") }}
                    </th>
                    <th class="col-2">&nbsp;</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in datasets" v-bind:key="index" class="d-flex">
                    <td class="col-4">{{ item.name }}</td>
                    <td class="col-2 text-right numeric">{{ item.size | formatNumber }}</td>
                    <td class="col-1">{{ item.phase }}</td>
                    <td class="col-3 numeric text-right">
                        {{ item.created }}<br>
                        {{ item.modified }}
                    </td>
                    <td class="col-2">
                        <button @click.prevent="setDataset(item)" class="btn btn-primary mb-4" type="submit">{{ $t("dataset.selectDataset") }}</button>
                    </td>
                </tr>
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
import stateMixin from "@/plugins/stateMixins.js";

export default {
    mixins: [stateMixin],
    data: function() {
        return {
            datasets: [],
            loading: false
        };
    },
    components: {
        Loader
    },
    methods: {
        setDataset: function(dataset) {
            this.loading = true;
            if (this.$store.getters.datasetId != dataset.id) {
                this.$store.dispatch("updateDataset", dataset);
            } else {
                this.$router.push({
                    name: "overview"
                });
            }
        }
    },
    mounted() {
        var url = CONFIG.apiBaseUrl + CONFIG.apiEndpoints.dataset;
        var self = this;
        axios
            .get(url)
            .then(function(response) {
                self.datasets = response["data"]["objects"];
            })
            .catch(function(error) {
                throw new Error(error);
            });
    },
    watch: {
        atLeastOneLoaded: function(newValue) {
            if (newValue) {
                this.$router.push({
                    name: "overview"
                });
            }
        }
    }
};
</script>

<style scoped lang="scss">
</style>