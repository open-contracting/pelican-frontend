<template>
    <dashboard>
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("field.title") }}</h2>
        <div class="description">
            <p>{{ $t('field.description[0]') }}</p>
            <p>{{ $t('field.description[1]') }}</p>
            <p>{{ $t('field.description[2]') }}</p>
        </div>

        <h4>{{ $t('field.all') }}</h4>
        <div class="result_box">
            <table class="table table-borderless">
                <thead>
                    <th>
                        <div class="d-flex align-items-center">
                            <div>{{ $t('field.table.head.object') }}</div>
                            <div class="sort_buttons">
                                <div :class="['asc', {active: sortedBy == 'name' && isAscendingSorted}]" @click.stop="sortByName()"></div>
                                <div :class="['desc', {active: sortedBy == 'name' && !isAscendingSorted}]" @click.stop="sortByName(false)"></div>
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
                <tbody>
                    <template v-for="n in tableData">
                        <tr :key="n.name">
                            <td rowspan="2">{{ n.name }}</td>
                            
                            <td class="percent">{{ n.coverageShare | formatNumber }}%</td>
                            <td class="ratio pr-0 text-right">({{ n.coverage.passed_count }}</td>
                            <td class="ratio px-0 text-center">&nbsp;/&nbsp;</td>
                            <td class="ratio pl-0 text-left">{{ n.coverage.total_count }})</td>

                            <td class="percent">{{ n.qualityShare | formatNumber }}%</td>
                            <td class="ratio pr-0 text-right">({{ n.quality.passed_count }}</td>
                            <td class="ratio px-0 text-center">&nbsp;/&nbsp;</td>
                            <td class="ratio pl-0 text-left">{{ n.quality.total_count }})</td>
                        </tr>
                        <tr :key="n.name + '-bar'" class="bar_row">
                            <td class="bar" colspan=4><ProgressBar :ok="n.coverageShare"/></td>
                            <td class="bar" colspan=4><ProgressBar :ok="n.qualityShare"/></td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import ProgressBar from "@/components/ProgressBar.vue";

export default {
    name: "field",
    data: function() {
        return {
            tableData: [],
            sortedBy: null,
            isAscendingSorted: null,
        }
    },
    components: { Dashboard, ProgressBar },
    computed: {
        stats: function() {
            return this.$store.getters.fieldLevelStats
        }
    },
    mounted: function() {
        var k
        for (k in this.stats) {
            this.tableData.push(Object.assign({}, this.stats[k], {
                name: k,
                coverageShare: this.okShare(this.stats[k].coverage),
                qualityShare: this.okShare(this.stats[k].quality)
            }))
        }

        this.sortByName()
    },
    methods: {
        okShare: function(item) {
            var result = item.passed_count / item.total_count * 100
            return isNaN(result) ? 0 : result
        },
        sort: function(comparator, asc = true) {
            this.tableData.sort(comparator)
            if (!asc) {
                this.tableData.reverse()
            }
        },
        sortByName: function(asc = true) {
            this.sortedBy = "name"
            this.isAscendingSorted =  asc
            this.sort((a, b) => a.name.localeCompare(b.name), asc)
        },
        sortByCoverage: function(asc = true) {
            this.sortedBy = "coverage"
            this.isAscendingSorted =  asc

            this.sort(function(a, b) {
                if (a.coverageShare < b.coverageShare) {
                    return -1
                } else if (a.coverageShare > b.coverageShare) {
                    return 1
                } else {
                    return 0
                }
            }, asc)
        },
        sortByQuality: function(asc = true) {
            this.sortedBy = "quality"
            this.isAscendingSorted =  asc
            
            this.sort(function(a, b) {
                if (a.qualityShare < b.qualityShare) {
                    return -1
                } else if (a.qualityShare > b.qualityShare) {
                    return 1
                } else {
                    return 0
                }
            }, asc)
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.description {
    color: $headings_light_color;
}

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

    tbody tr {
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
