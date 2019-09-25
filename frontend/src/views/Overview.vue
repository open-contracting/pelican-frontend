<template>
    <dashboard>
        <h2>{{ $t("sections.overview") }}</h2>
        <div class="row">
            <div class="col-12 col-md-6">
                <overview-card :title="$t('overview.collection_metadata')" class="collection_metadata">
                    <table v-if="collection" class="table">
                        <tbody>
                            <tr>
                                <td>{{ $t('overview.publisher')}}</td>
                                <td>{{ collection.publisher }}</td>
                            </tr>
                            <tr>
                                <td>URL</td>
                                <td>
                                    <a v-if="collection.url" :href="collection.url" target="_blank">{{ collection.url }}</a>
                                </td>
                            </tr>
                            <tr>
                                <td>OCID Prefix</td>
                                <td>{{ collection.ocid_prefix }}</td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.datalicense')}}</td>
                                <td>
                                    <a v-if="collection.data_license" :href="collection.data_license" target="_blank">{{ collection.data_license }}</a>
                                </td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.extensions')}}</td>
                                <td>
                                    <template v-for="(e, i) in collection.extensions">
                                        <a
                                            v-if="e.documentationUrl"
                                            :href="e.documentationUrl.hasOwnProperty('en') ? e.documentationUrl['en'] : e.documentationUrl"
                                            :key="e.name.hasOwnProperty('en') ? e.name['en'] : e.name"
                                            target="_blank"
                                        >{{ e.name.hasOwnProperty('en') ? e.name['en'] : e.name }}</a>
                                        <template v-else>{{ e.name.hasOwnProperty('en') ? e.name['en'] : e.name }}</template>

                                        <template v-if="i + 1 < collection.extensions.length">,</template>
                                    </template>
                                </td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.publishedFrom')}}</td>
                                <td>{{ collection.published_from }}</td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.publishedTo')}}</td>
                                <td>{{ collection.published_to }}</td>
                            </tr>
                        </tbody>
                    </table>
                </overview-card>
            </div>
            <div class="col-12 col-md-6">
                <overview-card :title="$t('overview.kingfisher_metadata')" class="kingfisher_metadata">
                    <table v-if="kingfisher" class="table">
                        <tbody>
                            <tr>
                                <td>{{ $t('overview.collectionId')}}</td>
                                <td>{{ kingfisher.collection_id }}</td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.processingFrom')}}</td>
                                <td>{{ kingfisher.processing_start }}</td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.processingTo')}}</td>
                                <td>{{ kingfisher.processing_end }}</td>
                            </tr>
                        </tbody>
                    </table>
                </overview-card>
                <overview-card :title="$t('overview.dqt_metadata')" class="dqt_metadata">
                    <table v-if="data_quality" class="table">
                        <tbody>
                            <tr>
                                <td>{{ $t('overview.processingFrom')}}</td>
                                <td>{{ data_quality.processing_start }}</td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.processingTo')}}</td>
                                <td>{{ data_quality.processing_end }}</td>
                            </tr>
                        </tbody>
                    </table>
                </overview-card>
            </div>
        </div>
        <div class="row">
            <div class="col-auto">
                <overview-card v-if="compiled_releases" :title="$t('overview.compiled_releases.title')" blank class="compiled_releases">
                    <template>
                        <h5 class="text-nowrap">{{ $t('overview.compiled_releases.value_label') }}</h5>
                        <div class="value">
                            <strong>{{ compiled_releases.total_unique_ocids | formatNumber }}</strong>
                        </div>
                    </template>
                </overview-card>
            </div>
            <div class="col">
                <overview-card v-if="lifecycle" blank class="lifecycle" :title="$t('overview.lifecycle.title')" :info="$t('overview.lifecycle.info')">
                    <div class="row">
                        <template v-for="n in ['planning', 'tender', 'award', 'contract', 'implementation']">
                            <div class="col mx-auto text-center" :key="n">
                                <div class="label">{{ $t("overview.lifecycle." + n) }}</div>
                                <div class="icon mx-auto"></div>
                                <div class="value">
                                    <strong>{{ lifecycle[n] | formatNumber }}</strong>
                                </div>
                            </div>
                            <div v-if="n != 'implementation'" class="col align-self-center" :key="n + '-arrow'">---------------></div>
                        </template>
                    </div>
                </overview-card>
            </div>
        </div>
        <div class="row">
            <div class="col-12 col-md-6">
                <overview-card v-if="prices" :title="$t('overview.prices.title')" :info="$t('overview.prices.info')" class="prices">
                    <h5>{{ $t('overview.prices.value_label') }}</h5>
                    <p>
                        <strong>$ {{ prices.total_volume_positive | formatNumber }}</strong>
                        in {{ prices.contracts_positive | formatNumber }} {{ $t('overview.prices.contracts') }}
                    </p>
                    <table v-if="prices" class="table">
                        <thead>
                            <tr>
                                <th>{{ $t("overview.prices.thead.category") }}</th>
                                <th class="text-right">{{ $t("overview.prices.thead.count") }}</th>
                                <th>{{ $t("overview.prices.thead.share") }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="c in ['0_10000', '10001_100000', '100001_1000000', '1000001+']" :key="c">
                                <td v-html="getPriceCategoryLabel(c)" />
                                <td class="text-right">{{ prices.price_category_positive[c].contracts | formatNumber }}</td>
                                <td>
                                    <div class="d-flex flex-row align-items-center share_progressbar">
                                        <div class="value">{{ (prices.price_category_positive[c].share * 100) | formatNumber }}%</div>
                                        <progress-bar :value="(prices.price_category_positive[c].share * 100)" class="flex-fill" />
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </overview-card>
            </div>
            <div class="col-12 col-md-6">
                <overview-card v-if="period" :title="$t('overview.period.title')" class="period">
                    <h5>{{ $t('overview.period.subtitle') }}</h5>
                    <p>{{ $t('overview.period.description') }}</p>
                    <div>
                        <GChart
                            type="ColumnChart"
                            :data="period_histogram"
                            :options="{
                                legend: 'none',
                                bar: {groupWidth: '95%'},
                                colors: ['#6C75E1'],
                                hAxis: {
                                    baselineColor: 'transparent',
                                    gridlines: {
                                        color: 'transparent'
                                    },
                                    showTextEvery: parseInt(period_histogram.length / 2.1),
                                    slantedText: false
                                },
                                vAxis: {
                                    baselineColor: 'transparent',
                                    gridlines: {
                                        color: 'transparent'
                                    }
                                }
                            }"
                        />
                    </div>
                </overview-card>
            </div>
        </div>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import OverviewCard from "@/components/OverviewCard.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import { GChart } from "vue-google-charts";

