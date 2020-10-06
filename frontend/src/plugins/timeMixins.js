export default {
    computed: {
        coverageShare() {
            if (this.check.meta.total_count == 0) {
                return 0.0;
            }

            return (this.check.meta.coverage_count / this.check.meta.total_count);
        },
        coveragePercentage() {
            return 100.0 * this.coverageShare;
        },
        checkShare() {
            if (this.check.meta.coverage_count == 0) {
                return 0.0;
            }

            return (this.check.meta.ok_count / this.check.meta.coverage_count);
        },
        checkPercentage() {
            return 100.0 * this.checkShare;
        }
    },
};