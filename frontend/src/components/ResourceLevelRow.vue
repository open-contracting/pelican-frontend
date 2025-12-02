<template>
  <div
    class="tr row clickable align-items-center"
    @click="detail()"
  >
    <div class="col-9 col-lg-5 break_word check_name">
      <span>{{ $t("resourceLevel." + name + ".name") }}</span>
    </div>
    <div class="td col-1 col-lg-1 text-right">
      <span
        v-if="okPercentage"
        class="value_ok"
      >{{ $filters.formatPercentage(okPercentage) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ $filters.formatPercentage(okPercentage) }}</span>
    </div>
    <div class="td col-1 col-lg-1 text-right">
      <span
        v-if="failedPercentage"
        class="value_failed"
      >{{ $filters.formatPercentage(failedPercentage) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ $filters.formatPercentage(failedPercentage) }}</span>
    </div>
    <div class="td col-1 col-lg-1 text-right">
      <span
        v-if="naPercentage"
        class="value_na"
      >{{ $filters.formatPercentage(naPercentage) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ $filters.formatPercentage(naPercentage) }}</span>
    </div>
    <div class="td col-4 d-none d-lg-block progress_column">
      <ProgressBar
        :ok="okPercentage"
        :failed="failedPercentage"
      />
    </div>
  </div>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";
import resourceCheckMixin from "@/plugins/resourceCheckMixins.js";

export default {
    components: { ProgressBar },
    mixins: [resourceCheckMixin],
    props: ["check", "name"],
    data: function () {
        return {
            detailRouterArguments: {
                name: "resourceCheckDetail",
                params: {
                    check: this.name,
                    datasetId: this.$store.getters.datasetId,
                },
            },
        };
    },
    methods: {
        detail: function () {
            this.$router.push(this.detailRouterArguments);
        },
    },
};
</script>

<style scoped lang="scss">
@import "@/scss/variables";

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
