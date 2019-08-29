export default {
    computed: {
        checkType() {
            var donut = [
                "distribution.main_procurement_category",
                "distribution.tender_status",
                // "distribution.tender_status"
            ];
            if (donut.includes(this.check.name)) {
                return "donut";
            }

            var bar = [
                "distribution.buyer",
                "distribution.tender_value",
                "distribution.contracts_value",
            ];
            if (bar.includes(this.check.name)) {
                return "bar";
            }

            var numeric = ["misc.url_availability"];
            if (numeric.includes(this.check.name)) {
                return "numeric";
            }

            var top3 = [
                "distribution.tender_value_repetition",
                "distribution.contracts_value_repetition",
                "distribution.awards_value_repetition"
            ];
            if (top3.includes(this.check.name)) {
                return "top3";
            }
            return null;
        }
    },
    methods: {
        orderedShares: function (shares) {
            var items = Object.keys(shares).map(function (key) {
                return [key, shares[key]];
            });

            items.sort(function (first, second) {
                return second[1]["count"] - first[1]["count"];
            });

            return items;
        }
    }
};