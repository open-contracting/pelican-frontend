<template>
    <dashboard-detail>
        <template v-slot:content>
            <h3>{{ $t("header").toUpperCase() }}</h3>
            <div class="row">
                <div class="col col-10">
                    <h2>{{ $t("datasetLevel." + check.name + ".name") }}</h2>
                </div>
                <div class="col col-2">
                    <span v-if="check.result == true" class="badge badge-pill ok_status">{{ $t("passed") }}</span>
                    <span v-if="check.result == false" class="badge badge-pill failed_status">{{ $t("failed") }}</span>
                </div>
            </div>
            <p>{{ $t("datasetLevel." + check.name + ".description") }}</p>

            <div class="result_box">
                <div v-if="checkType == 'bar'">
                    <BarChartBig :check="check"></BarChartBig>
                </div>
            </div>
        </template>

        <template v-slot:preview>
            <h5>{{ $t("preview.metadata") }}</h5>
            <vue-json-pretty :highlightMouseoverNode="'True'" :data="previewMetadata"></vue-json-pretty>

            <div class="divider">&nbsp;</div>

            <h5>{{ $t("preview.ocds_data") }}</h5>
            <vue-json-pretty :highlightMouseoverNode="'True'" :deep="2" :data="previewData"></vue-json-pretty>
        </template>
    </dashboard-detail>
</template>

<script>
import BarChartBig from "@/components/BarChartBig";
import VueJsonPretty from "vue-json-pretty";
import datasetMixin from "@/plugins/datasetMixins.js";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";

export default {
    name: "datasetCheckDetail",
    mixins: [datasetMixin],
    data: function() {
        return {
            check: null,
            previewData: null,
            previewMetadata: null,
            selectedKey: null,
            selectedSection: null
        };
    },
    components: { BarChartBig, VueJsonPretty, DashboardDetail },
    created() {
        this.check = this.$store.getters.datasetLevelCheckByName(
            this.$route.params.check
        );
    },
    methods: {},
    computed: {}
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.ok_status {
    background-color: $ok_color;
    color: white;
    font-size: 15px;
    padding: 10px;
}

.failed_status {
    background-color: $failed_color;
    color: white;
    font-size: 15px;
    padding: 10px;
}
</style>