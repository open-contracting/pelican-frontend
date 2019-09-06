<template>
    <dashboard-detail>
        <template v-slot:content>
            <h3>{{ $t("header").toUpperCase() }}</h3>
            <div class="row">
                <div class="col col-10">
                    <h2>{{ $t("datasetLevel." + check.name + ".name") }}</h2>
                </div>
                <div class="col col-2">
                    <span v-if="check.result == true" class="badge badge-pill ok_status">{{ $t("passed") }}</span>
                    <span v-if="check.result == false" class="badge badge-pill failed_status">{{ $t("failed") }}</span>
                </div>
            </div>
            <p>{{ $t("datasetLevel." + check.name + ".description") }}</p>

            <div class="result_box">
                <div v-if="checkType == 'bar'">
                    <BarChartBig :check="check"></BarChartBig>
                </div>

                <div v-if="checkType == 'donut'">
                    <table class="table table-borderless table-sm">
                        <tbody>
                            <tr v-for="share in shares" class="d-flex" v-bind:key="share[0]">
                                <td class="col-3 text-right label">
                                    <span class="check_name">{{ share[0] }}</span>
                                </td>
                                <td class="col-9 text-right">
                                    <InlineBar :count="share[1]['count']" :percentage="Math.round(share[1]['share'] * 10000) / 100" :state="'reg'" />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-if="checkType == 'top3'">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>{{ $t("top3.value") }}</th>
                                <th class="text-center">{{ $t("top3.share") }}</th>
                                <th class="text-center">{{ $t("top3.count") }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in check.meta.most_frequent" v-bind:key="index">
                                <td>{{ item.value_str }}</td>
                                <td class="text-right numeric">{{ Math.round(item.share * 100) / 100}}%</td>
                                <td class="text-right numeric">{{ item.count | formatNumber }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <ExampleBoxes :examples="examples" v-on:preview="preview"></ExampleBoxes>
        </template>

        <template v-slot:preview>
            <h5>{{ $t("preview.metadata") }}</h5>
            <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewMetadata"></vue-json-pretty>

            <div class="divider">&nbsp;</div>
            <span v-if="previewData">
                <h5>{{ $t("preview.ocds_data") }}</h5>
                <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewData"></vue-json-pretty>
            </span>
        </template>
    </dashboard-detail>
</template>

<script>
import BarChartBig from "@/components/BarChartBig";
import InlineBar from "@/components/InlineBar";
import VueJsonPretty from "vue-json-pretty";
import datasetMixin from "@/plugins/datasetMixins.js";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import ExampleBoxes from "@/components/ExampleBoxes.vue";

export default {
    name: "datasetCheckDetail",
    mixins: [datasetMixin],
    data: function() {
        return {
            check: null,
            previewDataItemId: null,
            previewMetadata: null,
            examples: null
        };
    },
    components: {
        BarChartBig,
        VueJsonPretty,
        DashboardDetail,
        InlineBar,
        ExampleBoxes
    },
    created() {
        this.check = this.$store.getters.datasetLevelCheckByName(
            this.$route.params.check
        );
        this.previewMetadata = this.check.meta;

        if (this.checkType == "donut") {
            this.examples = [];
            for (var key in this.shares) {
                if (this.shares[key][1].examples.length > 0) {
                    this.examples.push([
                        this.shares[key][0],
                        this.shares[key][1].examples
                    ]);
                }
            }
        }

        if (this.checkType == "bar") {
            this.examples = [];
            for (var barKey in this.check.meta.examples) {
                if (this.check.meta.examples[barKey].length > 0) {
                    this.examples.push([
                        barKey,
                        this.check.meta.examples[barKey]
                    ]);
                }
            }
        }

        if (this.checkType == "top3") {
            this.examples = [];
            var mostFrequent = this.check.meta.most_frequent;
            for (var topKey in mostFrequent) {
                if (mostFrequent[topKey].examples.length > 0) {
                    this.examples.push([
                        mostFrequent[topKey].value_str,
                        mostFrequent[topKey].examples
                    ]);
                }
            }
        }
    },
    methods: {
        preview: function(itemId) {
            this.$store.dispatch("loadDataItem", itemId);
            this.previewDataItemId = itemId;
        }
    },
    computed: {
        shares() {
            if (this.checkType == "donut") {
                return this.orderedShares(this.check.meta.shares);
            } else {
                return null;
            }
        },
        previewData() {
            return this.$store.getters.dataItemById(this.previewDataItemId);
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.ok_status {
    background-color: $ok_color;
    color: white;
    font-size: 15px;
    padding: 10px;
}

.failed_status {
    background-color: $failed_color;
    color: white;
    font-size: 15px;
    padding: 10px;
}

.label {
    padding-top: 6px;
}
</style>