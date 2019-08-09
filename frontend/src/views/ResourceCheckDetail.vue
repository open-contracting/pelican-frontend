<template>
    <div class="resource_level_check_detail">
        <div class="row">
            <div class="col col-6">
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
            </div>
        </div>
    </div>
</template>

<script>
import InlineBar from "@/components/InlineBar";

export default {
    name: "resourceCheckDetail",
    data: function() {
        return {
            check: null
        };
    },
    components: { InlineBar },
    created() {
        this.check = this.$store.getters.resourceLevelCheckByName(
            this.$route.params.check
        );
    },
    methods: {
        onePercent: function() {
            return (this.check.ok + this.check.failed + this.check.na) / 100;
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
