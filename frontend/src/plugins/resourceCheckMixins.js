export default {
  methods: {
    onePercent: function () {
      return this.check.total_count / 100;
    },
    applicationCount() {
      return this.check.passed_count + this.check.failed_count;
    },
  },
  computed: {
    okPercentage() {
      return (100 * this.check.passed_count) / this.check.total_count;
    },
    failedPercentage() {
      return (100 * this.check.failed_count) / this.check.total_count;
    },
    naPercentage() {
      return (100 * this.check.undefined_count) / this.check.total_count;
    },
    passPercentage() {
      return (100 * this.check.passed_count) / this.applicationCount();
    },
    nonpassPercentage() {
      return (100 * this.check.failed_count) / this.applicationCount();
    },
    individualPassPercentage() {
      return (
        (100 * this.check.individual_passed_count) /
        this.check.individual_application_count
      );
    },
    individualFailedPercentage() {
      return (
        (100 * this.check.individual_failed_count) /
        this.check.individual_application_count
      );
    },
  },
};
