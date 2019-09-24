<template>
    <div class="result_box">
        <table class="table table-borderless table-sm">
            <tbody>
                <tr v-if="ok && 'passed_count' in check" class="d-flex">
                    <td class="col-3 text-right label">{{ $t("passed") }}</td>
                    <td class="col-9 align-middle">
                        <InlineBar :count="check.passed_count" :percentage="okPercentage" :state="'ok'" :showCount="true" />
                    </td>
                </tr>
                <tr v-if="failed && 'failed_count' in check" class="d-flex">
                    <td class="col-3 text-right label">{{ $t("failed") }}</td>
                    <td class="col-9 align-middle">
                        <InlineBar :count="check.failed_count" :percentage="failedPercentage" :state="'failed'" :showCount="true" />
                    </td>
                </tr>
                <tr v-if="na && 'undefined_count' in check" class="d-flex">
                    <td class="col-3 text-right label">{{ $t("notAvailable") }}</td>
                    <td class="col-9 align-middle">
                        <InlineBar :count="check.undefined_count" :percentage="naPercentage" :state="'na'" :showCount="true" />
                    </td>
                </tr>
                <tr v-if="pass && 'passed_count' in check" class="d-flex">
                    <td class="col-3 text-right label">{{ $t("passed") }}</td>
                    <td class="col-9 align-middle">
                        <InlineBar :count="check.passed_count" :percentage="passPercentage" :state="'ok'" :showCount="true" />
                    </td>
                </tr>
                <tr v-if="nonPass && 'failed_count' in check" class="d-flex">
                    <td class="col-3 text-right label">{{ $t("failed") }}</td>
                    <td class="col-9 align-middle">
                        <InlineBar :count="check.failed_count" :percentage="nonpassPercentage" :state="'failed'" :showCount="true" />
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import InlineBar from "@/components/InlineBar";
import ResourceCheckMixins from "@/plugins/resourceCheckMixins.js";

export default {
    props: {
        check: Object,
        ok: Boolean,
        failed: Boolean,
        na: Boolean,
        pass: Boolean,
        nonPass: Boolean
    },
    data: function() {
        return {};
    },
    mixins: [ResourceCheckMixins],
    components: { InlineBar }
};
</script>

<style scoped lang="scss">
.label {
    padding-top: 8px;
}
</style>