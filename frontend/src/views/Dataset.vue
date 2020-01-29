<template>
    <dashboard>
        <h2>{{ $t("sections.dataset") }}</h2>
        <div class="description" v-html=" $t('datasetLevel.description')"></div>
        <b-row class="collection_header" align-h="between">
            <b-col class="text-left">
                <h4>{{ $t("datasetLevel.subheadline") }}</h4>
            </b-col>
            <b-col class="text-right insufficient_switch" @click="insufficientShown = !insufficientShown">
                <span v-if="insufficientShown">
                    <font-awesome-icon icon="eye-slash"/>
                    {{ $t("datasetLevel.insufficientShown") }}
                </span>
                <span v-else>
                    <font-awesome-icon icon="eye"/>
                    {{ $t("datasetLevel.insufficientHidden") }}
                </span>
            </b-col>
        </b-row>
        <template v-for="(section, index) in sections">
            <DatasetLevelSection :section="section" :insufficientShown="insufficientShown" v-bind:key="index"></DatasetLevelSection>
        </template>
    </dashboard>
</template>

<script>
// import Loader from "@/components/Loader.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";
import DatasetLevelSection from "@/components/DatasetLevelSection.vue"

export default {
    name: "dataset",
    components: { Dashboard, DatasetLevelSection },
    data: function() {
        return {
            sections: ["status_distribution", "value_distribution", "other_distribution", "repetition", "other"],
            insufficientShown: true
        };
    },
    mounted() {
        this.insufficientShown = this.$store.getters.insufficientShown;
    },
    watch: {
        insufficientShown: function (newInsufficientShown) {
            this.$store.commit("setInsufficientShown", newInsufficientShown);
        }
    },
};
</script>

<style lang="scss">
@import "src/scss/main";

.insufficient_switch :hover {
    text-decoration: underline;
}

.insufficient_switch {
    color: $primary;
    text-align: right;
    cursor: pointer;
    padding-top: 20px;
    margin-right: 30px;
}



</style>
