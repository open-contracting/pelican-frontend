export default {
    methods: {
        onePercent: function () {
            return (this.check.total_count) / 100;
        },
        applicationCount() {
            return this.check.passed_count + this.check.failed_count;
        },
    },
    computed: {
        okPercentage() {
            return Math.round(this.check.passed_count / this.onePercent());
        },
        failedPercentage() {
            return Math.round(this.check.failed_count / this.onePercent());
        },
        naPercentage() {
            return Math.round(this.check.undefined_count / this.onePercent());
        },
        passPercentage() {
            return Math.round(
                this.check.passed_count / (this.applicationCount() / 100)
            );
        },
        nonpassPercentage() {
            return Math.round(
                this.check.failed_count / (this.applicationCount() / 100)
            );
        },
    }
};