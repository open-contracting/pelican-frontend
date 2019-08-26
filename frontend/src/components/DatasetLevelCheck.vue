<template>
    <div class="dataset_result_box" v-bind:class="{ clickable: check.result != undefined }" v-on:click="detail(check.name)">
        <div class="row no-gutters">
            <div class="col col-1 col-sm-1 col-lg-1">
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

            <div class="col col-10 col-sm-11 col-lg-11">
                <h5 v-bind:class="{ undef: check.result == undefined }">{{ $t("datasetLevel." + check.name + ".name") }}</h5>
                <p v-bind:class="{ undef: check.result == undefined }">{{ $t("datasetLevel." + check.name + ".description") }}</p>

                <div class="text-center undef undef_message alert alert-light" v-if="check.result == undefined">
                    <font-awesome-icon :icon="['far', 'frown']" />
                    {{ $t("unsufficientData") }}
                </div>
                <div v-else>
                    <div v-if="checkType == 'donut'">
                        <DonutChart :check="check"></DonutChart>
                    </div>

                    <div v-if="checkType == 'bar'">
                        <BarChart :check="check"></BarChart>
                    </div>

                    <div v-if="checkType == 'numeric'" class="text-center">
                        <span class="check_numeric_value">{{ check.value }}</span>
                        <span class="check_numeric_count">&nbsp;/&nbsp;{{ check.meta.count }}100</span>
                    </div>

                    <div class="top3" v-if="checkType == 'top3'">
                        <table class="table table-sm">
                            <tr v-for="(item, index) in check.meta.most_frequent" v-bind:key="index">
                                <td>{{ item.amount }}</td>
                                <td class="text-right">{{ Math.round(item.share)}}%</td>
                            </tr>
                        </table>
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

.undefined_icon {
    color: $na_light_color;
}

.undef {
    color: $na_light_color;
}

.undef_message {
    font-size: 25px;
}

.dataset_result_box {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 25px;
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

.top3 > .table > tr:nth-child(1) > td {
    border-top: none;
}
</style>