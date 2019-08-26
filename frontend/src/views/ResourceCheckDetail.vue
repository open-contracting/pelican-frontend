<template>
    <dashboard-detail>
        <template v-slot:content>
            <h3>{{ $t("header").toUpperCase() }}</h3>
            <h2>{{ $t("resourceLevel." + check.name + ".name") }}</h2>
            <p>{{ $t("resourceLevel." + check.name + ".description") }}</p>

            <h5>{{ $t("resourceLevel.count_header") }} {{ check.ok + check.failed + check.na | formatNumber }}</h5>
            <div class="result_box">
                <table class="table table-borderless table-sm">
                    <tbody>
                        <tr class="d-flex">
                            <td class="col-3 text-right">
                                <span class="check_name">{{ $t("passed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.ok" :percentage="okPercentage" :state="'ok'" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-3 text-right">
                                <span class="check_name">{{ $t("failed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.failed" :percentage="failedPercentage" :state="'failed'" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-3 text-right">
                                <span class="check_name">{{ $t("notAvailable") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.na" :percentage="naPercentage" :state="'na'" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h5>{{ $t("resourceLevel.application_count_header") }} {{ check.application_count | formatNumber }}</h5>
            <div class="result_box">
                <table class="table table-borderless table-sm">
                    <tbody>
                        <tr class="d-flex">
                            <td class="col-3 text-right">
                                <span class="check_name">{{ $t("passed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.pass_count" :percentage="passPercentage" :state="'ok'" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-3 text-right">
                                <span class="check_name">{{ $t("failed") }}</span>
                            </td>
                            <td class="col-9">
                                <InlineBar :count="check.application_count - check.pass_count" :percentage="nonpassPercentage" :state="'failed'" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h5>{{ $t("examples.failed") }}</h5>
            <div class="result_box">
                <table class="table table-sm">
                    <thead>
                        <tr class="d-flex">
                            <th class="col-10" scope="col">{{ $t("examples.ocid") }}</th>
                            <th class="col-2 text-left" scope="col">{{ $t("examples.actions") }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(example, index) in check.examples.failed" class="d-flex" v-bind:key="index">
                            <td class="col-10 text-left">
                                <span class="check_name">{{ example.data.ocid }}</span>
                            </td>
                            <td class="col-2 clickable" v-on:click="changePreview(index, 'failed', example.data, example.meta)">
                                <span v-if="index != selectedKey || selectedSection != 'failed'">{{ $t("examples.preview") }}</span>
                                <span class="badge badge-primary" v-if="index == selectedKey && selectedSection == 'failed'">active</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h5>{{ $t("examples.passed") }}</h5>
            <div class="result_box">
                <table class="table table-sm">
                    <thead>
                        <tr class="d-flex">
                            <th class="col-10" scope="col">{{ $t("examples.ocid") }}</th>
                            <th class="col-2 text-left" scope="col">{{ $t("examples.actions") }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(example, index) in check.examples.passed" class="d-flex" v-bind:key="index">
                            <td class="col-10 text-left">
                                <span class="check_name">{{ example.data.ocid }}</span>
                            </td>
                            <td class="col-2 clickable" v-on:click="changePreview(index, 'passed', example.data, example.meta)">
                                <span v-if="index != selectedKey || selectedSection != 'passed'">{{ $t("examples.preview") }}</span>
                                <span class="badge badge-primary" v-if="index == selectedKey && selectedSection == 'passed'">active</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
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
import InlineBar from "@/components/InlineBar";
import VueJsonPretty from "vue-json-pretty";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";

export default {
    name: "resourceCheckDetail",
    data: function() {
        return {
            check: null,
            previewData: null,
            previewMetadata: null,
            selectedKey: null,
            selectedSection: null
        };
    },
    components: { InlineBar, VueJsonPretty, DashboardDetail },
    created() {
        this.check = this.$store.getters.resourceLevelCheckByName(
            this.$route.params.check
        );
        if (this.check.examples.failed.length > 0) {
            this.previewMetadata = this.check.examples.failed[0].meta;
            this.previewData = this.check.examples.failed[0].data;
            this.selectedKey = 0;
            this.selectedSection = "failed";
        }
    },
    methods: {
        onePercent: function() {
            return (this.check.ok + this.check.failed + this.check.na) / 100;
        },
        changePreview: function(key, section, data, metaData) {
            this.selectedKey = key;
            this.selectedSection = section;
            this.previewMetadata = metaData;
            this.previewData = data;
        }
    },
    computed: {
        okPercentage() {
            return Math.round(this.check.ok / this.onePercent());
        },
        failedPercentage() {
            return Math.round(this.check.failed / this.onePercent());
        },
        naPercentage() {
            return Math.round(this.check.na / this.onePercent());
        },
        passPercentage() {
            return Math.round(
                this.check.pass_count / (this.check.application_count / 100)
            );
        },
        nonpassPercentage() {
            return Math.round(
                (this.check.application_count - this.check.pass_count) /
                    (this.check.application_count / 100)
            );
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";
</style>