<template>
    <dashboard v-if="dataset">
        <h2>{{ $t("sections.overview") }}</h2>
        <div class="row">
            <div class="col-12 col-xl-6">
                <h4>{{ $t('overview.collection_metadata') }}</h4>
                <div class="result_box collection_metadata col col-12">
                    <div class="table_hl" v-if="collection">
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">{{ $t('overview.compiled_releases.value_label') }}</div>
                            <div class="td col col-8 d-flex align-items-center break_word">
                                <span class="ocid_count bold">{{ compiled_releases.total_unique_ocids | formatNumber }}</span>
                            </div>
                        </div>
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">{{ $t('overview.publisher')}}</div>
                            <div class="td col col-8 d-flex align-items-center break_word">{{ collection.publisher }}</div>
                        </div>
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">URL</div>
                            <div class="td col col-8 d-flex align-items-center break_word">
                                <a v-if="collection.url && collection.url.startsWith('http')" :href="collection.url" target="_blank">{{ collection.url }}</a>
                                <template v-else>
                                    <template v-if="collection.url">{{ collection.url }}</template>
                                </template>
                            </div>
                        </div>
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">OCID Prefix</div>
                            <div class="td col col-8 d-flex align-items-center">{{ collection.ocid_prefix }}</div>
                        </div>
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">{{ $t('overview.datalicense')}}</div>
                            <div class="td col col-8 d-flex align-items-center break_word">
                                <a v-if="collection.data_license" :href="collection.data_license" target="_blank">{{ collection.data_license }}</a>
                            </div>
                        </div>
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">{{ $t('overview.extensions')}}</div>
                            <div v-if="collection.extensions" class="td col col-8">
                                <template v-for="(e, i) in collection.extensions">
                                    <span v-if="e.hasOwnProperty('name')" :key="i">
                                        <a
                                            v-if="e.hasOwnProperty('documentationUrl') && e.documentationUrl.hasOwnProperty('en') ? e.documentationUrl['en'] != '' : e.documentationUrl != ''"
                                            :href="e.documentationUrl.hasOwnProperty('en') ? e.documentationUrl['en'] : e.documentationUrl"
                                            :key="i"
                                            target="_blank"
                                        >{{ e.name.hasOwnProperty('en') ? e.name['en'] : e.name }}</a>
                                        <a
                                            v-else
                                            v-on:click="extensionPreview(e.name.hasOwnProperty('en') ? e.name['en'] : e.name)"
                                            :key="i"
                                            target="_blank"
                                        >{{ e.name.hasOwnProperty('en') ? e.name['en'] : e.name }}</a>
                                        <template v-if="i + 1 < collection.extensions.length">, </template>
                                    </span>
                                </template>
                            </div>
                        </div>
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">{{ $t('overview.publishedFrom')}}</div>
                            <div class="td col col-8 d-flex align-items-center">{{ collection.published_from }}</div>
                        </div>
                        <div class="tr row">
                            <div class="td col col-4 d-flex align-items-center">{{ $t('overview.publishedTo')}}</div>
                            <div class="td col col-8 d-flex align-items-center">{{ collection.published_to }}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12 col-xl-6">
                <div class="row">
                    <div class="col-12 col-md-6 col-xl-12">
                        <h4>{{ $t('overview.kingfisher_metadata') }}</h4>
                        <div class="result_box collection_metadata kingfisher_metadata">
                            <div class="table_hl" v-if="kingfisher">
                                <div class="tr row">
                                    <div class="td col col-6">{{ $t('overview.collectionId')}}</div>
                                    <div class="td col col-6">{{ kingfisher.collection_id }}</div>
                                </div>
                                <div class="tr row">
                                    <div class="td col col-6">{{ $t('overview.kingfisher_processingFrom')}}</div>
                                    <div class="td col col-6">{{ kingfisher.processing_start }}</div>
                                </div>
                                <div class="tr row">
                                    <div class="td col col-6">{{ $t('overview.kingfisher_processingTo')}}</div>
                                    <div class="td col col-6">{{ kingfisher.processing_end }}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 col-md-6 col-xl-12">
                        <h4>{{ $t('overview.dqt_metadata') }}</h4>
                        <div class="result_box collection_metadata kingfisher_metadata dqt_metadata">
                            <div v-if="data_quality" class="table_hl">
                                <div class="tr row">
                                    <div class="td col col-6">{{ $t('overview.processingFrom')}}</div>
                                    <div class="td col col-6">{{ data_quality.processing_start }}</div>
                                </div>
                                <div class="tr row">
                                    <div class="td col col-6">{{ $t('overview.processingTo')}}</div>
                                    <div class="td col col-6">{{ data_quality.processing_end }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col col-12 lifecycle">
                <h4>
                    {{ $t('overview.lifecycle.title') }}
                    <Tooltip :text="$t('overview.lifecycle.info')"></Tooltip>
                </h4>
                <div class="result_box">
                    <div class="row">
                        <template v-for="n in ['planning', 'tender', 'award', 'contract', 'implementation']">
                            <div class="col col-sm-2 col-md text-center lifecycle_phase" :key="n">
                                <div class="lifecycle_label">{{ $t("overview.lifecycle." + n) }}</div>
                                <div class="icon">
                                    <img class="lifecycle_icon" v-bind:src="'/img/icons/' + n + '_icon.png'" />
                                </div>
                                <div class="lifecycle_value">
                                    <strong>{{ lifecycle[n] | formatNumber }}</strong>
                                </div>
                            </div>
                            <div v-if="n != 'implementation'" class="lifecycle_arrow" :key="n + '-arrow'">
                                <font-awesome-icon icon="long-arrow-alt-right" />
                            </div>
                        </template>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12 col-md-6 prices">
                <h4>
                    {{ $t('overview.prices.title') }}
                    <Tooltip :text="$t('overview.prices.info')"></Tooltip>
                </h4>
                <div class="result_box">
                    <h5>{{ $t('overview.prices.value_label') }}</h5>
                    <p class="total_value">
                        <strong class="bold">$ {{ prices.total_volume_positive | formatNumber }}</strong>
                        in
                        <strong class="bold">{{ prices.contracts_positive | formatNumber }}</strong>
                        {{ $t('overview.prices.contracts') }}
                    </p>
                    <div class v-if="prices">
                        <div class="thr row">
                            <div class="th col col-4">{{ $t("overview.prices.thead.category") }}</div>
                            <div class="th col col-4 text-right">{{ $t("overview.prices.thead.count") }}</div>
                            <div class="th col col-4 text-center">{{ $t("overview.prices.thead.share") }}</div>
                        </div>
                        <div class="row tr" v-for="c in ['0_10000', '10001_100000', '100001_1000000', '1000001+']" :key="c">
                            <div class="td col col-4" v-html="getPriceCategoryLabel(c)" />
                            <div class="td col col-4 text-right numeric">{{ prices.price_category_positive[c].contracts | formatNumber }}</div>
                            <div class="td col col-4">
                                <div class="row align-items-center share_progressbar no-gutters">
                                    <div class="col col-3 value text-right">{{ (prices.price_category_positive[c].share * 100) | formatNumber }}%</div>
                                    <div class="col col-9 value progress_holder d-flex align-items-center">
                                        <progress-bar :value="(prices.price_category_positive[c].share * 100)" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-6 period">
                <h4>{{ $t('overview.period.title') }}</h4>
                <div class="result_box">
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
                </div>
            </div>
        </div>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import { GChart } from "vue-google-charts";
import Tooltip from "@/components/Tooltip.vue";

export default {
    name: "overview",
    components: { Dashboard, ProgressBar, GChart, Tooltip },
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
        },
        extensionPreview(extensionName) {
            this.$router.push({
                name: "extensionPreview",
                params: {
                    extensionName: extensionName,
                    datasetId: this.$store.getters.datasetId
                }
            });
        }
    }
};
</script>


<style lang="scss">
@import "src/scss/main";

.ocid_count {
    font-size: 24px;
}

.tr:first-of-type .td {
    border-top: none;
}

.total_value {
    font-size: 25px;
}

div.col.col-9.value.progress_holder {
    padding-left: 5px;
}

.compiled_releases {
    .value {
        font-size: 40px;
    }
}

.lifecycle_phase {
    margin-bottom: 20px;
}

.lifecycle_icon {
    width: 35px;
    margin-bottom: 10px;
    margin-top: 10px;
}

.lifecycle_arrow {
    padding-top: 40px;
}

.lifecycle_value {
    font-size: 20px;
    font-weight: 500;
    line-height: 24px;
    text-align: center;
}
</style>

