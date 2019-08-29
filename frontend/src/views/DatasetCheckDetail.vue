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
                                <td class="col-3 text-right">
                                    <span class="check_name">{{ $t(share[0]) }}</span>
                                </td>
                                <td class="col-9 text-right">
                                    <InlineBar :count="share[1]['count']" :percentage="Math.round(share[1]['share'] * 10000) / 100" :state="'reg'" />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <ExampleBoxes :examples="examples"></ExampleBoxes>
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
            previewData: null,
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
                this.examples.push([
                    this.shares[key][0],
                    this.shares[key][1].examples,
                    false
                ]);
            }
        }
    },
    methods: {},
    computed: {
        shares() {
            if (this.checkType == "donut") {
                return this.orderedShares(this.check.meta.shares);
            } else {
                return null;
            }
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
</style>