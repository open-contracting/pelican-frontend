export const messages = {
    header: "Data Quality Assesment Results",
    sections: {
        home: 'Home',
        overview: 'Overview',
        field: 'Field',
        resource: 'Resource',
        dataset: 'Dataset',
        time: 'Time',
    },
    resourceLevel: {
        ok: "OK",
        failed: "FAILED",
        na: "N/A",
        check: "CHECK",
        coherent: {
            dates: "dates",
            period: "period",
            procurement_method_vs_number_of_tenderers: "procurement_method_vs_number_of_tenderers",
            tender_status: "tender_status",
        },
        consistent: {
            buyer_roles: "buyer_roles",
            number_of_tenderers: "number_of_tenderers",
            tender_value: "tender_value",
        },
        reference: {
            buyer_in_parties: "buyer_in_parties",
            contract_in_awards: "contract_in_awards",
            payee_in_parties: "payee_in_parties",
            payer_in_parties: "payer_in_parties",
            procuring_entity_in_parties: "procuring_entity_in_parties",
            supplier_in_parties: "supplier_in_parties",
            tenderer_in_parties: "tenderer_in_parties",
        }
    }
}