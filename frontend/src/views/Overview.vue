<template>
    <dashboard>
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.overview") }}</h2>
        <div class="row">
            <div class="col-12 col-md-6">
                <overview-card :title="$t('overview.collection_metadata')" class="collection_metadata">
                    <table v-if="collection" class="table">
                        <tbody>
                            <tr><td>{{ $t('overview.publisher')}}</td><td>{{ collection.publisher }}</td></tr>
                            <tr><td>URL</td><td><a v-if="collection.url" :href="collection.url">{{ collection.url }}</a></td></tr>
                            <tr><td>OCID Prefix</td><td>{{ collection.ocid_prefix }}</td></tr>
                            <tr>
                                <td>{{ $t('overview.datalicense')}}</td>
                                <td><a v-if="collection.data_license" :href="collection.data_license">{{ collection.data_license }}</a></td>
                            </tr>
                            <tr>
                                <td>{{ $t('overview.extensions')}}</td>
                                <td>
                                    <template v-for="(e, i) in collection.extensions">
                                        {{ e.name }}<template v-if="i + 1 < collection.extensions.length">, </template>                                 
                                    </template>
                                </td>
                            </tr>
                            <tr><td>{{ $t('overview.publishedFrom')}}</td><td>{{ collection.published_from }}</td></tr>
                            <tr><td>{{ $t('overview.publishedTo')}}</td><td>{{ collection.published_to }}</td></tr>
                        </tbody>
                    </table>
                </overview-card>
            </div>
            <div class="col-12 col-md-6">
                <overview-card :title="$t('overview.kingfisher_metadata')" class="kingfisher_metadata">
                    <table v-if="kingfisher" class="table">
                        <tbody>
                            <tr><td>{{ $t('overview.collectionId')}}</td><td>{{ kingfisher.collection_id }}</td></tr>
                            <tr><td>{{ $t('overview.processingFrom')}}</td><td>{{ kingfisher.processing_start }}</td></tr>
                            <tr><td>{{ $t('overview.processingTo')}}</td><td>{{ kingfisher.processing_end }}</td></tr>
                        </tbody>
                    </table>
                </overview-card>
                <overview-card :title="$t('overview.dqt_metadata')" class="dqt_metadata">
                    <table v-if="data_quality" class="table">
                        <tbody>                            
                            <tr><td>{{ $t('overview.processingFrom')}}</td><td>{{ data_quality.processing_start }}</td></tr>
                            <tr><td>{{ $t('overview.processingTo')}}</td><td>{{ data_quality.processing_end }}</td></tr>
                        </tbody>
                    </table>
                </overview-card>
            </div>
        </div>
        <div class="row">
            <div class="col-auto">
                <overview-card :title="$t('overview.compiled_releases')" blank class="compiled_releases">
                    <h5>{{ $t('overview.compiled_releases_label') }}</h5>
                    {{ compiled_releases.total_unique_ocids }} 
                </overview-card>              
            </div>
            <div class="col">
                <overview-card :title="$t('overview.lifecycle')" blank class="lifecycle">
                    <div class="row">
                        <template v-for="n in ['planning', 'tender', 'award', 'contract', 'implementation']">                            
                            <div class="col" :key="n">
                                <div>{{ $t("overview.lifecycle_" + n) }}</div>
                                <div></div>
                                <div>{{ lifecycle[n] }}</div>
                            </div>
                            <div v-if="n != 'implementation'" class="col" :key="n + '-arrow'">
                                --------------->
                            </div>
                        </template>
                    </div>                    
                </overview-card>
            </div>
        </div>
        <div class="row">
            <div class="col-12 col-md-6">
                <overview-card :title="$t('overview.prices')">
                    <table v-if="prices">
                        <tbody>
                            
                        </tbody>
                    </table>
                </overview-card>               
            </div>
            <div class="col-12 col-md-6">
                <overview-card :title="$t('overview.period')">
                    <table v-if="period">
                        <tbody>
                            
                        </tbody>
                    </table>
                </overview-card>               
            </div>
        </div>
    </dashboard>    
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import OverviewCard from "@/components/OverviewCard.vue";

export default {
    name: "overview",
    components: { Dashboard, OverviewCard },
    computed: {
        dataset: function() {
            return this.$store.getters.dataset
        },
        collection: function() {
            return this.getMetaData('collection_metadata')
        },
        kingfisher: function() {
            return this.getMetaData('kingfisher_metadata')
        },
        data_quality: function() {
            return this.getMetaData('data_quality_tool_metadata')
        },
        compiled_releases: function() {
            return this.getMetaData('compiled_releases')
        },
        lifecycle: function() {
            return this.getMetaData('tender_lifecycle')
        },
        prices: function() {
            return this.getMetaData('prices')
        },
        period: function() {
            return this.getMetaData('period')
        }
    },
    methods: {
        getMetaData: function(type) {
            return this.dataset && this.dataset.meta ? this.dataset.meta[type] : null
        }
    }
};
</script>

<style lang="scss">
@import "src/scss/main";
.compiled_releases, .lifecycle {
    .result_box {
        padding: 0 !important;
    }
}

.collection_metadata, .kingfisher_metadata, .dqt_metadata {
    .table tr:first-of-type td {
        border-top: none;
    }

    .table tr td:first-of-type {
        font-weight: 200;
    }

    .table tr td:nth-of-type(2) {
        font-weight: 400;
    }
}
</style>

