<template>
    <table class="table table-borderless">
        <thead>
            <th>
                <div class="d-flex align-items-center">
                    <div>{{ $t('field.table.head.object') }}</div>
                    <div class="sort_buttons">
                        <div :class="['asc', {active: sortedBy == 'path' && isAscendingSorted}]" @click.stop="sortByPath()"></div>
                        <div :class="['desc', {active: sortedBy == 'path' && !isAscendingSorted}]" @click.stop="sortByPath(false)"></div>
                    </div>
                </div>
            </th>
            <th colspan="4" @click="sortByCoverage()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.coverage') }}</span>
                    <div class="sort_buttons">
                        <div :class="['asc', {active: sortedBy == 'coverage' && isAscendingSorted}]" @click.stop="sortByCoverage()"></div>
                        <div :class="['desc', {active: sortedBy == 'coverage' && !isAscendingSorted}]" @click.stop="sortByCoverage(false)"></div>
                    </div>
                </div>
            </th>
            <th colspan="4" @click="sortByQuality()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.quality') }}</span>
                    <div class="sort_buttons">
                        <div :class="['asc', {active: sortedBy == 'quality' && isAscendingSorted}]" @click.stop="sortByQuality()"></div>
                        <div :class="['desc', {active: sortedBy == 'quality' && !isAscendingSorted}]" @click.stop="sortByQuality(false)"></div>
                    </div>
                </div>
            </th>
        </thead>
        <tbody v-for="n in stats" :key="n.path">
            <tr @click="$emit('field-check-detail', n.path)">
                <td rowspan="2">{{ n.path }}</td>
                
                <td class="percent">{{ n.coverageOkShare | formatNumber }}%</td>
                <td class="ratio pr-0 text-right">({{ n.coverage.passed_count | formatNumber }}</td>
                <td class="ratio px-0 text-center">&nbsp;/&nbsp;</td>
                <td class="ratio pl-0 text-left">{{ n.coverage.total_count | formatNumber}})</td>

                <template v-if="n.quality.total_count">
                    <td class="percent">{{ n.qualityOkShare | formatNumber }}%</td>
                    <td class="ratio pr-0 text-right">({{ n.quality.passed_count | formatNumber }}</td>
                    <td class="ratio px-0 text-center">&nbsp;/&nbsp;</td>
                    <td class="ratio pl-0 text-left">{{ n.quality.total_count | formatNumber }})</td>
                </template>
                <td colspan="4" v-else></td>
            </tr>
            <tr class="bar_row">
                <td class="bar" colspan=4><ProgressBar :ok="n.coverageOkShare"/></td>                        
                <td class="bar" colspan=4><ProgressBar v-if="n.quality.total_count" :ok="n.qualityOkShare"/></td>                        
            </tr>
        </tbody>
    </table>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";
import fieldCheckMixins from "@/plugins/fieldCheckMixins.js";

export default {
    data: function() {
        return {
        };
    },
    props: ["stats"],
    components: { ProgressBar },
    mixins: [fieldCheckMixins],
    computed: {
        sortedBy: function() {
            var value = this.$store.getters.fieldCheckSortedBy
            return value == null ? this.defaultSorting.by : value
        },
        isAscendingSorted: function() {
            var value = this.$store.getters.fieldCheckSortedAscending
            return value == null ? this.defaultSorting.asc : value
        },
        defaultSorting: function() {
            return {by: "processingOrder", asc: true}
        }
    },
    mounted: function() {
        this.$on('field-check-table-sort', (data) => this.$store.commit('setFieldCheckSorting', data))

        this.sortBy(this.sortedBy, this.isAscendingSorted)
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.table {
    thead {
        th {            
            color: $headings_light_color;
            font-family: $headings-font-family;            

            .sort_buttons {
                margin-left: 10px;
         
                & > div {
                    width: 0; 
                    height: 0;
                    border-color: $headings_light_color;
                    cursor: pointer;
                }

                .asc {           
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;                    
                    border-bottom: 8px solid $headings_light_color;
                    margin-bottom: 4px;

                    &:hover, &.active {
                        border-bottom-color: $headings_color;
                    }
                }

                .desc {
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;                    
                    border-top: 8px solid $headings_light_color;

                    &:hover, &.active {
                        border-top-color: $headings_color;
                    }
                }
            }
        }
    }

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
}
</style>