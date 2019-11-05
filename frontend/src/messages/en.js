export const messages = {
    header: "Data Quality Assessment Results",
    loader: {
        generic: "Loading… Please be patient.",
        examples: "Generating random examples… This takes some time for big datasets. Please be patient."
    },
    ocid: "ocid",
    ocids: "ocids",
    passed: "Passed",
    failed: "Failed",
    notAvailable: "Not available",
    created: "Created",
    modified: "Modified",
    core: {
        passedExamples: "Passed examples",
        failedExamples: "Failed examples",
        undefinedExamples: "Undefined examples"
    },
    kingfisherId: "Kingfisher ID",
    dataset: {
        id: "ID",
        name: "Name",
        size: "Items count",
        phase: "Phase",
        selectDataset: "Show",
        search: "Search dataset by name",
        timeVariance: "Time variance checks"
    },
    unsufficientData: {
        title: "Insufficient data",
        description: "Data was insufficient to calculate the check."
    },
    sections: {
        home: "Home",
        overview: "Overview",
        field: "Field",
        resource: "Compiled release",
        dataset: "Collection",
        time: "Time"
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
        previewOld: "preview old",
        previewNew: "preview new",
        ocid: "ocid",
        showMore: "show more examples",
        showLess: "hide"
    },
    datasetLevel: {
        description: "Collection checks focuses on a single field or structure in OCDS and inspects whether it has naturall distribution or whether the value repetition is not unexpectedly high. For some of the checks there are rules that may cause that the check fails (too frequent price value) but there are also checks that always pass. The purpose of such checks is to visualize the collection content but there can be no significant failure (document type distribution).",
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
                description: "This check examines a suspicious number of small buyers having only one OCID. This can indicate a problem in publishing buyers identifiers. It fails if more than 50% of all buyers have just one OCID.",
                description_long: "This check examines a suspicious number of small buyers having only one OCID. This can indicate a problem in publishing buyers identifiers. It fails if more than 50% of all buyers have just one OCID."
            },
            buyer_repetition: {
                name: "Buyer repetition",
                description: "",
                description_long: ""
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
                description_long: "Calculates a frequency of occurence of different types of documents. All documents from all phases of contracting process are included. This check passes everytime and serves only for data presentation"
            }
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
            passedExamples: "Passed examples"
        }
    },
    resourceLevel: {
        description: "Resource level checks inspects the data quality from the perspective of a single compiled release. Each check can use various information from the whole compiled release to confirm that the logic of the data is correct. It's possible that one logical rule can be applied several times to a single compiled release because of two reasons <ul><li>the same data structure (e.g. OrganizationReference) can be found under various JSON keys</li><li>there migth be multiple occurences of the same data structure within one array</li></ul>In such case a result of a check is an aggregation of results of all individual checks. The check passes  if all the individual checks pass.",
        subheadline: "All Resource Level Checks",
        ok: "OK",
        failed: "FAILED",
        na: "N/A",
        check: "CHECK",
        count_header: "Checked compiled releases:",
        count_header_tooltip: "Total number of compiled releases in a collection. For each compiled release the check is evaluated right once. It either passes, fails or there are insufficient data, therefore, the result is unavailable. This statistic shows what is the percentage of compiled releases that has problematic data.",
        application_count_header: "Individual checks:",
        application_count_header_tooltip: "One check can consist of multiple individual checks that controls the same logical rule using multiple instances of the same data structure (e.g. multiple suppliers). This statistic shows what is the percentage of passed and failed individual checks.",
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
            }
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
            }
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
            }
        }
    },
    overview: {
        collection_metadata: "Collection Metadata",
        kingfisher_metadata: "Kingfisher Metadata",
        dqt_metadata: "Data Quality Tool Metadata",
        compiled_releases: {
            title: "Compiled Releases",
            value_label: "Total Unique OCIDs"
        },
        prices: {
            title: "Contract Values",
            value_label: "Total Contract Value",
            contracts: "contracts",
            thead: {
                category: "Value range (USD)",
                count: "Contracts count",
                share: "% of total"
            },
            info: "This excludes: contract values with missing amounts, missing currencies, non-numeric amounts and unknown currencies; and contract values occurring in compiled releases whose release date is invalid, before 1999, or in the future."
        },
        period: {
            title: "Release Dates",
            subtitle: "Release Date Distribution",
            description: "The distribution of release dates of all compiled releases."
        },
        lifecycle: {
            title: "Objects per Stage",
            planning: "Planning",
            tender: "Tender",
            award: "Award",
            contract: "Contract",
            implementation: "Implementation",
            info: "In OCDS, data is organized into objects, for each stage of a contracting process. Each compiled release has: at most one Planning object, at most one Tender object, any number of Award objects, and any number of Contract objects. Each Contract object has at most one Implementation object. As such, the number of Award objects can exceed the number of unique OCIDs, but the number of Tender objects can't."
        },
        publisher: "Publisher name",
        datalicense: "License",
        extensions: "Extensions",
        extensionsUnsupported: "Unsupported format",
        publishedFrom: "Published from",
        publishedTo: "Published to",
        collectionId: "Collection ID",
        processingFrom: "Started processing at",
        processingTo: "Finished processing at"
    },
    field: {
        title: "Field Level Checks",
        description: "<p>Field level checks control each field separately without using information from other fields. Each field can be checked on two levels.</p><p>Coverage - presence of a field is checked. Empty field is considered to be missing. Each field can be checked as many times as is the number of occurence of its parent structure. For example, if there is 50k <i>awards</i> in a dataset containing 90k <i>suppliers</i> in total <i>awards.title</i> check can be performed 50.000x but awards.suppliers.id can be performed 90.000x</p><p>Quality - once the field is present additional quality checks like is it a non-negative number or is it a two-letter lowercase ISO639-1 code can be performed. These controls run only for fields that are present in the dataset.</p>",
        all: "ALL CHECKS",
        table: {
            head: {
                object: "OBJECT",
                coverage: "COVERAGE",
                quality: "QUALITY"
            }
        },
        search: "Search object by name",
        hidden: " {n} hidden"
    },
    fieldDetail: {
        checks: "checks",
        path: "Field path",
        coverage: {
            label: "Coverage",
            exists: {
                count_header: "Exists",
                count_header_tooltip: "There can be as many occurences of each field as is the number of occurences of its parent structure. This check inspects that the parent structure has particular JSON key set. For example for field path 'tender.title' it checks whether all 'tender' objects have 'title' key set"
            },
            non_empty: {
                count_header: "Non-Empty",
                count_header_tooltip: "This check is a part of coverage checks and controls whether the particular field does not have empty value. Except null values also empty strings and empty arrays are considered to be empty fields."
            }
        },
        quality: {
            label: "Quality",
            ocid_prefix_check: {
                count_header: "Registered prefix",
                count_header_tooltip: "To pass this check 'ocid' must start with a registered prefix."
            },
            date_time: {
                count_header: "Realistic datetime",
                count_header_tooltip: "To pass this check value of a given field must fulfill the condition 1970-01-01 <= value <= 2050-01-01"
            },
            email: {
                count_header: "Email format",
                count_header_tooltip: "To pass this check value of a given field must be a string with a valid email format"
            },
            identifier_scheme: {
                count_header: "Identifier scheme",
                count_header_tooltip: "To pass this check value of a given field must be a value from org-id.guide scheme list"
            },
            telephone: {
                count_header: "Telephone format",
                count_header_tooltip: "To pass this check value of a given field must be a string with a valid phone format"
            },
            document_description_length: {
                count_header: "Document description length",
                count_header_tooltip: "To pass this check value of a given field must be a string not longer than 250 words"
            },
            document_type: {
                count_header: "Coherent document type",
                count_header_tooltip: "If the 'documentType' value is a code in the extended 'documentType' codelist, and the section for the code is non-empty, then the section must include a section of OCDS document where the document is published"
            },
            document_format_codelist: {
                count_header: "Document format",
                count_header_tooltip: "To pass this check 'format' of the document must be a value from IANA Media Types codelist"
            },
            number_checks: {
                count_header: "Non-negative value",
                count_header_tooltip: "The value of a given must be a non-negative number to pass this check"
            },
            language: {
                count_header: "Two-letter lowercase ISO639-1 code",
                count_header_tooltip: "To pass this check value of a given field must be a two-letter lowercase ISO639-1 code"
            }
        }
    },
    timeLevel: {
        description: "<p>Time-based checks provide an insight into how a particular dataset developed in time. It's based on comparison of compiled releases with the same ocid, therefore, the first and most important check controls that ocids are not disappearing when the dataset is updated. The rest of checks then compares pairs of compiled releases and inspects specific information to asses whether the compiled release changed or not changet in an expected way. Each check consists of two numbers</p><p>Coverage - says what is the percentage of compiled releases from the older dataset appropriate for a particular checks that are also present in a newer version of a dataset</p><p>Check result - says what's the percentage of successfully checked pairs of compiled releases when the specific rule could be applied.</p>",
        checkResult: "Check result",
        coverageResult: "Coverage result",
        subheadline: "All Time Variance Level Checks",
        coverage: {
            header: "Compiled realeases processed:",
            header_tooltip: "This number says how many compiled releases from the older version of the dataset fulfill all conditions so that it can be compared with the newer version. OCID presence is a must have. On top of that, some other conditions might be added. For example 'tender.title' must be set for 'Tender title stability' check. The statistis says how many compiled releases that fullfiled all conditions were also found in the newer version of a dataset so that the final check can be performed.",
            ok: "Included",
            failed: "Not included"
        },
        check: {
            header: "Compiled realease pairs checked:",
            header_tooltip: "This number says how many pairs (old and new) of compiled releases was eventually checked by a given rule (e.g. Tender title stability or Phase stability)",
            ok: "Ok",
            failed: "Failed"
        },
        phase_stable: {
            name: "Phase stability",
            description: "To check that the contracting process has an expected progression existence and counts of <i>planning</i>, <i>tender</i>, <i>awards</i> and <i>contracts</i> is being inspected",
            descriptionLong: "This check controls that each compiled release in the newer version of dataset has the same or higher number of <i>planning</i>, <i>tender</i>, <i>awards</i> and <i>contracts</i> objects than in the older version. If the compiled release with the same ocid is present in both versions of the dataset it checks that:<ul><li><i>planning</i> exists in the new version if it existed in the old version</li><li><i>tender</i> exists in the new version if it existed in the old version</li><li>size of <i>awards</i> in the new version is higher or equal to the size of <i>awards</i> in the old version</li><li>size of <i>contracts</i> in the new version is higher or equal to the size of <i>contracts</i> in the old version</li></ul> The comparison of a pair of compiled releases fails if at least one of the above-described comparisons fails"
        },
        ocid: {
            name: "OCID existence",
            description: "OCID is a globally unique identifier for a contracting process. Once the contracting process is launched and present in a collection it should be always present in all future versions of a collection.",
            descriptionLong: "OCID is a globally unique identifier for a contracting process. Once the contracting process is launched and present in a collection it should be always present in all future versions of a collection. This check takes one by one each ocid from older version of a dataset a controls that it's also present in a newer version of a dataset."
        },
        tender_title: {
            name: "Tender title stability",
            description: "The tender should not be changing its title during the life cycle of the contracting process. This check controls that the <i>tender.title</i> remains the same through the time.",
            descriptionLong: "For all pairs of compiled releases determined by the same <i>ocid</i> in both older and newer version of the same dataset the <i>tender.title</i> field is being compared. Only those compiled realeses that have a <i>tender.title</i> set in the older verion are being taken into consideration. The titles does not need to be necessarily 100% the same, small typos are allowed. Before the comparison all white spaces are removed and values are converted to lower case."
        }
    }
}