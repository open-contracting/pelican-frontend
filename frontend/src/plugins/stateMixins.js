export default {
  computed: {
    datasetId() {
      return this.$store.getters.datasetId;
    },
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
      return (
        this.datasetLoaded ||
        this.resourceLoaded ||
        this.fieldLoaded ||
        this.timeVarianceLoaded
      );
    },
  },
};