export default {
    name: "overview",
    components: { Dashboard, OverviewCard, ProgressBar, GChart },
    computed: {
        dataset: function() {
            return this.$store.getters.dataset;
        },
        collection: function() {
            return this.getMetaData("collection_metadata");
        },
        kingfisher: function() {
            return this.getMetaData("kingfisher_metadata");
        },
        data_quality: function() {
            return this.getMetaData("data_quality_tool_metadata");
        },
        compiled_releases: function() {
            return this.getMetaData("compiled_releases");
        },
        lifecycle: function() {
            return this.getMetaData("tender_lifecycle");
        },
        prices: function() {
            return this.getMetaData("prices");
        },
        period: function() {
            return this.getMetaData("period");
        },
        period_histogram: function() {
            var hist = [["date", "count"]];
            if (this.period) {
                this.period.forEach(function(p) {
                    hist.push([p.date_str, p.count]);
                });
            }
            return hist;
        }
    },
    methods: {
        getMetaData: function(type) {
            return this.dataset && this.dataset.meta
                ? this.dataset.meta[type]
                : null;
        },
        getPriceCategoryLabel(categoryId) {
            if (categoryId == "0_10000") {
                return (
                    "$" +
                    this.formatNumber(0) +
                    " - $" +
                    this.formatNumber(10000)
                );
            } else if (categoryId == "10001_100000") {
                return (
                    "$" +
                    this.formatNumber(10001) +
                    " - $" +
                    this.formatNumber(100000)
                );
            } else if (categoryId == "100001_1000000") {
                return (
                    "$" +
                    this.formatNumber(100001) +
                    " - $" +
                    this.formatNumber(1000000)
                );
            } else if (categoryId == "1000001+") {
                return "$" + this.formatNumber(1000001) + "+";
            }

            return categoryId;
        },
        formatNumber(number) {
            return this.$options.filters.formatNumber(number);
        }
    }
};
</script>


<style lang="scss">
@import "src/scss/main";
.overview_card * {
    color: $text-color;
}
.compiled_releases,
.lifecycle {
    .result_box {
        padding: 0 !important;
    }

    .row > div {
        margin: 0 !important;
    }
}

.collection_metadata,
.kingfisher_metadata,
.dqt_metadata {
    .table tr:first-of-type td {
        border-top: none;
    }

    .table tbody tr {
        td {
            vertical-align: middle;
        }

        td:first-of-type {
            font-weight: 200;
            color: $headings_light_color;
            white-space: nowrap;
            font-family: $font-family-thin;
        }

        td:nth-of-type(2) {
            font-weight: 400;
        }

        a {
            color: $text-color;
            text-decoration: underline;
        }

        a:hover {
            text-decoration: none;
        }
    }

    .table tbody tr a:hover {
        text-decoration: none;
    }
}

.prices {
    .table thead {
        th {
            border-bottom: none;
            color: $headings_light_color;
            font-size: 12px;
        }
    }

    .table tr:first-of-type td {
        border-top: none;
    }

    .share_progressbar {
        .value {
            margin-right: 10px;
            color: $headings_light_color;
        }
    }

    h5 + p {
        font-size: 25px !important;
    }
}

.period {
    p {
        color: $headings_light_color;
    }
}

.lifecycle {
    .icon {
        height: 40px;
        width: 40px;
        background-color: $ok_color;
        border-radius: 20px;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    h4 {
        margin-bottom: 20px;
        margin-top: 20px;
    }

    .value {
        font-size: 20px;
    }

    .row {
        .col:first-of-type {
            padding-left: 0;
        }
    }
}

.compiled_releases {
    .value {
        font-size: 40px;
    }
}
</style>

