<template>
    <div
        class="card mb-4 dataset_result_box result_box"
        v-bind:class="{ clickable: check.result != undefined, undef: check.result == undefined }"
        v-on:click="detail(check.name)"
    >
        <div class="card-body">
            <div class="row no-gutters">
                <div class="col col-10 col-sm-10 col-lg-10">
                    <h5 class="check_headline">{{ $t("datasetLevel." + check.name + ".name") }}</h5>
                </div>

                <div class="col col-2 col-sm-2 col-lg-2 text-right">
                    <span v-if="check.result == true" class="badge badge-pill ok_status">{{ $t("passed") }}</span>
                    <span v-if="check.result == false" class="badge badge-pill failed_status">{{ $t("failed") }}</span>
                </div>
            </div>

            <div class="row no-gutters">
                <div class="col col-12">
                    <p class="check_description" v-html="$t('datasetLevel.' + check.name + '.description')"></p>
                </div>
            </div>
        </div>

        <div class="card-body">
            <div class="row no-gutters justify-content-end">
                <div class="col col-12">
                    <div class="chart_envelope text-center" v-if="check.result == undefined">
                        <img class="undefined_image" src="/img/unsufficient_data.png" />
                        <br />
                        <div class="undefined_title">{{ $t("unsufficientData.title") }}</div>
                        <p v-html="$t('unsufficientData.description')"></p>
                    </div>
                    <div v-else>
                        <div v-if="checkType == 'donut'">
                            <div class="chart_envelope">
                                <DonutChart :check="check"></DonutChart>
                            </div>
                        </div>

                        <div v-if="checkType == 'bar'">
                            <div class="chart_envelope">
                                <BarChart :check="check"></BarChart>
                            </div>
                        </div>

                        <div v-if="checkType == 'numeric'" class="text-center">
                            <span class="check_numeric_value">{{ check.meta.total_passed }}</span>
                            <span class="check_numeric_count">&nbsp;/&nbsp;{{ check.meta.total_processed }}</span>
                        </div>

                        <div class="top3" v-if="checkType == 'top3'">
                            <div class="chart_envelope">
                                <table id="top3_table" class="table table-sm">
                                    <tr v-for="(item, index) in check.meta.most_frequent" v-bind:key="index">
                                        <td>{{ item.value_str }}</td>
                                        <td class="text-right numeric">{{ Math.round(item.share * 100) / 100 | formatNumber2D}}%</td>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <div class="biggest_share" v-if="checkType == 'biggest_share'">
                            <div class="row">
                                <div
                                    class="col col-12 text-center total_share"
                                    v-bind:class="{ color_failed: check.result == false, color_ok: check.result == true }"
                                >{{ Math.round(check.meta.ocid_share * 10000) / 100 }}%</div>
                            </div>
                            <div class="row">
                                <div
                                    class="col col-12 text-center ocid_count"
                                >{{ check.meta.ocid_count | formatNumber }}&nbsp;from&nbsp;{{ check.meta.total_ocid_count | formatNumber }} {{ $t("ocids") }}</div>
                            </div>
                        </div>

                        <div class="single_value_share" v-if="checkType == 'single_value_share'">
                            <div class="chart_envelope">
                                <BarChartSingleValue :check="check"></BarChartSingleValue>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DonutChart from "@/components/DonutChart.vue";
import BarChart from "@/components/BarChart.vue";
import BarChartSingleValue from "@/components/BarChartSingleValue.vue";
import datasetMixin from "@/plugins/datasetMixins.js";

export default {
    data: function() {
        return {};
    },
    components: { DonutChart, BarChart, BarChartSingleValue },
    props: ["check"],
    mixins: [datasetMixin],
    methods: {
        onePercent: function() {
            return (this.check.ok + this.check.failed + this.check.na) / 100;
        },
        detail: function(name) {
            if (this.check.result != undefined) {
                this.$router.push({
                    name: "datasetCheckDetail",
                    params: {
                        check: name,
                        datasetId: this.$store.getters.datasetId
                    }
                });
            }
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.chart_envelope {
    margin-bottom: 10px;
}

.ok_status {
    background-color: $ok_color;
    color: white;
    font-size: 10px;
    padding: 8px;
}

.failed_status {
    background-color: $failed_color;
    color: white;
    font-size: 10px;
    padding: 8px;
}

.card-body {
    padding: 15px;
}

.check_headline {
    overflow-wrap: break-word;
    margin-bottom: 20px;
}

.check_description {
    overflow-wrap: break-word;
    color: $headings_light_color;
}

.ok_icon {
    color: $ok_color;
}

.dataset_result_box {
    display: inline-block;
    background-color: white;
    padding: 5px;
    border-radius: 10px;
    border: 0px;
}

.dataset_result_box h5 {
    font-size: 15px;
    margin-top: 3px;
}

.dataset_result_box p {
    font-size: 13px;
}

.failed_icon {
    color: $failed_color;
}

.check_numeric_value {
    font-size: 60px;
    font-weight: 700;
}

.check_numeric_count {
    font-size: 30px;
    font-weight: 700;
}

#top3_table > tr:nth-child(1) > td {
    border-top: none;
}

.biggest_share .total_share {
    font-size: 70px;
    font-weight: 700;
}

.biggest_share .ocid_count {
    font-size: 15px;
    font-weight: 700;
}
</style>