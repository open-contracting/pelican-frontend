<template>
    <div
        class="card mb-4 h-100 time_variance_result_box result_box"
        :class="{ clickable: check.coverage_result != undefined, undef: check.coverage_result == undefined }"
        @click="detail(check.name)"
    >
        <div class="card-body">
            <div class="row no-gutters">
                <div class="col col-10 col-sm-10 col-lg-10">
                    <h5 class="check_headline">
                        {{ $t("timeLevel." + check.name + ".name") }}
                    </h5>
                </div>

                <div class="col col-2 col-sm-2 col-lg-2 text-right">
                    <span v-if="result == true" class="badge badge-pill ok_status">{{ $t("passed") }}</span>
                    <span v-if="result == false" class="badge badge-pill failed_status">{{ $t("failed") }}</span>
                </div>
            </div>

            <div class="row no-gutters">
                <div class="col col-12">
                    <p class="check_description" v-html="$t('timeLevel.' + check.name + '.description')" />
                </div>
            </div>
        </div>

        <div class="card-body">
            <div class="row no-gutters justify-content-end">
                <div class="col col-12">
                    <template v-if="check.coverage_result != null">
                        <div class="row">
                            <div class="col col-6 text-center">
                                <h6>{{ $t("timeLevel.coverageResult") }}</h6>
                            </div>
                            <div class="col col-6 text-center">
                                <h6>{{ $t("timeLevel.checkResult") }}</h6>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col col-6 text-center">
                                <span class="result_percentage" :class="{ color_failed: !check.coverage_result }">
                                    {{ coveragePercentage | formatPercentage }}
                                </span>
                            </div>
                            <div class="col col-6 text-center">
                                <span class="result_percentage" :class="{ color_failed: !check.check_result }">
                                    {{ checkPercentage | formatPercentage }}
                                </span>
                            </div>
                        </div>
                    </template>
                    <div v-else class="row">
                        <div class="col col-12 text-center">
                            <img class="undefined_image" src="/img/insufficient_data.png" />
                            <br />
                            <div class="undefined_title">
                                {{ $t("insufficientData.title") }}
                            </div>
                            <p v-html="$t('insufficientData.description')" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import timeMixins from "@/plugins/timeMixins.js";

export default {
    mixins: [timeMixins],
    props: ["check"],
    data: function () {
        return {};
    },
    computed: {
        result() {
            return this.check.coverage_result && this.check.check_result;
        }
    },
    methods: {
        detail: function (name) {
            this.$router.push({
                name: "timeVarianceCheckDetail",
                params: { check: name }
            });
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

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
}

.ok_icon {
    color: $ok_color;
}

.time_variance_result_box {
    background-color: white;
    padding: 5px;
    border-radius: 10px;
}

.time_variance_result_box h5 {
    font-size: 15px;
    margin-top: 3px;
}

.time_variance_result_box p {
    font-size: 13px;
}

.failed_icon {
    color: $failed_color;
}

.result_percentage {
    font-size: 40px;
}
</style>
