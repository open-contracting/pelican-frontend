<template>
    <tbody>
        <tr>
            <td rowspan="2"><slot>{{ check.path }}</slot></td>
            
            <td class="percent">{{ check.coverageOkShare | formatNumber }}%</td>
            <td class="ratio pr-0 text-right">({{ check.coverage.passed_count | formatNumber }}</td>
            <td class="ratio px-0 text-center">&nbsp;/&nbsp;</td>
            <td class="ratio pl-0 text-left">{{ check.coverage.total_count | formatNumber}})</td>

            <template v-if="check.quality.total_count">
                <td class="percent">{{ check.qualityOkShare | formatNumber }}%</td>
                <td class="ratio pr-0 text-right">({{ check.quality.passed_count | formatNumber }}</td>
                <td class="ratio px-0 text-center">&nbsp;/&nbsp;</td>
                <td class="ratio pl-0 text-left">{{ check.quality.total_count | formatNumber }})</td>
            </template>
            <td colspan="4" v-else></td>
        </tr>
        <tr class="bar_row">
            <td class="bar" colspan=4><ProgressBar :ok="check.coverageOkShare"/></td>                        
            <td class="bar" colspan=4><ProgressBar v-if="check.quality.total_count" :ok="check.qualityOkShare"/></td>                        
        </tr>
    </tbody>    
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";

export default {
    data: function() {
        return {
        };
    },
    name: "field-check-table-row",
    props: ["check"],
    components: { ProgressBar }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

tbody:hover {
    background-color: rgba(0, 0, 0, 0.06);
}

tbody tr {
    cursor: pointer;

    &.bar_row td {
        border-bottom: 1px solid $na_light_color;
        padding-top: 0;
    }
    
    &:not(.bar_row) td:not(:first-of-type) {        
        padding-bottom: 0;
    }

    &:not(.bar_row) td:first-of-type {        
        border-bottom: 1px solid $na_light_color;
        width: 1px;
    }

    td {
        vertical-align: middle;

        &.percent {
            font-family: $headings-font-family;
            white-space: nowrap;
        }

        &.ratio {
            color: $na_color;
            font-family: $font-family-mono;
            white-space: nowrap;                
            text-align: right;

            &:not(:first-of-type) {
                width: 1px;
            }
        }
    }
}
</style>