export default {
    computed: {
        resourceLoaded() {
            if (this.$store.getters.resourceLevelStats != null) {
                return true;
            }
            return false;
        },
        datasetLoaded() {
            if (this.$store.getters.datasetLevelStats != null) {
                return true;
            }
            return false;
        },
        fieldLoaded() {
            if (this.$store.getters.fieldLevelStats != null) {
                return true;
            }
            return false;
        },
        timeVarianceLoaded() {
            if (this.$store.getters.timeVarianceLevelStats != null) {
                return true;
            }
            return false;
        },
        atLeastOneLoaded() {
            if (this.$store.getters.datasetLevelStats != null || this.$store.getters.resourceLevelStats != null ||
                this.$store.getters.fieldLevelStats != null || this.$store.getters.timeVarianceLevelStats != null) {
                return true;
            }
            return false;
        }
    },
};