<template>
    <div class="dataset_result_box" v-bind:class="{ clickable: check.result != undefined, undef: check.result == undefined }" v-on:click="detail(check.name)">
        <div class="row no-gutters">
            <div class="col col-2 col-sm-2 col-lg-1 text-left">
                <span v-if="check.result == true" class="ok_icon">
                    <font-awesome-icon :icon="['far', 'check-circle']" />
                </span>
                <span v-if="check.result == false" class="failed_icon">
                    <font-awesome-icon :icon="['far', 'times-circle']" />
                </span>
                <span v-if="check.result == undefined" class="undefined_icon">
                    <font-awesome-icon :icon="['far', 'question-circle']" />
                </span>
            </div>

            <div class="col col-10 col-sm-10 col-lg-11">
                <div class="row">
                    <div class="col-12">
                        <h5>{{ $t("datasetLevel." + check.name + ".name") }}</h5>
                        <p>{{ $t("datasetLevel." + check.name + ".description") }}</p>
                    </div>
                </div>

                <div class="row h-100 align-items-center">
                    <div class="col-12">
                        <div class="chartEnvelope text-center" v-if="check.result == undefined">
                            <img class="undefined_image" src="/img/unsufficient_data.png" />
                            <br />
                            <div class="undefined_title">{{ $t("unsufficientData.title") }}</div>
                            <p>{{ $t("unsufficientData.description") }}</p>
                        </div>
                        <div v-else>
                            <div v-if="checkType == 'donut'">
                                <div class="chartEnvelope">
                                    <DonutChart :check="check"></DonutChart>
                                </div>
                            </div>

                            <div v-if="checkType == 'bar'">
                                <div class="chartEnvelope">
                                    <BarChart :check="check"></BarChart>
                                </div>
                            </div>

                            <div v-if="checkType == 'numeric'" class="text-center">
                                <span class="check_numeric_value">{{ check.meta.total_passed }}</span>
                                <span class="check_numeric_count">&nbsp;/&nbsp;{{ check.meta.total_processed }}</span>
                            </div>

                            <div class="top3" v-if="checkType == 'top3'">
                                <table class="table table-sm">
                                    <tr v-for="(item, index) in check.meta.most_frequent" v-bind:key="index">
                                        <td>{{ item.value_str }}</td>
                                        <td class="text-right numeric">{{ Math.round(item.share * 100) / 100}}%</td>
                                    </tr>
                                </table>
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
import datasetMixin from "@/plugins/datasetMixins.js";

export default {
    data: function() {
        return {};
    },
    components: { DonutChart, BarChart },
    props: ["check"],
    mixins: [datasetMixin],
    methods: {
        onePercent: function() {
            return (this.check.ok + this.check.failed + this.check.na) / 100;
        },
        detail: function(name) {
            this.$router.push({
                name: "datasetCheckDetail",
                params: { check: name }
            });
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.ok_icon {
    color: $ok_color;
}

.dataset_result_box {
    display: inline-block;
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 25px;
    min-height: 340px;
}

.chartEnvelope {
    position: relative;
    top: -50px;
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

.undef {
    background-color: #fafbff;
}

.undefined_title {
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
}

.undefined_image {
    margin-top: 20px;
}

.check_numeric_value {
    font-size: 60px;
    font-weight: 700;
}

.check_numeric_count {
    font-size: 30px;
    font-weight: 700;
}

.top3 > .table > tr:nth-child(1) > td {
    border-top: none;
}
</style>