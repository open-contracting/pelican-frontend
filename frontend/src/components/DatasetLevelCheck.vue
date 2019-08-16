<template>
    <div class="dataset_result_box">
        <div class="row no-gutters">
            <div class="col col-1 col-sm-1 col-lg-1">
                <span v-if="check.result" class="ok_icon">
                    <font-awesome-icon :icon="['far', 'check-circle']" />
                </span>
                <span v-else class="failed_icon">
                    <font-awesome-icon :icon="['far', 'times-circle']" />
                </span>
            </div>

            <div class="col col-10 col-sm-11 col-lg-11">
                <h5>{{ checkType }} {{ $t("datasetLevel." + check.name + ".name") }}</h5>
                <p>
                    {{ $t("datasetLevel." + check.name + ".description") }}
                </p>
                <div v-if="checkType == 'donut'">
                    <DonutChart :check="check"></DonutChart>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DonutChart from "@/components/DonutChart.vue";

export default {
    data: function() {
        return {};
    },
    components: {DonutChart},
    props: ["check"],
    methods: {},
    computed: {
        checkType() {
            var donut = [
                "distribution.main_procurement_category",
                "distribution.tender_status"
            ]
            if (donut.includes(this.check.name)) {
                return "donut";
            }
            return null;
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
    background-color: white;
    padding: 10px;
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
</style>