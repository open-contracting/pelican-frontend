<template>
    <div
        class="tr row clickable align-items-center"
        v-on:click="detail()"
        @contextmenu.prevent="
            $root.$emit('navigationContextMenu', { event: $event, routerArguments: detailRouterArguments })
        "
    >
        <div class="col-9 col-lg-5 break_word check_name">
            <span>{{ $t("resourceLevel." + name + ".name") }}</span>
        </div>
        <div class="td col-1 col-lg-1 text-right">
            <span class="value_ok">{{ okPercentage | formatPercentage }}</span>
        </div>
        <div class="td col-1 col-lg-1 text-right">
            <span v-if="failedPercentage" class="value_failed">{{ failedPercentage | formatPercentageOmitZero }}</span>
            <span v-else class="value_na opacity">{{ failedPercentage | formatPercentageOmitZero }}</span>
        </div>
        <div class="td col-1 col-lg-1 text-right">
            <span class="value_na">{{ naPercentage | formatPercentage }}</span>
        </div>
        <div class="td col-4 d-none d-lg-block progress_column">
            <ProgressBar :ok="okPercentage" :failed="failedPercentage" />
        </div>
    </div>
</template>

<script>
import resourceCheckMixin from "@/plugins/resourceCheckMixins.js";
import ProgressBar from "@/components/ProgressBar.vue";

export default {
    data: function () {
        return {
            detailRouterArguments: {
                name: "resourceCheckDetail",
                params: {
                    check: this.name,
                    datasetId: this.$store.getters.datasetId
                }
            }
        };
    },
    mixins: [resourceCheckMixin],
    components: { ProgressBar },
    props: ["check", "name"],
    methods: {
        detail: function () {
            this.$router.push(this.detailRouterArguments);
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.check_name {
    padding-left: 65px;
}

.progress_column {
    padding-left: 40px;
}

.opacity {
    opacity: 0.6;
}
</style>
