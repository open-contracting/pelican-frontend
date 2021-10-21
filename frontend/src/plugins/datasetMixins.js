export default {
    data: function () {
        return {
            checkTypeVersionControl: {
                "distribution.main_procurement_category": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.tender_status": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.tender_procurement_method": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.tender_award_criteria": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.tender_submission_method": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.awards_status": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.contracts_status": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.milestone_status": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.milestone_type": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.document_document_type": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.value_currency": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.related_process_relation": {
                    checkType: "donut",
                    version: 1
                },
                "distribution.tender_value": {
                    checkType: "bar",
                    version: 1
                },
                "distribution.contracts_value": {
                    checkType: "bar",
                    version: 1
                },
                "distribution.awards_value": {
                    checkType: "bar",
                    version: 1
                },
                "misc.url_availability": {
                    checkType: "numeric",
                    version: 1
                },
                "unique.tender_id": {
                    checkType: "numeric",
                    version: 2
                },
                "consistent.related_process_title": {
                    checkType: "numeric",
                    version: 1
                },
                "reference.related_process_identifier": {
                    checkType: "numeric",
                    version: 2
                },
                "distribution.tender_value_repetition": {
                    checkType: "top3",
                    version: 1
                },
                "distribution.contracts_value_repetition": {
                    checkType: "top3",
                    version: 1
                },
                "distribution.awards_value_repetition": {
                    checkType: "top3",
                    version: 1
                },
                "distribution.buyer_repetition": {
                    checkType: "biggest_share",
                    version: 1
                },
                "distribution.buyer": {
                    checkType: "single_value_share",
                    version: 1
                }
            }
        };
    },
    computed: {
        checkType() {
            if (!(this.check.name in this.checkTypeVersionControl)) {
                throw "unknown check: " + this.check.name;
            }

            if (this.check.meta.version != this.checkTypeVersionControl[this.check.name].version) {
                return null;
            }

            return this.checkTypeVersionControl[this.check.name].checkType;
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
