<template>
    <div
        v-if="check"
        class="tr row clickable"
        v-on:click="detail()"
        @contextmenu.prevent="
            $root.$emit('navigationContextMenu', { event: $event, routerArguments: detailRouterArguments })
        "
    >
        <div class="td col col-4 break_word">
            <slot>{{ check.path }}</slot>
        </div>

        <div class="td col col-4">
            <div v-if="showStats" class="row h-100 no-gutters align-items-center">
                <div
                    class="col col-3 col-lg-2 col-xl-2 field_check_result d-flex align-items-center justify-content-end"
                >
                    <span class="field_check_result_value">{{ check.coverageOkShare | formatPercentage }}</span>
                </div>
                <div
                    class="col col-9 col-lg-7 col-xl-5 col-xxl-4 col-xxxxl-3 numeric field_check_count d-flex align-items-center justify-content-end"
                >
                    ({{ check.coverage.passed_count | formatNumber }}/{{ check.coverage.total_count | formatNumber }})
                </div>
                <div
                    class="col col-12 col-lg-3 col-xl-4 col-xxl-6 col-xxxxl-7 field_check_bar d-flex align-items-center justify-content-end"
                >
                    <span class="field_check_bar_envelope">
                        <ProgressBar :ok="check.coverageOkShare" />
                    </span>
                </div>
            </div>
        </div>

        <template v-if="check.quality.total_count">
            <div class="td col col-4">
                <div v-if="showStats" class="row h-100 no-gutters align-items-center">
                    <div
                        class="col col-3 col-lg-2 col-xl-2 field_check_result d-flex align-items-center justify-content-end"
                    >
                        <span class="field_check_result_value">{{ check.qualityOkShare | formatPercentage }}</span>
                    </div>
                    <div
                        class="col col-9 col-lg-7 col-xl-5 col-xxl-4 col-xxxxl-3 numeric field_check_count d-flex align-items-center justify-content-end"
                    >
                        ({{ check.quality.passed_count | formatNumber }}/{{
                            check.quality.total_count | formatNumber
                        }})
                    </div>
                    <div
                        class="col col-12 col-lg-3 col-xl-4 col-xxl-6 col-xxxxl-7 field_check_bar d-flex align-items-center justify-content-end"
                    >
                        <span class="field_check_bar_envelope">
                            <ProgressBar v-if="check.quality.total_count" :ok="check.qualityOkShare" />
                        </span>
                    </div>
                </div>
            </div>
        </template>
        <div class="td col col-4" v-else></div>
    </div>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";

export default {
    data: function () {
        return {
            detailRouterArguments: {
                name: "fieldCheckDetail",
                params: {
                    path: this.check.path,
                    datasetId: this.$store.getters.datasetId
                }
            }
        };
    },
    name: "field-check-table-row",
    props: {
        check: Object,
        showStats: {
            type: Boolean,
            default: true
        }
    },
    components: { ProgressBar },
    methods: {
        detail: function () {
            this.$router.push(this.detailRouterArguments);
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

tbody tr {
    cursor: pointer;
}

.field_check_result {
    color: #4a4a4a;
    font-family: $font-family-bold;
    font-size: 16px;
    font-weight: 700;
    line-height: 16px;
}

.field_check_result_value {
    position: relative;
    top: 1px;
}

.field_check_count {
    color: $na_color;
    font-size: 12px;
    align-items: center;
}

.field_check_bar_envelope {
    padding-left: 10px;
    width: 100%;
    position: relative;
    top: -1px;
}
</style>
