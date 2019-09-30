<template>
    <div class="row d-flex clickable" v-on:click="detail()">
        <div class="col-9 col-lg-5 break_word check_name">
            <span>{{ $t("resourceLevel." + name + ".name") }}</span>
        </div>
        <div class="col-1 col-lg-1 text-right">
            <span v-if=" okPercentage> 0" class="value_ok">{{ okPercentage }}%</span>
        </div>
        <div class="col-1 col-lg-1 text-right">
            <span v-if=" failedPercentage> 0" class="value_failed">{{ failedPercentage }}%</span>
        </div>
        <div class="col-1 col-lg-1 text-right">
            <span v-if=" naPercentage> 0" class="value_na">{{ naPercentage }}%</span>
        </div>
        <div class="col-4 d-none d-lg-block progress_column">
            <ProgressBar :ok="okPercentage" :failed="failedPercentage" />
        </div>
    </div>
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
</style>