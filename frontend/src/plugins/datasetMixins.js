export default {
    data: function () {
        return {
            reportOnlyData: {
                "distribution.tender_award_criteria": true,
                "distribution.tender_submission_method": true,
                "distribution.milestone_type": true,
                "distribution.document_document_type": true,
                "distribution.value_currency": true,
                "distribution.related_process_relation": true
            },
            // # Keep in sync with CHECK_TYPES in dataset.py
            checkTypeData: {
                // donut
                "distribution.main_procurement_category": "donut",
                "distribution.tender_status": "donut",
                "distribution.tender_procurement_method": "donut",
                "distribution.tender_award_criteria": "donut",
                "distribution.tender_submission_method": "donut",
                "distribution.awards_status": "donut",
                "distribution.contracts_status": "donut",
                "distribution.milestone_status": "donut",
                "distribution.milestone_type": "donut",
                "distribution.document_document_type": "donut",
                "distribution.value_currency": "donut",
                "distribution.related_process_relation": "donut",
                // bar
                "distribution.tender_value": "bar",
                "distribution.contracts_value": "bar",
                "distribution.awards_value": "bar",
                // numeric
                "misc.url_availability": "numeric",
                "unique.tender_id": "numeric",
                "consistent.related_process_title": "numeric",
                "reference.related_process_identifier": "numeric",
                // top3
                "distribution.tender_value_repetition": "top3",
                "distribution.contracts_value_repetition": "top3",
                "distribution.awards_value_repetition": "top3",
                // biggest_share
                "distribution.buyer_repetition": "biggest_share",
                // single_value_share
                "distribution.buyer": "single_value_share"
            }
        };
    },
    computed: {
        checkType() {
            if (!(this.check.name in this.checkTypeData)) {
                throw "unknown check: " + this.check.name;
            }
            return this.checkTypeData[this.check.name];
        },
        reportOnly() {
            return this.reportOnlyData[this.check.name];
        },
        shares() {
            if (this.checkType == "donut") {
                return this.orderedShares(this.check.meta.shares);
            } else {
                return null;
            }
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
