<template>
    <div class="card mb-4 time_variance_result_box result_box clickable" v-on:click="detail(check.name)">
        <div class="card-body">
            <div class="row no-gutters">
                <div class="col col-2 col-sm-2 col-lg-1 text-left">
                    <span v-if="result == true" class="result_icon ok_icon">
                        <font-awesome-icon :icon="['far', 'check-circle']" />
                    </span>
                    <span v-if="result == false" class="result_icon failed_icon">
                        <font-awesome-icon :icon="['far', 'times-circle']" />
                    </span>
                </div>

                <div class="col col-10 col-sm-10 col-lg-11">
                    <h5 class="check_headline">{{ $t("timeLevel." + check.name + ".name") }}</h5>
                    <p class="check_description" v-html="$t('timeLevel.' + check.name + '.description')"></p>
                </div>
            </div>
        </div>

        <div class="card-body">
            <div class="row no-gutters justify-content-end">
                <div class="col col-10 col-sm-10 col-lg-11">
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
                            <span class="result_percentage" v-bind:class="{ color_failed: !check.coverage_result }">{{ check.coverage_value }}</span> %
                        </div>
                        <div class="col col-6 text-center">
                            <span class="result_percentage" v-bind:class="{ color_failed: !check.check_result }">{{ check.check_value }}</span> %
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {};
    },
    props: ["check"],
    methods: {
        detail: function(name) {
            this.$router.push({
                name: "timeVarianceCheckDetail",
                params: { check: name }
            });
        }
    },
    computed: {
        result() {
            return this.check.coverage_result && this.check.check_result;
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.result_icon {
    font-size: 16px;
}

.card-body {
    padding: 15px;
}

.check_headline {
    overflow-wrap: break-word;
}

.check_description {
    overflow-wrap: break-word;
}

.ok_icon {
    color: $ok_color;
}

.time_variance_result_box {
    display: inline-block;
    background-color: white;
    padding: 0px;
    border-radius: 10px;
    margin-bottom: 25px;
    min-height: 340px;
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
    font-size: 50px;
}
</style>