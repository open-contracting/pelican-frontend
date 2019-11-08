export const messages = {
    header: "Data Quality Assessment Results",
    loader: {
        generic: "Loading… Please be patient.",
        examples: "Generating random examples… This takes some time for large datasets. Please be patient."
    },
    ocid: "ocid",
    ocids: "ocids",
    passed: "Passed",
    failed: "Failed",
    notAvailable: "Not available",
    created: "Created",
    modified: "Modified",
    core: {
        passedExamples: "Sample of successes",
        failedExamples: "Sample of failures",
        undefinedExamples: "Sample of unprocessed data"
    },
    kingfisherId: "Kingfisher ID",
    dataset: {
        id: "ID",
        name: "Name",
        size: "Count",
        phase: "Status",
        selectDataset: "Show",
        search: "Search report by name",
        timeVariance: "Time-based checks"
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
        ocds_data: "Data Preview"
    },
    examples: {
        failed: "Sample releases with failed rules",
        passed: "Sample releases with passed rules",
        actions: "Actions",
        preview: "Preview",
        previewOld: "Preview old",
        previewNew: "Preview new",
        ocid: "ocid",
        showMore: "Show more examples",
        showLess: "Show fewer examples"
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
        description: "<p>These checks operate on individual compiled releases; each compiled release is analyzed in isolation. There are three types of checks:</p><ul><li><p><b>Coherence</b>: The data makes sense and is possible. <i>Example</i>: A start date that is after an end date is incoherent.</p></li><li><p><b>Consistency</b>: If the value of one field implies the value of another field, the values should be identical or commensurate. <i>Examples</i>: The entry in the <code>parties</code> array that is referenced from the <code>buyer</code> field should have 'buyer' in its <code>roles</code> array; the monetary value of an award should be commensurate with the monetary values of its related contracts.</p></li><li><p><b>Reference</b>: A reference field has a valid target. <i>Examples</i>: Every <code>awardID<code> in every contract matches the <code>id</code> of an award; every <code>buyer.id</code> matches the <code>id</code> of a party.</p></li><p>A check is 'N/A' if the relevant fields are not set. <i>Example</i>: If the <code>contracts.awardID</code> field is not set, then the reference check is not run.</p>",
        subheadline: "All Resource-Level Checks",
        ok: "Passed",
        failed: "Failed",
        na: "N/A",
        check: "Check",
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
                name: "Realistic value",
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
                name: "Buyer organization reference",
                description: "<code>buyer.id</code> is present and matches the <code>id</code> of a party."
            },
            payee_in_parties: {
                name: "Payee organization reference",
                description: "Every <code>contracts[].implementation.transactions[].payee.id</code> is present and matches the <code>id</code> of a party."
            },
            payer_in_parties: {
                name: "Payer organization reference",
                description: "Every <code>contracts[].implementation.transactions[].payer.id</code> is present and matches the <code>id</code> of a party."
            },
            procuring_entity_in_parties: {
                name: "Procuring entity organization reference",
                description: "<code>tender.procuringEntity.id</code> is present and matches the <code>id</code> of a party."
            },
            supplier_in_parties: {
                name: "Supplier organization references",
                description: "Each <code>awards[].suppliers[].id</code> is present and matches the <code>id</code> of a party."
            },
            tenderer_in_parties: {
                name: "Tenderer organization references",
                description: "Each <code>tender.tenderers[].id</code> is present and matches the <code>id</code> of a party."
            },
            contract_in_awards: {
                name: "Award reference",
                description: "Each <code>contracts[].awardID</code> is present and matches the <code>awardID</code> of exactly one award. The test is skipped if there are no awards."
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
            info: "This excludes: contract values with missing amounts, missing currencies, non-numeric amounts, negative amounts, and unknown currencies; and contract values occurring in compiled releases whose release date is invalid, before 1999, or in the future. To determine the number of excluded contract values, compare the number of contracts here to the number of objects in the contract stage, above."
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
        collectionId: "Compiled Collection ID",
        processingFrom: "Started processing at",
        processingTo: "Finished processing at"
    },
    field: {
        title: "Field-Level Checks",
        description: "<p>These checks operate on individual fields within compiled releases; each occurrence of each field is analyzed in isolation. There are two types of checks:</p><ul><li><p><b>Coverage:</b> There is one check per field in the release schema. If a field is set, and its value is neither null nor empty (whether it is an object, array or string), then the coverage test passes.</p><p>If a field is on an object in an array, then the coverage test is run for each object in the array. <i>Example</i>: There are 100 compiled releases, all of which have 5 parties. The check for the <code>parties</code> field will be reported out of 100, but the checks for its child fields (like <code>parties.id</code>) will be reported out of 500.</p><p>Child fields are reported in the context of their parent field. <i>Example</i>: There are 100 compiled releases, 10 of which set <code>tender</code>. The check for the <code>tender</code> field will be reported out of 100, but the checks for its child fields (like <code>tender.id</code>) will be reported out of 10.</p></li><li><p><b>Quality:</b> If there is a quality check for the field, and if the coverage test passes, then the quality test is run. The quality checks differ per field, and are described in detail on sub-pages. <i>Examples</i>: <code>ocid</code> value has a registered prefix; release date is in the past.</p></li></ul>",
        all: "All Field-Level Checks",
        table: {
            head: {
                object: "Field path",
                coverage: "Coverage",
                quality: "Quality"
            }
        },
        search: "Search field by name",
        hidden: " {n} hidden"
    },
    fieldDetail: {
        checked: "checked",
        path: "Field path",
        coverage: {
            label: "Coverage",
            exists: {
                count_header: "Field is set",
                count_header_tooltip: "There is one test per <i>possible</i> occurrence of the field. <i>Example</i>: If the parent <code>tender</code> field is set in 10 compiled releases, then the child <code>tender.id</code> field is reported out of 10. If there are 100 entries across all <code>awards</code> arrays in all compiled releases, then the <code>awards.id</code> field is reported out of 100."
            },
            non_empty: {
                count_header: "Field isn't null or empty",
                count_header_tooltip: "There is one test per <i>actual</i> occurrence of the field. The test passes if the field value is neither null nor empty (i.e. it is not an empty string, empty array or empty object). See the above check for other details."
            }
        },
        quality: {
            label: "Quality",
            ocid_prefix_check: {
                count_header: "OCID prefix is registered",
                count_header_tooltip: "The value is a string and starts with a registered OCID prefix."
            },
            date_time: {
                count_header: "Date is realistic",
                count_header_tooltip: "The value is a string, starts in YYYY-MM-DD format, isn't before 1970 and isn't after 2050."
            },
            email: {
                count_header: "Email address is valid",
                count_header_tooltip: "The value is a valid address according to RFC 2822."
            },
            identifier_scheme: {
                count_header: "Identifier scheme is recognized",
                count_header_tooltip: "The value is a string and is an org-id.guide code."
            },
            telephone: {
                count_header: "Phone number is possible",
                count_header_tooltip: "The value is a possible number according to Google's libphonenumber."
            },
            document_description_length: {
                count_header: "Has 250 characters or less",
                count_header_tooltip: "The length of the value is less than or equal to 250."
            },
            document_type: {
                count_header: "Document type is coherent",
                count_header_tooltip: "The document type is appropriate to the field path. Specifically, the value is a documentType code, and the code's 'Section' corresponds to the field's path."
            },
            document_format_codelist: {
                count_header: "Document format is recognized",
                count_header_tooltip: "The value is a string and is either an IANA Media Type or the 'offline/print' code."
            },
            number_checks: {
                count_header: "Number is non-negative",
                count_header_tooltip: "The value isn't a complex number, can be parsed as a floating-point number, and is non-negative."
            },
            language: {
                count_header: "Language code is recognized",
                count_header_tooltip: "The value is a string and is a two-letter, lowercase, ISO 639-1 code."
            }
        }
    },
    timeLevel: {
        description: "<p>These checks focus on changes within a dataset over time. Each check has two steps:</p><ul><li><b>Find pairs:</b> The compiled releases in the older collection are filtered according to check-specific criteria, and then each is attempted to be paired with a compiled release with the same OCID in the newer collection. If no pair is found, this test fails. <i>Example</i>: The buyer should be invariant across time. If an older release sets the <code>buyer</code> field (thereby satisfying the check's criterion), then it is attempted to be paired with a newer release.</li><li><b>Check pairs:</b> Once a pair is found, the check is run. <i>Example</i>: The buyer should be invariant across time. If the two releases have different values for the <code>buyer</code> field, this test fails.</li></ul>",
        checkResult: "Pairs passed",
        coverageResult: "Pairs found",
        subheadline: "All Time-Based Checks",
        coverage: {
            header: "Finding compiled release pairs:",
            header_tooltip: "The compiled releases in the older collection are filtered according to check-specific criteria, and then each is attempted to be paired with a compiled release with the same OCID in the newer collection. If no pair is found, this test fails. <i>Example</i>: The buyer should be invariant across time. If an older release sets the <code>buyer</code> field (thereby satisfying the check's criterion), then it is attempted to be paired with a newer release.",
            ok: "Found",
            failed: "Not found"
        },
        check: {
            header: "Checking compiled release pairs:",
            header_tooltip: "Once a pair is found, the check is run. <i>Example</i>: The buyer should be invariant across time. If the two releases have different values for the <code>buyer</code> field, this test fails.",
            ok: "Passed",
            failed: "Failed"
        },
        phase_stable: {
            name: "Stage stability",
            description: "A compiled release in the newer collection should have at least the same number of <code>planning</code>, <code>tender</code>, <code>awards</code> and <code>contracts</code> objects as its pair in the older collection.",
            descriptionLong: "A compiled release in the newer collection should have at least the same number of <code>planning</code>, <code>tender</code>, <code>awards</code> and <code>contracts</code> objects as its pair in the older collection."
        },
        ocid: {
            name: "OCID persistence",
            description: "All OCIDs in an older collection of a data source should be present in this newer collection of the same source.",
            descriptionLong: "<p>All OCIDs in an older collection of a data source should be present in this newer collection of the same source.</p><p>This check always has the same results for pairs found and pairs passed, because no further tests are run in the latter step.</p>"
        },
        tender_title: {
            name: "Tender title stability",
            description: "The tender title should be invariant across time.",
            descriptionLong: "<p>The tender title should be invariant across time.</p><p>If an older compiled release sets the <code>tender.title</code> field, then it is attempted to be paired with a newer compiled release. If the lowercased, whitespace-normalized values of the two <code>tender.title</code> fields in the two compiled releases are equal, the test passes.</p>"
        }
    }
}