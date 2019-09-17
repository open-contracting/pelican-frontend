<template>
    <tr class="d-flex clickable" v-on:click="detail()">
        <td class="col-5">
            <span class="check_name">{{ $t("resourceLevel." + name + ".name") }}</span>
        </td>
        <td class="col-1 text-right">
            <span v-if=" okPercentage> 0" class="value_ok">{{ okPercentage }}%</span>
        </td>
        <td class="col-1 text-right">
            <span v-if=" failedPercentage> 0" class="value_failed">{{ failedPercentage }}%</span>
        </td>
        <td class="col-1 text-right">
            <span v-if=" naPercentage> 0" class="value_na">{{ naPercentage }}%</span>
        </td>
        <td class="col-1 text-right"></td>
        <td class="col-3">
            <ProgressBar :ok="okPercentage" :failed="failedPercentage" />
        </td>
    </tr>
</template>

<script>

import resourceCheckMixin from "@/plugins/resourceCheckMixins.js";
import ProgressBar from "@/components/ProgressBar.vue";

export default {
    data: function() {
        return {};
    },
    mixins: [resourceCheckMixin],
    components: { ProgressBar },
    props: ["check", "name"],
    methods: {
        detail: function() {
            this.$router.push({
                name: "resourceCheckDetail",
                params: { check: this.name }
            });
        }
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.check_name {
    padding-left: 35px;
}
</style>