<template>
    <tr v-if="check" class="d-flex">
        <td class="col col-4">
            <slot>{{ check.path }}</slot>
        </td>

        <td class="col col-4">
            <div class="row no-gutters">
                <div class="col col-2 text-right coverage_result">{{ check.coverageOkShare | formatNumber }}%</div>
                <div
                    class="col col-6 numeric coverage_count text-right"
                >({{ check.coverage.passed_count | formatNumber }}/{{ check.coverage.total_count | formatNumber}})</div>
                <div class="col col-4 coverage_bar">
                    <ProgressBar :ok="check.coverageOkShare" />
                </div>
            </div>
        </td>

        <template v-if="check.quality.total_count">
            <td class="col col-2">
                <div class="row no-gutters">
                    <div class="col col-1 text-right">{{ check.qualityOkShare | formatNumber }}%</div>
                    <div class="col numeric text-right">({{ check.quality.passed_count | formatNumber }}/{{ check.quality.total_count | formatNumber }})</div>
                </div>
            </td>
            <td class="col col-2">
                <ProgressBar v-if="check.quality.total_count" :ok="check.qualityOkShare" />
            </td>
        </template>
        <td class="col col-4" colspan="1" v-else></td>
    </tr>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";

export default {
    data: function() {
        return {};
    },
    name: "field-check-table-row",
    props: ["check"],
    components: { ProgressBar }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

tbody tr {
    cursor: pointer;

    td {
        vertical-align: middle;
    }
}

.coverage_result {
    color: #4a4a4a;
    font-family: $font-family-bold;
    font-size: 16px;
    font-weight: 700;
    line-height: 19px;
}

.coverage_count {
    color: $na_light_color;
}

.coverage_bar {
    padding-right: 15px;
}
</style>