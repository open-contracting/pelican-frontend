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
            <table class="table">
                <thead>
                    <th>{{ $t('field.table.head.object') }}</th>
                    <th>{{ $t('field.table.head.coverage') }}</th>
                    <th>{{ $t('field.table.head.quality') }}</th>
                </thead>
                <tbody>
                    <tr v-for="(v, k) in stats" :key="k">
                        <td>{{ $t("field.table.object." + k) }}</td>
                        <td>
                            <div class="d-flex flex-row align-items-center">
                                <span>{{ okShare(v.coverage) | formatNumber }}% ({{ v.coverage.passed_count }} / {{ v.coverage.total_count }})</span>
                                <ProgressBar :ok="okShare(v.coverage)"/>
                            </div>
                        </td>
                        <td>
                            <div class="d-flex flex-row align-items-center">
                                <span>{{ okShare(v.quality) | formatNumber }}% ({{ v.quality.passed_count }} / {{ v.quality.total_count }})</span>
                                <ProgressBar :ok="okShare(v.quality)"/>
                            </div>
                        </td>
                    </tr>
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
    components: { Dashboard, ProgressBar },
    computed: {
        stats: function() {
            return this.$store.getters.fieldLevelStats
        }
    },
    methods: {
        okShare: function(item) {
            return item.passed_count / item.total_count * 100
        }        
    }
};
</script>

<style lang="scss">
@import "src/scss/main";

.description {
    color: $headings_light_color;
}

.table tr:first-of-type td {
    border-top: none;
}

.table {
    thead {
        th {
            border-bottom: none !important;
            color: $headings_light_color;
            font-family: $headings-font-family;
        }
    }
    tbody tr {
        td {
            vertical-align: middle;
        }
    }
}
</style>
