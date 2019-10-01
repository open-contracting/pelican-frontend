<template>
    <dashboard-detail>
        <template v-if="check != null" v-slot:content>
            <h2>{{ $t("timeLevel." + check.name + ".name") }}</h2>
            <p v-html=" $t('timeLevel.' + check.name + '.descriptionLong')"></p>

            <h5>
                {{ $t("timeLevel.coverage.header") }} {{ check.meta.total_count | formatNumber }}
                <Tooltip :text="$t('timeLevel.coverage.header_tooltip')"></Tooltip>
            </h5>
            <div class="result_box">
                <table class="table table-borderless table-sm">
                    <tbody>
                        <tr class="d-flex">
                            <td class="col-4 text-right label">
                                <span class="check_name">{{ $t("timeLevel.coverage.ok") }}</span>
                            </td>
                            <td class="col-8">
                                <InlineBar :count="check.meta.coverage_count" :percentage="check.coverage_value" :state="'ok'" :showCount="true" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-4 text-right label">
                                <span class="check_name">{{ $t("timeLevel.coverage.failed") }}</span>
                            </td>
                            <td class="col-8">
                                <InlineBar
                                    :count="check.meta.total_count - check.meta.coverage_count"
                                    :percentage="100 - check.coverage_value"
                                    :state="'failed'"
                                    :showCount="true"
                                />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h5>
                {{ $t("timeLevel.check.header") }} {{ check.meta.coverage_count | formatNumber }}
                <Tooltip :text="$t('timeLevel.check.header_tooltip')"></Tooltip>
            </h5>
            <div class="result_box">
                <table class="table table-borderless table-sm">
                    <tbody>
                        <tr class="d-flex">
                            <td class="col-4 text-right label">
                                <span class="check_name">{{ $t("timeLevel.check.ok") }}</span>
                            </td>
                            <td class="col-8">
                                <InlineBar :count="check.meta.check_count" :percentage="check.check_value" :state="'ok'" :showCount="true" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-4 text-right label">
                                <span class="check_name">{{ $t("timeLevel.check.failed") }}</span>
                            </td>
                            <td class="col-8">
                                <InlineBar
                                    :count="check.meta.coverage_count - check.meta.check_count"
                                    :percentage="100 - check.check_value"
                                    :state="'failed'"
                                    :showCount="true"
                                />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="result_box" v-if="check.meta.examples">
                <table class="table table-sm">
                    <thead>
                        <tr class="d-flex">
                            <th class="col-6" scope="col">{{ $t("timeLevel.examples.oldItemOcid") }}</th>
                            <th class="col-6" scope="col">{{ $t("timeLevel.examples.newTiemOcid") }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in check.meta.examples.slice(0, 5)" class="d-flex" v-bind:key="index">
                            <td class="col-6 text-left numeric">
                                <span class="check_name">{{ item.ocid }}</span>
                                <br />
                                <span v-if="index != selectedKey || selectedSection != section[0]">{{ $t("examples.preview") }}</span>
                                <span class="badge badge-primary" v-if="index == selectedKey && selectedSection == section[0]">active</span>
                            </td>
                            <td class="col-6 text-left numeric">
                                <span class="check_name">{{ item.new_item_ocid }}</span>
                                <br />
                                <span v-if="index != selectedKey">{{ $t("examples.preview") }}</span>
                                <span class="badge badge-primary" v-if="index == selectedKey">active</span>
                            </td>
                        </tr>
                        <tr v-if="!showMore">
                            <td colspan="2" class="text-center bold clickable moreLess" v-on:click.stop="showMore(section[0])">
                                <a>
                                    <font-awesome-icon icon="chevron-down" />
                                    {{ $t("examples.showMore") }}
                                </a>
                            </td>
                        </tr>
                        <span v-if="showMore">
                            <tr v-for="(item, index) in check.meta.examples.slice.slice(5, )" class="d-flex" v-bind:key="index">
                                <td class="col-6 text-left numeric">
                                    <span class="check_name">{{ item.ocid }}</span>
                                    <br />
                                    <span v-if="index != selectedKey || selectedSection != section[0]">{{ $t("examples.preview") }}</span>
                                    <span class="badge badge-primary" v-if="index == selectedKey && selectedSection == section[0]">active</span>
                                </td>
                                <td class="col-6 text-left numeric">
                                    <span class="check_name">{{ item.new_item_ocid }}</span>
                                    <br />
                                    <span v-if="index != selectedKey">{{ $t("examples.preview") }}</span>
                                    <span class="badge badge-primary" v-if="index == selectedKey">active</span>
                                </td>
                            </tr>
                        </span>
                        <tr v-if="showMore">
                            <td colspan="2" class="text-center bold clickable moreLess" v-on:click.stop="showLess(section[0])">
                                <a>
                                    <font-awesome-icon icon="chevron-up" />
                                    {{ $t("examples.showLess") }}
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </template>

        <template v-slot:preview>
            <h5>{{ $t("preview.metadata") }}</h5>
            <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewMetadata"></vue-json-pretty>

            <div class="divider">&nbsp;</div>
            <span v-if="previewData">
                <h5>{{ $t("preview.ocds_data") }}</h5>
                <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="previewData"></vue-json-pretty>
            </span>
        </template>
    </dashboard-detail>
</template>

<script>
import InlineBar from "@/components/InlineBar";
import VueJsonPretty from "vue-json-pretty";
import DashboardDetail from "@/views/layouts/DashboardDetail.vue";
import Tooltip from "@/components/Tooltip.vue";

export default {
    name: "timeVarianceCheckDetail",
    data: function() {
        return {
            check: null,
            previewDataItemId: null,
            previewMetadata: null,
            examples: null
        };
    },
    components: {
        VueJsonPretty,
        DashboardDetail,
        InlineBar,
        Tooltip
    },
    created() {
        this.check = this.$store.getters.timeVarianceLevelCheckByName(
            this.$route.params.check
        );

        if (this.check != null) {
            this.previewMetadata = this.check.meta;
        }
    },
    methods: {
        preview: function(itemId) {
            this.$store.dispatch("loadDataItem", itemId);
            this.previewDataItemId = itemId;
        }
    },
    computed: {
        previewData() {
            return this.$store.getters.dataItemById(this.previewDataItemId);
        },
        coverageState() {
            return this.check.coverage_result ? "ok" : "failed";
        },
        checkState() {
            return this.check.check_result ? "ok" : "failed";
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";
</style>