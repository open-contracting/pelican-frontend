export default {
    computed: {
        datasetId() {
            return this.$store.getters.datasetId;
        },
        fieldLoaded() {
            return this.$store.getters.fieldLevelStats != null;
        },
        resourceLoaded() {
            return this.$store.getters.resourceLevelStats != null;
        },
        datasetLoaded() {
            return this.$store.getters.datasetLevelStats != null;
        },
        timeVarianceLoaded() {
            return this.$store.getters.timeVarianceLevelStats != null;
        },
        atLeastOneLoaded() {
            return this.datasetLoaded || this.resourceLoaded || this.fieldLoaded || this.timeVarianceLoaded;
        },
    },
};
