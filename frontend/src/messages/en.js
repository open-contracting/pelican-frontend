export const messages = {
    header: "Data Quality Assesment Results",
    loader: "Still loading the great stuff for you. Please be patient.",
    passed: "Passed",
    failed: "Failed",
    notAvailable: "Not available",
    created: "created",
    modified: "modified",
    dataset: {
        id: "id",
        size: "items count",
        phase: "phase",
        selectDataset: "show"
    },
    unsufficientData: {
        title: "Unsufficient data",
        description: "The check could not have been calculated because of unsufficient data."
    },
    sections: {
        home: 'Home',
        overview: 'Overview',
        field: 'Field',
        resource: 'Resource',
        dataset: 'Dataset',
        time: 'Time',
    },
    preview: {
        metadata: "Metadata",
        ocds_data: "OCDS Data Preview"
    },
    examples: {
        failed: "Sample releases with failed rules",
        passed: "Sample releases with passed rules",
        actions: "actions",
        preview: "preview",
        ocid: "ocid",
        showMore: "show more examples",
        showLess: "hide"
    },
    datasetLevel: {
        subheadline: "All Dataset Level Checks",
        label_0_1: "1%",
        label_1_5: "1 - 5%",
        label_5_20: "5 - 10%",
        label_20_50: "20 - 50%",
        label_50_100: "50 - 100%",
        distribution: {
            tender_status: {
                name: "Tender status distribution",
                description: "Calculates a frequenfy of occurence of different tender statuses. The check passes if <i>active</i> and <i>complete</i> status is present in 0.1 - 99% cases",
                description_long: "Calculates a frequenfy of occurence of different tender statuses. The check passes if <i>active</i> and <i>complete</i> status is present in 0.1 - 99% cases"
            },
            contracts_value_repetition: {
                name: "Contracts value repetition",
                description: "Examines that contract values are not repeating to frequently. 3 most frequent <i>contracts[i].value.amount</i> and <i>contracts[i].value.currency</i> combinations should appear in fewer than 10% of tenders.",
                description: "Examines that contract values are not repeating to frequently. 3 most frequent <i>contracts[i].value.amount</i> and <i>contracts[i].value.currency</i> combinations should appear in fewer than 10% of tenders."
            },
            awards_value_repetition: {
                name: "Awards value repetition",
                description: "Examines that award values are not repeating to frequently. 3 most frequent <i>awards[i].value.amount</i> and <i>awards[i].value.currency</i> combinations should appear in fewer than 10% of tenders.",
                description: "Examines that award values are not repeating to frequently. 3 most frequent <i>awards[i].value.amount</i> and <i>awards[i].value.currency</i> combinations should appear in fewer than 10% of tenders."
            },
            tender_value_repetition: {
                name: "Tender value repetition",
                description: "Examines that tender values are not repeating to frequently. 3 most frequent <i>tender.value.amount</i> and <i>tender.value.currency</i> combinations should appear in fewer than 10% of tenders.",
                description_long: "Examines that values are not repeating to frequently. 3 most frequent <i>tender.value.amount</i> and <i>tender.value.currency</i> combinations should appear in fewer than 10% of tenders."
            },
            buyer: {
                name: "Buyer distribution",
                description: "This check examines a suspicious number of small buyers having only one OCID. This can indicate a problem in publishing buyers identifiers. It fails if the share of single OCID buyers is > 50%",
                description: "This check examines a suspicious number of small buyers having only one OCID. This can indicate a problem in publishing buyers identifiers. It fails if the share of single OCID buyers is > 50%",
            },
            tender_value: {
                name: "Tender value distribution",
                description: "If sum of 1% of top tender values is more than 50% of sum of all tender values it may indicate some insanely high published numbers.",
                description_long: "Checks that the sum of the top 1% of <i>tender.value</i> values is < 50%. Displays share of each interval of top values on the overall awards value."
            },
            awards_value: {
                name: "Awards value distribution",
                description: "If sum of 1% of top award values is more than 50% of sum of all award values it may indicate some insanely high published numbers.",
                description_long: "Checks that the sum of the top 1% of <i>awards[i].value</i> values is < 50%. Displays share of each interval of top values on the overall awards value."
            },
            contracts_value: {
                name: "Contracts value distribution",
                description: "If sum of 1% of top contract values is more than 50% of sum of all contract values it may indicate some insanely high published numbers.",
                description: "Checks that the sum of the top 1% of contracts[i].value values is < 50%. Displays share of each interval of top values on the overall contracts value."
            },
            main_procurement_category: {
                name: "Main procurement category distribution",
                description: "Checks that no value of <i>tender.mainProcurementCategory</i> occurs in more than 95 % cases which would be unnatural distribution.",
                description_long: "Checks that no value of <i>tender.mainProcurementCategory</i> occurs more than 95 % of the time."
            },
        },
        unique: {
            id: {
                name: "id",
                description: "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
            }
        },
        misc: {
            url_availability: {
                name: "url_availability",
                description: "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
            }
        }
    },
    resourceLevel: {
        subheadline: "All Resource Level Checks",
        ok: "OK",
        failed: "FAILED",
        na: "N/A",
        check: "CHECK",
        count_header: "Checked contracting processes:",
        application_count_header: "Individual checks:",
        coherent: {
            categoryName: "Coherency",
            period: {
                name: "Period start and end date",
                description: "Checks that the startDate of a period is lower or equal to the endDate of a given period."
            },
            procurement_method_vs_number_of_tenderers: {
                name: "Procurement method - number of tenderers",
                description: "Checks that 'numberOfTenderers' is 0 or 1 if procurementMethod is 'direct'."
            },
            tender_status: {
                name: "Tender status - awards and contracts",
                description: "Checks that there are no awards or contracts if the status of tender is planning, planned, active, cancelled, unsuccessful or withdrawn."
            },
            awards_status: {
                name: "Awards status - contracts",
                description: "Checks that there are no contracts for a given award if its status is pending, cancelled or unsuccessful."
            },
            contracts_status: {
                name: "Contract status - transactions",                                                                    
                description: "Checks that there are no transactions for a given contract if its status is pending, cancelled."
            },
            milestone_status: {
                name: "Milestone status - dateMet",                                                                    
                description: "Checks that dateMet is not set or is empty if milestone's status is either 'scheduled' or 'notMet'."
            },
            value_realistic: {
                name: "Realisitic value",                                                                    
                description: "Checks whether the value's amount converted to USD is between -5 billion USD and 5 billion USD"
            },
            dates: {
                name: "Realisitic value",                                                                    
                description: "Checks the logical chain of dates within a contracting process. Tender's tenderPeriod has to end before tender's contractPeriod starts. It also has to end before any award is awarded or any contract is signed. All contracts signature date as well as awards dates has to be lower or equal to the compiled release's date. A contract cannot be signed before the related award is awarded. Each contract has to be signed before any transaction for this contract happens."
            },
            milestones_dates: {
                name: "Contracting process dates",                                                                    
                description: "Checks that the date when a milestone was met is after the date when it was last modified. Both dates have to be lower or equal to the compiled release's date"
            },
            amendments_dates: {
                name: "Amendment dates",                                                                    
                description: "Depending to which phase of contracting process the specific amendment belongs it checks that it was amended after tender period started or after the particular award was awarded or after the particular contract was signed. All date also has to be lower or equal to the compiled release's date"
            },
            document_dates: {
                name: "Document dates",                                                                    
                description: "Checks that the publication date of a document is lower or equal to the modification date and that both are lower or equal to the compiled release's date"
            },
        },
        consistent: {
            categoryName: "Consistency",
            number_of_tenderers: {
                name: "Number of tenderers - tenderers size",
                description: "Checks whether number of tenderers is consistent with a size of tenderers array. This can be only checked if both values are set."
            },
            tender_value: {
                name: "Tender value - planning budget",
                description: "Compares value of tender and amount of a budget. This check can be performed if both values are positive or negative numbers, both have 'amount' and 'currency' set and both values either have the same currency or can be converted to USD. If so, the check passes if value of a tender does not differ from budget by more than 50 %. 100% is a budget amount."
            },
            contracts_value: {
                name: "Contracts value - award value",
                description: "Compares a total value of all contracts related to one award. The sum of all relevant contract values does not differ from the matching award's value by more than 50%"
            },
            contracts_implementation_transactions_value: {
                name: "Contract value - transactions value",
                description: "Compares a total value of all transactions related to one contract. The sum of all transaction values is less or equal to contract's value"
            },
            parties_role: {
                name: "Parties roles",
                description: "Examines whether parties are assigned to correct roles by checking that a given party is also referenced from a correct place in a compiled release. For example when a party has a role 'supplier' it has to be referenced from at least one award's 'suppliers' array."
            },
            period_duration_in_days: {
                name: "Period duration",
                description: "Compares date fields within a given period with 'durationInDays' field. Duration in days must be equal to the difference between startDate and endDate. If endDate is not set then durationInDays must be equal to the difference between startDate and maxExtentDate."
            },
            buyer_in_parties_roles: {
                name: "Party has a 'buyer' role",
                description: "Examines whether organization from a 'parties' array referenced from a buyer field has a 'buyer' role set."
            },
            supplier_in_parties_roles: {
                name: "Party has a 'supplier' role",
                description: "Examines whether organization from a 'parties' array referenced from a specific supplier has a 'supplier' role set."
            },
            tenderer_in_parties_roles: {
                name: "Party has a 'tenderer' role",
                description: "Examines whether organization from a 'parties' array referenced from a specific tenderer has a 'tenderer' role set."
            },
            procuring_entity_in_parties_roles: {
                name: "Party has a 'procuringEntity' role",
                description: "Examines whether organization from a 'parties' array referenced from a tender's procuringEntity field has a 'procuringEntity' role set."
            },
            payer_in_parties_roles: {
                name: "Party has a 'payer' role",
                description: "Examines whether organization from a 'parties' array referenced from a specific payer has a 'payer' role set."
            },
            payee_in_parties_roles: {
                name: "Party has a 'payee' role",
                description: "Examines whether organization from a 'parties' array referenced from a specific payee has a 'payee' role set."
            },
            buyer_name_in_parties: {
                name: "Buyer's name",
                description: "Checks that the name of a buyer is the same for 'buyer' OrganizationReference as well as for the referenced Organization in 'parties' array"
            },
            payee_name_in_parties: {
                name: "Payee's name",
                description: "Checks that the name of a payee is the same for 'payee' OrganizationReference as well as for the referenced Organization in 'parties' array"
            },
            payer_name_in_parties: {
                name: "Payer's name",
                description: "Checks that the name of a payer is the same for 'payer' OrganizationReference as well as for the referenced Organization in 'parties' array"
            },
            procuring_entity_name_in_parties: {
                name: "Procuring entity's name",
                description: "Checks that the name of a procuring entity is the same for 'procuringEntity' OrganizationReference as well as for the referenced Organization in 'parties' array"
            },
            supplier_name_in_parties: {
                name: "Supplier's name",
                description: "Checks that the name of a supplier is the same for 'suppliers' OrganizationReference as well as for the referenced Organization in 'parties' array"
            },
            tenderer_name_in_parties: {
                name: "Tenderer's name",
                description: "Checks that the name of a tenderer is the same for 'tenderers' OrganizationReference as well as for the referenced Organization in 'parties' array"
            },
        },
        reference: {
            categoryName: "Reference",
            buyer_in_parties: {
                name: "Buyer to parties",
                description: "Checks that the 'id' from 'buyer' OrganizationReference references to an existing Organization in 'parties' array"
            },
            payee_in_parties: {
                name: "Payee to parties",
                description: "Checks that the 'id' from 'payee' OrganizationReference references to an existing Organization in 'parties' array"
            },
            payer_in_parties: {
                name: "Payer to parties",
                description: "Checks that the 'id' from 'payer' OrganizationReference references to an existing Organization in 'parties' array"
            },
            procuring_entity_in_parties: {
                name: "Procuring entity to parties",
                description: "Checks that the 'id' from 'procuringEntity' OrganizationReference references to an existing Organization in 'parties' array"
            },
            supplier_in_parties: {
                name: "Supplier to parties",
                description: "Checks that the 'id' from 'suppliers' OrganizationReference references to an existing Organization in 'parties' array"
            },
            tenderer_in_parties: {
                name: "Tenderer to parties",
                description: "Checks that the 'id' from 'tenderers' OrganizationReference references to an existing Organization in 'parties' array"
            },
            contract_in_awards: {
                name: "Contract - Award",
                description: "Checks whether proper reference to an award is set for particular contract. It passes if 'awards' array contains exactly one item with a proper id (determined by contract's awardID) set"
            },
        }
    }
}