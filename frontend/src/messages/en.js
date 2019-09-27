export const messages = {
    header: "Data Quality Assesment Results",
    loader: {
        generic: "Still loading the great stuff for you. Please be patient.",
        examples: "Generating random examples for you. Please be patient, this takes some time for big datasets"
    },
    ocid: "ocid",
    ocids: "ocids",
    passed: "Passed",
    failed: "Failed",
    notAvailable: "Not available",
    created: "created",
    modified: "modified",
    core: {
        passedExamples: "Passed examples",
        failedExamples: "Failed examples",
        undefinedExamples: "Undefined examples",
    },
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
        label_1: "1",
        label_2_20: "2 - 10",
        label_21_50: "21 - 50",
        label_51_100: "51 - 100",
        label_100: "100+",
        examples: "Examples",
        distribution: {
            tender_status: {
                name: "Tender status distribution",
                description: "Calculates a frequency of occurence of different tender statuses. The check passes if <i>active</i> and <i>complete</i> status is present in 0.1 - 99% cases",
                description_long: "Calculates a frequency of occurence of different tender statuses. The check passes if <i>active</i> and <i>complete</i> status is present in 0.1 - 99% cases"
            },
            contracts_value_repetition: {
                name: "Contracts value repetition",
                description: "Examines that contract values are not repeating to frequently. 3 most frequent <i>contracts[i].value.amount</i> and <i>contracts[i].value.currency</i> combinations should appear in fewer than 10% of tenders.",
                description_long: "Examines that contract values are not repeating to frequently. 3 most frequent <i>contracts[i].value.amount</i> and <i>contracts[i].value.currency</i> combinations should appear in fewer than 10% of tenders."
            },
            awards_value_repetition: {
                name: "Awards value repetition",
                description: "Examines that award values are not repeating to frequently. 3 most frequent <i>awards[i].value.amount</i> and <i>awards[i].value.currency</i> combinations should appear in fewer than 10% of tenders.",
                description_long: "Examines that award values are not repeating to frequently. 3 most frequent <i>awards[i].value.amount</i> and <i>awards[i].value.currency</i> combinations should appear in fewer than 10% of tenders."
            },
            tender_value_repetition: {
                name: "Tender value repetition",
                description: "Examines that tender values are not repeating to frequently. 3 most frequent <i>tender.value.amount</i> and <i>tender.value.currency</i> combinations should appear in fewer than 10% of tenders.",
                description_long: "Examines that values are not repeating to frequently. 3 most frequent <i>tender.value.amount</i> and <i>tender.value.currency</i> combinations should appear in fewer than 10% of tenders."
            },
            buyer: {
                name: "Buyer distribution",
                description: "This check examines a suspicious number of small buyers having only one OCID. This can indicate a problem in publishing buyers identifiers. It fails if the share of single OCID buyers is > 50%",
                description_long: "This check examines a suspicious number of small buyers having only one OCID. This can indicate a problem in publishing buyers identifiers. It fails if the share of single OCID buyers is > 50%",
            },
            tender_value: {
                name: "Tender value distribution",
                description: "If sum of 1% of top tender values is more than 50% of sum of all tender values it may indicate some insanely high published numbers.",
                description_long: "This check processes all <i>tender.value</i> values which has both amount and currency set. <ul><li>It converts all values to USD using compiled releases <i>date</i> field.</li><li>It calculates a total amount of all tenders values converted to USD.</li><li>It orders all values in descending order and checks that the 1% of top values (10 out of 1000 even that the 11th value is the same as 10th) is not more than 50% of the total amount.</li></ul> For illustration purposes also the share of other groups of values is shown. For example 20 - 50% shows what is the share of values 201-500 (considering 1000 values) in ordered list of values."
            },
            awards_value: {
                name: "Awards value distribution",
                description: "If sum of 1% of top award values is more than 50% of sum of all award values it may indicate some insanely high published numbers.",
                description_long: "This check processes all <i>awards[i].value</i> values which has both amount and currency set. <ul><li>It converts all values to USD using compiled releases <i>date</i> field.</li><li>It calculates a total amount of all awards values converted to USD.</li><li>It orders all values in descending order and checks that the 1% of top values (10 out of 1000 even that the 11th value is the same as 10th) is not more than 50% of the total amount.</li></ul> For illustration purposes also the share of other groups of values is shown. For example 20 - 50% shows what is the share of values 201-500 (considering 1000 values) in ordered list of values."
            },
            contracts_value: {
                name: "Contracts value distribution",
                description: "If sum of 1% of top contract values is more than 50% of sum of all contract values it may indicate some insanely high published numbers.",
                description_long: "This check processes all <i>contract[i].value</i> values which has both amount and currency set. <ul><li>It converts all values to USD using compiled releases <i>date</i> field.</li><li>It calculates a total amount of all contracts values converted to USD.</li><li>It orders all values in descending order and checks that the 1% of top values (10 out of 1000 even that the 11th value is the same as 10th) is not more than 50% of the total amount.</li></ul> For illustration purposes also the share of other groups of values is shown. For example 20 - 50% shows what is the share of values 201-500 (considering 1000 values) in ordered list of values."
            },
            main_procurement_category: {
                name: "Main procurement category distribution",
                description: "Checks that no value of <i>tender.mainProcurementCategory</i> occurs in more than 95 % cases which would be unnatural distribution.",
                description_long: "Checks that no value of <i>tender.mainProcurementCategory</i> occurs more than 95 % of the time."
            },
            tender_procurement_method: {
                name: "Procurement method distribution",
                description: "Calculates a frequency of occurence of different procurement methods. The check passes if <i>open</i> procurement method is present in 0.1 - 99% cases",
                description_long: "Checks that no value of <i>tender.mainProcurementCategory</i> occurs more than 95 % of the time."
            },
            tender_award_criteria: {
                name: "Award criteria distribution",
                description: "Calculates a frequency of occurence of different award criteria. This check passes always and serves only for data presentation",
                description_long: "Calculates a frequency of occurence of different award criteria. This check passes always and serves only for data presentation"
            },
            tender_submission_method: {
                name: "Submission method distribution",
                description: "Calculates a frequency of occurence of different submission methods. This check passes always and serves only for data presentation",
                description_long: "Calculates a frequency of occurence of different submission methods. This check passes always and serves only for data presentation"
            },
            awards_status: {
                name: "Award status distribution",
                description: "Calculates a frequency of occurence of different statuses of awards. The check passes if <i>active</i> status is present in 0.1 - 99% cases",
                description_long: "Calculates a frequency of occurence of different statuses of awards. The check passes if <i>active</i> status is present in 0.1 - 99% cases"
            },
            contracts_status: {
                name: "Contract status distribution",
                description: "Calculates a frequency of occurence of different statuses of contracts. The check passes if <i>active</i> and <i>terminated</i> status is present in 0.1 - 99% cases",
                description_long: "Calculates a frequency of occurence of different statuses of contracts. The check passes if <i>active</i> and <i>terminated</i> status is present in 0.1 - 99% cases"
            },
            milestone_status: {
                name: "Milestone status distribution",
                description: "Calculates a frequency of occurence of different statuses of milestones. All milestones from all phases of contracting process are included. The check passes if <i>met</i> status is present in 0.1 - 99% cases",
                description_long: "Calculates a frequency of occurence of different statuses of milestones. All milestones from all phases of contracting process are included. Namely: <ul><li>planning.milestones.status</li><li>tender.milestones.status</li><li>contracts.milestones.status</li><li>contracts.implementation.milestones.status</li></ul>The check passes if <i>met</i> status is present in 0.1 - 99% cases"
            },
            milestone_type: {
                name: "Milestone type distribution",
                description: "Calculates a frequency of occurence of different types of milestones. All milestones from all phases of contracting process are included. This check passes everytime and serves only for data presentation",
                description_long: "Calculates a frequency of occurence of different types of milestones. All milestones from all phases of contracting process are included. Namely: <ul><li>planning.milestones.type</li><li>tender.milestones.type</li><li>contracts.milestones.type</li><li>contracts.implementation.milestones.type</li></ul>This check passes everytime and serves only for data presentation"
            },
            document_type: {
                name: "Document type distribution",
                description: "Calculates a frequency of occurence of different types of documents. All documents from all phases of contracting process are included. This check passes everytime and serves only for data presentation",
                description_long: "Calculates a frequency of occurence of different types of documents. All documents from all phases of contracting process are included. Namely: <ul><li>planning.documents.documentType</li><li>tender.documents.documentType</li><li>awards.documents.documentType</li><li>contracts.documents.documentType</li><li>contracts.implementation.documents.documentType</li><li>contracts.milestones.documents.documentType</li></ul>This check passes everytime and serves only for data presentation"
            },
            value_currency: {
                name: "Currency distribution",
                description: "Calculates a frequency of occurence of different currencies. Currencies from all value objects from all phases of contracting process are included. This check passes everytime and serves only for data presentation",
                description_long: "Calculates a frequency of occurence of different currencies. Currencies from all value objects from all phases of contracting process are included. Namely: <ul><li>tender.value.currency</li><li>tender.minValue.currency</li><li>awards.value.currency</li><li>contracts.value.currency</li><li>planning.budget.value.currency</li><li>contracts.implementation.transactions.value.currency</li></ul>This check passes everytime and serves only for data presentation"
            },
            related_process_relation: {
                name: "Related process relation distribution",
                description: "Calculates a freque   ncy of occurence of different relations between related processes. This check passes everytime and serves only for data presentation",
                description_long: "Calculates a freque   ncy of occurence of different relations between related processes. This check passes everytime and serves only for data presentation"
            },
            document_document_type: {
                name: "Document type distribution",
                description: "Calculates a frequency of occurence of different types of documents. All documents from all phases of contracting process are included. This check passes everytime and serves only for data presentation",
                description_long: "Calculates a frequency of occurence of different types of documents. All documents from all phases of contracting process are included. This check passes everytime and serves only for data presentation",
            },
        },
        unique: {
            ok: "All values are unique.",
            failed: "There are non-unique values.",
            id: {
                name: "id",
                description: "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
            }
        },
        misc: {
            url_availability: {
                name: "URL availability",
                description: "This check examines a random sample of URLs collected accross the whole data collection and tests whether requests to these URLs returns valid response. This check passes if all responses are valid.",
                description_long: "This check examines a random sample of URLs collected accross the whole data collection and tests whether requests to these URLs returns valid response. This check passes if all responses are valid"
            }
        },
        consistent: {
            related_process_title: {
                name: "Related processes tile consistency",
                description: "Related process reference should have the same title as the related process itself.",
                description_long: "If two related processes with <i>ocid</i> scheme are detected it's tested that they have the same title. <i>relatedProcesses[i].title</i> or <i>contracts[i].relatedProcesses[j].title</i> is compared to tender.title of corresponding compiled release."
            }
        },
        reference: {
            related_process_identifier: {
                name: "Related processes identifier reference",
                description: "If compiled release references to some related process using <i>ocid</i> scheme in <i>relatedProcesses[i]</i> or <i>contracts[i].relatedProcesses[j]</i> compiled release with such ocid must exist in a collection",
                description_long: "If compiled release references to some related process using <i>ocid</i> scheme in <i>relatedProcesses[i]</i> or <i>contracts[i].relatedProcesses[j]</i> compiled release with such ocid must exist in a collection"
            }
        },
        numeric: {
            passed: "passed",
            processed: "tested",
            failed: "failed",
            failedExamples: "Failed examples",
            passedExamples: "Passed examples",
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
                description: "Checks that there are no awards or contracts if the status of tender is <i>planning</i>, <i>planned</i>, <i>active</i>, <i>cancelled</i>, <i>unsuccessful</i> or <i>withdrawn</i>."
            },
            awards_status: {
                name: "Awards status - contracts",
                description: "Checks that there are no contracts for a given award if its status is <i>pending</i>, <i>cancelled</i> or <i>unsuccessful</i>."
            },
            contracts_status: {
                name: "Contract status - transactions",
                description: "Checks that there are no transactions for a given contract if its status is <i>pending</i>, <i>cancelled</i>."
            },
            milestone_status: {
                name: "Milestone status - dateMet",
                description: "Checks that dateMet is not set or is empty if milestone's status is either <i>scheduled</i> or <i>notMet</i>."
            },
            value_realistic: {
                name: "Realisitic value",
                description: "Checks whether the value's amount converted to USD is between -5 billion USD and 5 billion USD"
            },
            dates: {
                name: "Coherent dates",
                description: "Checks the logical chain of dates within a contracting process. Tender's tenderPeriod has to end before tender's contractPeriod starts. It also has to end before any award is awarded or any contract is signed. All contracts signature dates as well as awards dates has to be lower or equal to the compiled release's date. A contract cannot be signed before the related award is awarded. Each contract has to be signed before any transaction for this contract happens. Following pairs of dates are being compared if both are available (first has to be lower or the second): <ul><li>tender.tenderPeriod.endDate, tender.contractPeriod.startDate</li><li>tender.tenderPeriod.endDate, any contracts[i].dateSigned</li><li>any contracts[i].dateSigned, date</li><li>tender.tenderPeriod.endDate, any awards[i].date</li><li>any awards[i].date, date</li><li>awards[i].date, contracts[j].dateSigned - only pairs where awards[i].id = contracts[j].awardID</li><li>contracts[i].dateSigned, contracts[i].implementation.transactions[j].date - only compare transactions that relates to the specific contract (those that are nested in a particular contract object)</li></ul>"
            },
            milestones_dates: {
                name: "Milestones dates",
                description: "Checks that the date when a milestone was met is after the date when it was last modified. Both dates have to be lower or equal to the compiled release's date"
            },
            amendments_dates: {
                name: "Amendment dates",
                description: "Depending to which phase of contracting process the specific amendment belongs it checks that it was amended after tender period started or after the particular award was awarded or after the particular contract was signed. All date also has to be lower or equal to the compiled release's date"
            },
            documents_dates: {
                name: "Documents dates",
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
                description: "Compares a total value of all contracts related to one award and checks that the sum of all relevant contract values does not differ from the matching award's value by more than 50%. All considered values either have the same currency or can be converted to USD using compiled releases <i>date</i> field."
            },
            contracts_implementation_transactions_value: {
                name: "Contract value - transactions value",
                description: "Compares a total value of all transactions related to one contract and checks that the sum of all transaction values is less or equal to contract's value. All considered values either have the same currency or can be converted to USD using compiled releases <i>date</i> field."
            },
            parties_roles: {
                name: "Parties roles",
                description: "Examines whether parties are assigned to correct roles by checking that a given party is also referenced from a correct place in a compiled release. For example when a party has a role 'supplier' it has to be referenced from at least one award's 'suppliers' array. Roles that are being tester are <ul><li>procuringEntity</li><li>tenderer</li><li>supplier</li><li>payer</li><li>payee</li></ul>"
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
    },
    overview: {
        collection_metadata: "COLLECTION METADATA",
        kingfisher_metadata: "KINGFISHER METADATA",
        dqt_metadata: "DATA QUALITY TOOL METADATA",
        compiled_releases: {
            title: "COMPILED RELEASES",
            value_label: "Total Unique OCIDs"
        },
        prices: {
            title: "PRICES",
            value_label: "Total Value",
            contracts: "contracts",
            thead: {
                category: "price category",
                count: "contracts count",
                share: "% of total value"
            },
            info: "This visualization show the total value of contracts in US dollars. Only contracts for which value could" +
                " be converted to US dollars we used. Contracts are further broken down into several price categories." +
                " Number of contracts for each category is displayed together with a share of those contracts on the total value."
        },
        period: {
            title: "PERIOD",
            subtitle: "Compiled Releases in Time",
            description: "Distribution of compiled releases in time based on compiled release's Date field."
        },
        lifecycle: {
            title: "TENDER LIFECYCLE",
            planning: "Planning",
            tender: "Tender",
            award: "Award",
            contract: "Contract",
            implementation: "Implementation",
            info: "A number of occurrences of a particural section in all compiled releases." +
                " While plannings and tenders can appear only once in each compiled release awards, contracts and implementation" +
                " can be present multipletimes."
        },
        publisher: "Publisher",
        datalicense: "Data License",
        extensions: "Extensions",
        publishedFrom: "Published From",
        publishedTo: "Published To",
        collectionId: "Collection ID",
        processingFrom: "Processing Start",
        processingTo: "Processing End"
    },
    field: {
        title: "Field Level Checks",
        description: [
            "Field level checks control each field separately without using information from other fields. Each field can be checked on two levels.",
            "Coverage - presence of a field is checked. Empty field is considered to be missing. Each field can be checked as many times as is" +
            " the number of occurence of its parent structure. For example, if there is 50k awards in a dataset containing 90k suppliers in total" +
            " awards.title check can be performed 50.000x but awards.suppliers.id can be performed 90.000x",
            "Quality - once the field is present additional quality checks like is it a non-negative number or is it a two-letter lowercase ISO639-1 code can" +
            " be performed. These controls run only for fields that are present in the dataset."
        ],
        all: "ALL CHECKS",
        table: {
            head: {
                object: "OBJECT",
                coverage: "COVERAGE",
                quality: "QUALITY"
            }
        },
        search: "Search object by name",
        hidden: "Another {n} checks was hidden"
    },
    fieldDetail: {
        checks: "checks",
        path: "Field path",
        coverage: {
            label: "Coverage",
            exists: {
                count_header: "Exists"
            },
            non_empty: {
                count_header: "Non-Empty"
            }
        },
        quality: {
            label: "Quality",
            ocid_prefix_check: {
                count_header: "Registered prefix"
            },
            date_time: {
                count_header: "Realistic datetime"
            },
            email: {
                count_header: "Email format"
            },
            identifier_scheme: {
                count_header: "Identifier scheme"
            },
            telephone: {
                count_header: "Telephone format"
            },
            document_description_length: {
                count_header: "Document description length"
            },
            document_type: {
                count_header: "Coherent document type"
            },
            document_format_codelist: {
                count_header: "Document format"
            },
            number_checks: {
                count_header: "Non-negative value"
            },
            language: {
                count_header: "Two-letter lowercase ISO639-1 code"
            }
        }
    },
    timeLevel: {
        checkResult: "Check result",
        coverageResult: "Coverage result",
        subheadline: "All Time Variance Level Checks",
        coverage: {
            header: "Contracting realeases processed:",
            ok: "Ok",
            failed: "Not included"
        },
        check: {
            header: "Contracting realeases checked:",
            ok: "Ok",
            failed: "Failed"
        },
        phase_stable: {
            name: "Phase stability",
            description: "Generate Lorem Ipsum placeholder text for use in your graphic, print and web layouts, and discover plugins for your favorite writing, design and blogging tools.",
            descriptionLong: "Generate Lorem Ipsum placeholder text for use in your graphic, print and web layouts, and discover plugins for your favorite writing, design and blogging tools."

        },
        ocid: {
            name: "OCID existence",
            description: "Generate Lorem Ipsum placeholder text for use in your graphic, print and web layouts, and discover plugins for your favorite writing, design and blogging tools.",
            descriptionLong: "Generate Lorem Ipsum placeholder text for use in your graphic, print and web layouts, and discover plugins for your favorite writing, design and blogging tools."

        },
        tender_title: {
            name: "Tender title stability",
            description: "Generate Lorem Ipsum placeholder text for use in your graphic, print and web layouts, and discover plugins for your favorite writing, design and blogging tools.",
            descriptionLong: "Generate Lorem Ipsum placeholder text for use in your graphic, print and web layouts, and discover plugins for your favorite writing, design and blogging tools."

        },
    }
}