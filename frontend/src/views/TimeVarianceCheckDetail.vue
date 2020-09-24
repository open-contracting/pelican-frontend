<template>
    <dashboard-detail>
        <template v-if="check != null" v-slot:content>
            <h2>{{ $t("timeLevel." + check.name + ".name") }}</h2>
            <p v-html=" $t('timeLevel.' + check.name + '.descriptionLong')"></p>

            <h5>
                {{ $t("timeLevel.coverage.header") }}
                <span class="bold">{{ check.meta.total_count | formatNumber }}</span>
                &nbsp;
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
                {{ $t("timeLevel.check.header") }}
                <span class="bold">{{ check.meta.coverage_count | formatNumber }}</span>
                &nbsp;
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
                                <InlineBar :count="check.meta.ok_count" :percentage="check.check_value" :state="'ok'" :showCount="true" />
                            </td>
                        </tr>
                        <tr class="d-flex">
                            <td class="col-4 text-right label">
                                <span class="check_name">{{ $t("timeLevel.check.failed") }}</span>
                            </td>
                            <td class="col-8">
                                <InlineBar :count="check.meta.failed_count" :percentage="100 - check.check_value" :state="'failed'" :showCount="true" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="result_box" v-if="check.meta.examples && check.meta.examples.length > 0">
                <table class="table table-sm">
                    <thead>
                        <tr class="d-flex">
                            <th class="col-10" scope="col">{{ $t("ocid") }}</th>
                            <th class="col-2 text-left" scope="col">{{ $t("examples.actions") }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in check.meta.examples.slice(0, 5)" class="d-flex" v-bind:key="index">
                            <td class="col-9 text-left numeric d-flex align-items-center">
                                <span class="check_name">{{ item.ocid }}</span>
                            </td>
                            <td class="col-3 text-right numeric">
                                <span v-if="(index + 'new') != selectedKey">
                                    <a v-on:click.stop.prevent="preview(index + 'new', item.item_id)" href="#">{{ $t("examples.previewOld") }}</a>
                                </span>
                                <span v-else class="badge badge-primary">active</span>
                                <br />
                                <span v-if="(index + 'old') != selectedKey">
                                    <a v-on:click.stop.prevent="preview(index + 'old', item.new_item_id)" href="#">{{ $t("examples.previewNew") }}</a>
                                </span>
                                <span v-else class="badge badge-primary">active</span>
                            </td>
                        </tr>
                        <tr v-if="!showMore">
                            <td colspan="2" class="text-center bold clickable moreLess" v-on:click.stop="showMore = true">
                                <a>
                                    <font-awesome-icon icon="chevron-down" />
                                    {{ $t("examples.showMore") }}
                                </a>
                            </td>
                        </tr>
                        <span v-if="showMore">
                            <tr v-for="(item, index) in check.meta.examples.slice(0, 5)" class="d-flex" v-bind:key="index">
                                <td class="col-9 text-left numeric d-flex align-items-center">
                                    <span class="check_name">{{ item.ocid }}</span>
                                </td>
                                <td class="col-3 text-right numeric">
                                    <span v-if="(index + 5 + 'new') != selectedKey">
                                        <a v-on:click.stop.prevent="preview(index + 5 + 'new', item.item_id)" href="#">{{ $t("examples.previewOld") }}</a>
                                    </span>
                                    <span v-else class="badge badge-primary">active</span>
                                    <br />
                                    <span v-if="(index + 5 + 'old') != selectedKey">
                                        <a v-on:click.stop.prevent="preview(index + 5 + 'old', item.new_item_id)" href="#">{{ $t("examples.previewNew") }}</a>
                                    </span>
                                    <span v-else class="badge badge-primary">active</span>
                                </td>
                            </tr>
                        </span>
                        <tr v-if="showMore">
                            <td colspan="2" class="text-center bold clickable moreLess" v-on:click.stop="showMore = false">
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
                <h5>{{ $t("preview.ocdsData") }}</h5>
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
            examples: null,
            showMore: false,
            selectedKey: null
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
            this.previewMetadata = Object.assign({}, this.check.meta);
            delete this.previewMetadata.examples;
        }
    },
    methods: {
        preview: function(selectedKey, itemId) {
            this.selectedKey = selectedKey;
            this.$store.dispatch("loadDataItem", itemId);
            this.previewDataItemId = itemId;
        }
    },
    computed: {
        previewData() {
            var result = this.$store.getters.dataItemById(
                this.previewDataItemId
            );

            if (result) {
                return result["data"];
            }

            return null;
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