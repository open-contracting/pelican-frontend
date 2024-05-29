export default {
    data: () => ({
        reportOnlyData: {
            "distribution.tender_award_criteria": true,
            "distribution.tender_submission_method": true,
            "distribution.milestone_type": true,
            "distribution.document_document_type": true,
            "distribution.value_currency": true,
            "distribution.related_process_relation": true,
        },
        // Keep in sync with CHECK_TYPES in dataset.py
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
            "distribution.buyer": "single_value_share",
        },
        // Keep in sync with check descriptions.
        ticksData: {
            // donut
            "distribution.main_procurement_category": [0, 0.95],
            "distribution.tender_status": [0.001, 0.99],
            "distribution.awards_status": [0.001, 0.99],
            "distribution.contracts_status": [0.001, 0.99],
            "distribution.milestone_status": [0.001, 0.99],
            "distribution.tender_procurement_method": [0.001, 0.99],
            // bar
            "distribution.tender_value": [0, 0.5],
            "distribution.contracts_value": [0, 0.5],
            "distribution.awards_value": [0, 0.5],
            // single_value_share
            "distribution.buyer": [0, 0.5],
        },
        // Keep in sync with check descriptions.
        stylesData: {
            // donut
            "distribution.main_procurement_category": [],
            "distribution.tender_status": ["active", "complete"],
            "distribution.awards_status": ["active"],
            "distribution.contracts_status": ["active", "terminated"],
            "distribution.milestone_status": ["met"],
            "distribution.tender_procurement_method": ["open"],
        },
    }),
    computed: {
        checkType() {
            if (!(this.check.name in this.checkTypeData)) {
                throw `unknown check: ${this.check.name}`;
            }
            return this.checkTypeData[this.check.name];
        },
        reportOnly() {
            return this.reportOnlyData[this.check.name];
        },
        ticks() {
            return this.ticksData[this.check.name];
        },
        styles() {
            return this.stylesData[this.check.name];
        },
        shares() {
            if (this.checkType === "donut") {
                return this.orderedShares(this.check.meta.shares);
            } else {
                return null;
            }
        },
    },
    methods: {
        orderedShares: (shares) => {
            var items = Object.keys(shares).map((key) => [key, shares[key]]);

            items.sort((first, second) => second[1].count - first[1].count);

            return items;
        },
    },
};
