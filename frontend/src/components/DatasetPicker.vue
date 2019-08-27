<template>
    <span v-if="!loading">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th class="col-3" scope="col">{{ $t("dataset.id") }}</th>
                    <th class="col-2 text-center" scope="col">{{ $t("dataset.size") }}</th>
                    <th class="col-2 text-center" scope="col">{{ $t("dataset.phase") }}</th>
                    <th class="col-2 text-center" scope="col">
                        {{ $t("created") }}
                        <br />
                        {{ $t("modified") }}
                    </th>
                    <th class="col-1" scope="col">&nbsp;</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in datasets" v-bind:key="index">
                    <td>{{ item.dataset_id }}</td>
                    <td class="text-right">{{ item.size | formatNumber }}</td>
                    <td>{{ item.phase }}</td>
                    <td>
                        {{ item.created }}
                        <br />
                        {{ item.modified }}
                    </td>
                    <td>
                        <button @click.prevent="setDatasetId(item.dataset_id)" class="btn btn-primary mb-4" type="submit">{{ $t("selectDataset") }}</button>
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
            datasetId: "uk_2019-08-23_14:42:39",
            loading: false
        };
    },
    components: {
        Loader
    },
    methods: {
        setDatasetId: function(datasetId) {
            this.loading = true;
            if (this.$store.getters.datasetId != datasetId) {
                this.$store.dispatch("updateDatasetId", datasetId);
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
        atLeastOneLoaded: function(newValue, oldValue) {
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