<template>
    <table class="table table-borderless">
        <thead>
            <th>
                <div class="d-flex align-items-center">
                    <div>{{ $t('field.table.head.object') }}</div>
                    <div class="sort_buttons">
                        <div :class="['asc', {active: sortedBy == 'path' && isAscendingSorted}]" @click.stop="sortByPath(tableData)"></div>
                        <div :class="['desc', {active: sortedBy == 'path' && !isAscendingSorted}]" @click.stop="sortByPath(tableData, false)"></div>
                    </div>
                </div>
            </th>
            <th colspan="4" @click="sortByCoverage()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.coverage') }}</span>
                    <div class="sort_buttons">
                        <div :class="['asc', {active: sortedBy == 'coverage' && isAscendingSorted}]" @click.stop="sortByCoverage(tableData)"></div>
                        <div :class="['desc', {active: sortedBy == 'coverage' && !isAscendingSorted}]" @click.stop="sortByCoverage(tableData, false)"></div>
                    </div>
                </div>
            </th>
            <th colspan="4" @click="sortByQuality()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.quality') }}</span>
                    <div class="sort_buttons">
                        <div :class="['asc', {active: sortedBy == 'quality' && isAscendingSorted}]" @click.stop="sortByQuality(tableData)"></div>
                        <div :class="['desc', {active: sortedBy == 'quality' && !isAscendingSorted}]" @click.stop="sortByQuality(tableData, false)"></div>
                    </div>
                </div>
            </th>
        </thead>
        
        <template v-for="n in tableData">
            <FieldCheckTableRow v-if="isSearched(n)" :key="n.path" :check="n" @click.native="$emit('field-check-detail', n.path)">
                <span v-html="highlightSearch(n.path)" />
                <template v-if="hasHidden(n)">
                    <div class="hide_button">
                        <i>{{ $t('field.hidden', { n: n._hidden.length }) }}</i>
                        <button @click.stop="switchHidden(n)" :class="['btn', {disabled: isHidden(n)}]">
                            <font-awesome-icon icon="eye-slash" />
                        </button>
                    </div>
                </template>
            </FieldCheckTableRow>
            <template v-for="h in n._hidden">
                <FieldCheckTableRow v-if="isSearched(h)" :check="h" :key="h.path" :class="['hidden', {'d-none': isHidden(n)}]"
                    @click.native="$emit('field-check-detail', h.path)">
                    <span v-html="highlightSearch(h.path)" />
                </FieldCheckTableRow>
            </template>
        </template>
    </table>
</template>

<script>
import fieldCheckMixins from "@/plugins/fieldCheckMixins.js";
import FieldCheckTableRow from "@/components/FieldCheckTableRow.vue";

export default {
    data: function() {
        return {
            showHidden: {}
        };
    },
    components: { FieldCheckTableRow },
    mixins: [ fieldCheckMixins ],
    computed: {
        stats: function() {
            return this.$store.getters.fieldLevelStats
        },
        tableData: function() {
            if (!this.stats) {
                return []
            }
            var data = []
            var lastWithHidden = null

            this.sortBy(this.stats, "path")

            this.stats.forEach(n => {
                if (n.coverage.total_count) {
                    data.push(n)
                    
                    if (!n.coverage.passed_count) {
                        lastWithHidden = n
                        lastWithHidden["_hidden"] = []
                    }
                } else {
                    lastWithHidden["_hidden"].push(n)
                }
            })

            return data
        },
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

        this.sortBy(this.tableData, this.sortedBy, this.isAscendingSorted)
    },
    methods: {
        hasHidden: function(check) {
            return "_hidden" in check && check._hidden.length > 0
        },
        switchHidden: function(check) {
            var patch = {}
            patch[check.path] = !this.showHidden[check.path]
            this.showHidden = Object.assign({}, this.showHidden, patch)
        },
        isHidden: function(check) {
            return !this.showHidden[check.path]
        },
        resetSorting: function() {
            this.sortByProcessingOrder(this.tableData)
        },
        isSearched: function(check) {
            return !this.search || (check && this.isPathSearched(check.path))
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.table {   
    tbody {
        &.hidden {
            color: $na_color;
        }

        .hide_button {
            font-size: 14px;
            font-family: $font-family-thin;
            white-space: nowrap;
        }
    }

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
}
</style>