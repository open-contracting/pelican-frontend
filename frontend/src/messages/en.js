export const messages = {
    header: "Data Quality Assessment Results",
    loader: {
        generic: "Loading… Please be patient.",
        examples: "Generating random examples… This takes some time for large datasets. Please be patient.",
        data: "Loading data preview. Please be patient.",
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
        undefinedExamples: "Sample of unprocessed data",
    },
    kingfisherId: "Kingfisher ID",
    dataset: {
        id: "ID",
        name: "Name",
        size: "Count",
        phase: "Status",
        selectDataset: "Show",
        search: "Search report by name",
        timeVariance: "Time-based checks",
        filter: "filter",
        actions: "actions",
        comparsion: "comparsion",
    },
    datasetFilter: {
        headline: "Dataset filtering",
        submit: "Filter",
        items: "selected",
        itemsAll: "criteria will not limit the parent dataset",
        submitResultOk: "Ok",
        submitResultFailed: "Failed",
        releaseDateFromTo: "Release date from - to",
        releaseDateFrom: "Release date from",
        releaseDateTo: "Release date to",
        buyerName: "Buyer name",
        procuringEntityName: "Procuring entity name",
        buyerNameRegex: "Buyer name",
        buyerNameRegexTooltip: "Standard SQL ILIKE pattern",
        procuringEntityNameRegex: "Procuring entity name",
        procuringEntityNameRegexTooltip: "Standard SQL ILIKE pattern",
        statusOk: "Calculation will start in a moment.",
    },
    datasetReport: {
        headline: "Dataset report",
        statusOk: "Report has been successfully created.",
        link: "Link: ",
        statusFailed: "Report creation failed.",
        documentId: "Document id",
        documentIdTooltip: "Id or url of document containing some report tags",
        folderId: "Folder id",
        folderIdTooltip: "Id or url of folder for the final report",
        submit: "Submit"

    },
    datasetValuesMultiselect: {
        noResult: "No values found. Consider changing the search query.",
        limitText: " more selected",
    },
    insufficientData: {
        title: "Insufficient data",
        description: "Data was insufficient to calculate the check.",
    },
    sections: {
        home: "Home",
        overview: "Overview",
        field: "Field",
        resource: "Compiled release",
        dataset: "Collection",
        time: "Time",
    },
    preview: {
        metadata: "Metadata",
        ocds_data: "Data Preview",
        cannot_display: "The JSON data cannot be previewed, because its large size (more than 3,000 lines) can cause some browsers to crash. You can download the JSON file, instead.",
    },
    examples: {
        failed: "Sample releases with failed rules",
        passed: "Sample releases with passed rules",
        downloads: "Download",
        download_json: "JSON",
        actions: "Actions",
        preview: "Preview",
        previewOld: "Preview old",
        previewNew: "Preview new",
        ocid: "ocid",
        showMore: "Show more examples",
        showLess: "Show fewer examples",
    },
    navigationContextMenu: {
        openNewTab: "Open in New Tab",
        openNewWindow: "Open in New Window",
        copyToClipboard: "Copy to Clipboard",
    },
    datasetLevel: {
        description: "<p>These checks operate on a collection: all compiled releases from a given source at a single point in time. There are five types of checks:</p><ul><li><p><b>Distribution</b>: The distribution of a field's values suggests no omissions or inaccuracies. <i>Examples</i>: If all <code>procurementMethod</code> fields have a value of 'open', then the collection either omits or misreports non-open methods; if all <code>tender.status</code> fields have a value of 'active', then the collection either omits or misreports non-active statuses.</p></li><li><p><b>Repetition</b>: The repetition of a field's values suggests no data entry or mapping issues. <i>Examples</i>: If the contract value is zero 10% of the time, there might be a data mapping issue; if the award value is $25,000 10% of the time, there might be a data entry issue.</p></li><li><p><b>Uniqueness</b>: A field's values are unique across the collection.</p></li><li><p><b>Availability</b>: A random sample of URL values return no responses with HTTP error codes.</p></li><li><p><b>Related processes</b>: A related process reference field has a valid target within the collection, and its <code>title</code> is consistent with the target's <code>tender.title</code>.</p></li></ul><p>Some checks report distributions, but don't pass or fail; for example, the distribution of document types has no pass-fail criterion.</p><p>Some of these checks might, in principle, serve as red flags. The difference is that red flags are more sensitive. These checks have higher thresholds for failure; i.e. the data needs to be not only suspect (mild outliers) but <i>bad</i> (extreme outlier).</p>",
        subheadline: "All Collection-Level Checks",
        label_0_1: "top 1%",
        label_1_5: "top 1-5%",
        label_5_20: "top 5-20%",
        label_20_50: "top 20-50%",
        label_50_100: "last 50%",
        label_1: "1",
        label_2_20: "2 - 20",
        label_21_50: "21 - 50",
        label_51_100: "51 - 100",
        label_100: "100+",
        examples: "Examples",
        from: "from",
        insufficientShown: "Hide not calculated checks",
        insufficientHidden: "Show not calculated checks",
        sections: {
            status_distribution: "Status distribution",
            value_distribution: "Value distribution",
            other_distribution: "Other distribution",
            repetition: "Repetition",
            other: "Other",
        },
        distribution: {
            tender_status: {
                name: "Tender status distribution",
                description: "Visualizes the distribution of <code>tender.status</code> values. The 'active' and 'complete' codes each occur in between 1% and 99% of cases.",
                description_long: "<p>Visualizes the distribution of <code>tender.status</code> values. The 'active' and 'complete' codes each occur in between 1% and 99% of cases.</p><p>The test is skipped if the field is never present. The codelist is closed.</p>",
            },
            contracts_value_repetition: {
                name: "Contracts value repetition",
                description: "Lists the 5 most frequent pairs of <code>contracts.value.amount</code> and <code>contracts.value.currency</code>. The 3 most frequent pairs appear in fewer than 10% of cases.",
                description_long: "<p>Lists the 5 most frequent pairs of <code>contracts.value.amount</code> and <code>contracts.value.currency</code>. The 3 most frequent pairs appear in fewer than 10% of cases.</p><p>The test is skipped if ther are no pairs.</p>",
            },
            awards_value_repetition: {
                name: "Awards value repetition",
                description: "Lists the 5 most frequent pairs of <code>awards.value.amount</code> and <code>awards.value.currency</code>. The 3 most frequent pairs appear in fewer than 10% of cases.",
                description_long: "<p>Lists the 5 most frequent pairs of <code>awards.value.amount</code> and <code>awards.value.currency</code>. The 3 most frequent pairs appear in fewer than 10% of cases.</p><p>The test is skipped if ther are no pairs.</p>",
            },
            tender_value_repetition: {
                name: "Tender value repetition",
                description: "Lists the 5 most frequent pairs of <code>tender.value.amount</code> and <code>tender.value.currency</code>. The 3 most frequent pairs appear in fewer than 10% of cases.",
                description_long: "<p>Lists the 5 most frequent pairs of <code>tender.value.amount</code> and <code>tender.value.currency</code>. The 3 most frequent pairs appear in fewer than 10% of cases.</p><p>The test is skipped if ther are no pairs.</p>",
            },
            buyer: {
                name: "Buyer distribution",
                description: "Fewer than 50% of all buyers are identified in only one compiled release. Failure indicates issues in buyer identification.",
                description_long: "<p>Fewer than 50% of all buyers are identified in only one compiled release. Failure indicates issues in buyer identification. Buyers are identified by <code>buyer.identifier.scheme</code> and <code>buyer.identifier.id</code>. For illustration purposes, the share of all buyers identified in other numbers of compiled releases is shown.</p><p>The test is skipped if the <code>buyer.identifier.scheme</code> and <code>buyer.identifier.id</code> fields are both present in fewer than 1,000 compiled releases.</p>",
            },
            buyer_repetition: {
                name: "Buyer repetition",
                description: "The most common buyer is identified in 1% to 50% of compiled releases. Failure indicates issues in buyer identification or buyer over-representation.",
                description_long: "<p>The most common buyer is identified in 1% to 50% of compiled releases. Failure indicates issues in buyer identification or buyer over-representation. Buyers are identified by <code>buyer.identifier.scheme</code> and <code>buyer.identifier.id</code>.</p><p>The test is skipped if the <code>buyer.identifier.scheme</code> and <code>buyer.identifier.id</code> fields are both present in fewer than 1,000 compiled releases.</p>",
            },
            tender_value: {
                name: "Tender value distribution",
                description: "The sum of the top 1% of tender values doesn't exceed 50% of the sum of all tender values. Failure indicates extreme outliers in the top 1%.",
                description_long: "<p>The sum of the top 1% of tender values doesn't exceed 50% of the sum of all tender values. Failure indicates extreme outliers in the top 1%. All values are converted to USD as of the compiled release's <code>date</code>. For illustration purposes, the shares of other ranges of values are shown.</p><p>The test is skipped if fewer than 100 values are included. A value is excluded if an amount is missing or non-numeric, if a currency is missing or unknown, or if currency conversion is necessary and the release date is invalid, before 1999, or in the future.</p>",
            },
            awards_value: {
                name: "Awards value distribution",
                description: "The sum of the top 1% of award values doesn't exceed 50% of the sum of all award values. Failure indicates extreme outliers in the top 1%.",
                description_long: "<p>The sum of the top 1% of award values doesn't exceed 50% of the sum of all award values. Failure indicates extreme outliers in the top 1%. All values are converted to USD as of the compiled release's <code>date</code>. For illustration purposes, the shares of other ranges of values are shown.</p><p>The test is skipped if fewer than 100 values are included. A value is excluded if an amount is missing or non-numeric, if a currency is missing or unknown, or if currency conversion is necessary and the release date is invalid, before 1999, or in the future.</p>",
            },
            contracts_value: {
                name: "Contracts value distribution",
                description: "The sum of the top 1% of contract values doesn't exceed 50% of the sum of all contract values. Failure indicates extreme outliers in the top 1%.",
                description_long: "<p>The sum of the top 1% of contract values doesn't exceed 50% of the sum of all contract values. Failure indicates extreme outliers in the top 1%. All values are converted to USD as of the compiled release's <code>date</code>. For illustration purposes, the shares of other ranges of values are shown.</p><p>The test is skipped if fewer than 100 values are included. A value is excluded if an amount is missing or non-numeric, if a currency is missing or unknown, or if currency conversion is necessary and the release date is invalid, before 1999, or in the future.</p>",
            },
            main_procurement_category: {
                name: "Main procurement category distribution",
                description: "Visualizes the distribution of <code>tender.mainProcurementCategory</code> values. No code occurs in more than 95% of cases.",
                description_long: "<p>Visualizes the distribution of <code>tender.mainProcurementCategory</code> values. No code occurs in more than 95% of cases.</p><p>The test is skipped if the field is never present. The codelist is closed.</p>",
            },
            tender_procurement_method: {
                name: "Procurement method distribution",
                description: "Visualizes the distribution of <code>tender.procurementMethod</code> values. The 'open' code occurs in between 1% and 99% of cases.",
                description_long: "<p>Visualizes the distribution of <code>tender.procurementMethod</code> values. The 'open' code occurs in between 1% and 99% of cases.</p><p>The test is skipped if the field is never present. The codelist is closed.</p>",
            },
            tender_award_criteria: {
                name: "Award criteria distribution",
                description: "Visualizes the distribution of <code>tender.awardCriteria</code> values. No test is performed.",
                description_long: "<p>Visualizes the distribution of <code>tender.awardCriteria</code> values. No test is performed.</p><p>The codelist is open.</p>",
            },
            tender_submission_method: {
                name: "Submission method distribution",
                description: "Visualizes the distribution of <code>tender.submissionMethod</code> values. No test is performed.",
                description_long: "<p>Visualizes the distribution of <code>tender.submissionMethod</code> values. No test is performed.</p><p>The codelist is open.</p>",
            },
            awards_status: {
                name: "Award status distribution",
                description: "Visualizes the distribution of <code>awards.status</code> values. The 'active' code occurs in between 1% and 99% of cases.",
                description_long: "<p>Visualizes the distribution of <code>awards.status</code> values. The 'active' code occurs in between 1% and 99% of cases.</p><p>The test is skipped if the field is never present. The codelist is closed.</p>",
            },
            contracts_status: {
                name: "Contract status distribution",
                description: "Visualizes the distribution of <code>contracts.status</code> values. The 'active' and 'terminated' codes each occur in between 1% and 99% of cases.",
                description_long: "<p>Visualizes the distribution of <code>contracts.status</code> values. The 'active' and 'terminated' codes each occur in between 1% and 99% of cases.</p><p>The test is skipped if the field is never present. The codelist is closed.</p>",
            },
            milestone_status: {
                name: "Milestone status distribution",
                description: "Visualizes the distribution of milestone <code>status</code> values. The 'met' code occurs in between 1% and 99% of cases.",
                description_long: "<p>Visualizes the distribution of milestone <code>status</code> values. The 'met' code occurs in between 1% and 99% of cases. The milestone fields are:</p><ul><li><code>planning.milestones.status</code></li><li><code>tender.milestones.status</code></li><li><code>awards.milestones.status</code></li><li><code>contracts.implementation.milestones.status</code></li></ul><p>The test is skipped if the field is never present. The codelist is closed.</p>",
            },
            milestone_type: {
                name: "Milestone type distribution",
                description: "Visualizes the distribution of milestone <code>type</code> values. No test is performed.",
                description_long: "<p>Visualizes the distribution of milestone <code>type</code> values. No test is performed. The milestone fields are:</p><ul><li><code>planning.milestones.type</code></li><li><code>tender.milestones.type</code></li><li><code>awards.milestones.type</code></li><li><code>contracts.implementation.milestones.type</code></li></ul><p>The codelist is open.</p>",
            },
            value_currency: {
                name: "Currency distribution",
                description: "Visualizes the distribution of <code>currency</code> values. No test is performed.",
                description_long: "<p>Visualizes the distribution of <code>currency</code> values. No test is performed. The fields are:</p><ul><li><code>planning.budget.value.currency</code></li><li><code>tender.value.currency</code></li><li><code>tender.minValue.currency</code></li><li><code>awards.value.currency</code></li><li><code>contracts.value.currency</code></li><li><code>contracts.implementation.transactions.value.currency</code></li></ul><p>The codelist is closed.</p>",
            },
            related_process_relation: {
                name: "Related process relation distribution",
                description: "Visualizes the distribution of <code>relatedProcesses.relationship</code> values. No test is performed.",
                description_long: "<p>Visualizes the distribution of <code>relatedProcesses.relationship</code> values. No test is performed.</p><p>The codelist is open.</p>",
            },
            document_document_type: {
                name: "Document type distribution",
                description: "Visualizes the distribution of document <code>documentType</code> values. No test is performed.",
                description_long: "<p>Visualizes the distribution of document <code>documentType</code> values. No test is performed. The document fields are:</p><ul><li><code>planning.documents.documentType</code></li><li><code>tender.documents.documentType</code></li><li><code>awards.documents.documentType</code></li><li><code>contracts.documents.documentType</code></li><li><code>contracts.implementation.documents.documentType</code></li></ul><p>The codelist is open.</p>",
            }
        },
        unique: {
            ok: "All values are unique.",
            failed: "Not all values are unique.",
            id: {
                name: "id",
                description: "Please ignore until further notice.",
            },
        },
        misc: {
            url_availability: {
                name: "URL availability",
                description: "A random sample of 100 URL values return no responses with HTTP error codes.",
                description_long: "A random sample of 100 URL values return no responses with HTTP error codes. The URL fields are: <ul><li><code>planning.documents.url</code></li><li><code>tender.documents.url</code></li><li><code>awards.documents.url</code></li><li><code>contracts.documents.url</code></li></ul>",
            },
        },
        consistent: {
            related_process_title: {
                name: "Tender's title is consistent",
                description: "A related process object has the same value for its <code>title</code> field as the <code>tender.title</code> field of the compiled release it references.",
                description_long: "A related process object has the same value for its <code>title</code> field as the <code>tender.title</code> field of the compiled release it references. The related process fields are: <ul><li><code>contracts.relatedProcesses</code></li><li><code>relatedProcesses</code></li></ul>",
            },
        },
        reference: {
            related_process_identifier: {
                name: "Related process reference",
                description: "If a related process has a <code>scheme</code> of 'ocid' and its <code>identifier</code> is present, then its <code>identifier</code> matches the <code>ocid</code> of a compiled release.",
                description_long: "If a related process has a <code>scheme</code> of 'ocid' and its <code>identifier</code> is present, then its <code>identifier</code> matches the <code>ocid</code> of a compiled release. The related process fields are: <ul><li><code>contracts.relatedProcesses</code></li><li><code>relatedProcesses</code></li></ul>",
            },
        },
        numeric: {
            passed: "passed",
            processed: "tested",
            failed: "failed",
            failedExamples: "Failed examples",
            passedExamples: "Passed examples",
        },
        top3: {
            value: "Value",
            share: "Share",
            count: "Occurrences",
        },
    },
    resourceLevel: {
        description: "<p>These checks operate on individual compiled releases; each compiled release is analyzed in isolation. There are three types of checks:</p><ul><li><p><b>Coherence</b>: The data makes sense and is possible. <i>Example</i>: A start date that is after an end date is incoherent.</p></li><li><p><b>Consistency</b>: If the value of one field implies the value of another field, the values should be identical or commensurate. <i>Examples</i>: The entry in the <code>parties</code> array that is referenced from the <code>buyer</code> field should have 'buyer' in its <code>roles</code> array; the monetary value of an award should be commensurate with the monetary values of its related contracts.</p></li><li><p><b>Reference</b>: A reference field has a valid target. <i>Examples</i>: Every <code>awardID</code> in every contract matches the <code>id</code> of an award; every <code>buyer.id</code> matches the <code>id</code> of a party.</p></li><li><p>A check is 'N/A' if the relevant fields are not set; any other reasons to skip a test are noted for each check. <i>Example</i>: If the <code>contracts.awardID</code> field is not set, then the reference check is not run.</p></li></ul>",
        subheadline: "All Compiled Release-Level Checks",
        ok: "Passed",
        failed: "Failed",
        na: "N/A",
        check: "Check",
        count_header: "Compiled releases checked:",
        count_header_tooltip: "Each compiled release is checked, and either it passes, it fails or the check is inapplicable.",
        application_count_header: "Individual tests performed:",
        application_count_header_tooltip: "One 'check' can be made up of many 'tests'; for example, when checking whether start dates aren't after end dates, each pair of start dates and end dates is <i>tested</i>. This shows the proportion of tests that passed or failed, instead of the proportion of compiled releases that passed or failed.",
        coherent: {
            categoryName: "Coherence",
            period: {
                name: "Start dates aren't after end dates",
                description: "<p>For each period, <code>startDate</code> is less than or equal to <code>endDate</code>.</p><p>Since the test operates on all period objects, the test silently ignores any dates that can't be parsed.</p>",
            },
            procurement_method_vs_number_of_tenderers: {
                name: "At most one tenderer for sole sourcing",
                description: "If the <code>tender.procurementMethod</code> is 'direct', then the <code>tender.numberOfTenderers</code> is at most 1.",
            },
            tender_status: {
                name: "No awards or contracts for incomplete tenders",
                description: "If <code>tender.status</code> is incomplete ('planning', 'planned', 'active', 'cancelled', 'unsuccessful' or 'withdrawn'), then <code>awards</code> and <code>contracts</code> are blank.",
            },
            awards_status: {
                name: "No contracts for inactive awards",
                description: "If an award's <code>status</code> is inactive ('pending', 'cancelled', 'unsuccessful'), then no contract's <code>awardID</code> matches the award's <code>id</code>.",
            },
            contracts_status: {
                name: "No transactions for unsigned contracts",
                description: "If a contract's <code>status</code> is unsigned ('pending' or 'cancelled'), then its <code>implementation.transactions</code> is blank.",
            },
            milestone_status: {
                name: "No date met for unmet milestones",
                description: "If a milestone's <code>status</code> is unmet ('scheduled' or 'notMet'), then its <code>dateMet</code> is blank.",
            },
            value_realistic: {
                name: "Monetary values are realistic",
                description: "<p>Each monetary value is between -5 billion USD and +5 billion USD.</p><p>Since the test operates on all value objects, the test silently ignores any missing or non-numeric amounts and any missing or unknown currencies. If currency conversion is necessary, but the release date is invalid, before 1999, or in the future, the test silently ignores the value.</p>",
            },
            dates: {
                name: "Contracting process timeline",
                description: "<p>All dates relating to stages of the contracting process follow a coherent timeline.</p><ul><li><code>tender.tenderPeriod.endDate <= tender.contractPeriod.startDate</code>: The last day for submissions isn't after the contract's anticipated start date.</li><li><code>tender.tenderPeriod.endDate <= awards[].date</code>: The last day for submissions isn't after an award's date.</li><li><code>tender.tenderPeriod.endDate <= contracts[].dateSigned</code>: The last day for submissions isn't after a contract's signature date.</li><li><code>awards[i].date <= contracts[].dateSigned</code>: An award's date isn't after the signature date of any of its related contracts.</li><li><code>contracts[].dateSigned <= contracts[].implementation.transactions[].date</code>: A contract's signature date isn't after the date of any of its related transactions.</li></ul><p>Also, each award's <code>date</code> and each contract's <code>dateSigned</code> aren't after the release date.<p><p>Since the test operates on multiple dates, the test silently ignores any dates that can't be parsed.</p>",
            },
            milestones_dates: {
                name: "Milestone dates",
                description: "<p>For each milestone, <code>dateModified</code> and <code>dateMet</code> aren't after the release date.</p><p>Since the test operates on all milestone objects, the test silently ignores any dates that can't be parsed.</p>",
            },
            amendments_dates: {
                name: "Amendment dates",
                description: "<p>For each amendment, <code>date</code> isn't after the release date, and: a tender amendment's <code>date</code> isn't before the <code>tenderPeriod</code>; an award amendment's <code>date</code> isn't before the award's <code>date</code>; a contract amendment's <code>date</code> isn't before the contract's <code>dateSigned</code>.</p><p>Since the test operates on all amendment objects, the test silently ignores any dates that can't be parsed.</p>",
            },
            documents_dates: {
                name: "Document dates",
                description: "<p>For each document, <code>datePublished</code> and <code>dateModified</code> aren't after the release date, and <code>datePublished</code> isn't after <code>dateModified</code>.</p><p>Since the test operates on all document objects, the test silently ignores any dates that can't be parsed.</p>",
            },
        },
        consistent: {
            categoryName: "Consistency",
            number_of_tenderers: {
                name: "Number of tenderers is consistent",
                description: "<p>The value of the <code>numberOfTenderers</code> field is equal to the number of entries in the <code>tenderers</code> array.</p><p>The test is skipped if the <code>tenderers</code> field is not an array.</p>",
            },
            tender_value: {
                name: "Planning budget is commensurate with tender value",
                description: "<p><code>planning.budget.amount</code> isn't less than 50%, or more than 150%, of <code>tender.value</code>, after conversion to USD if necessary.</p><p>The test is skipped if an amount is missing, zero or non-numeric, if a currency is missing or unknown, if the two amounts aren't both positive or both negative, or if currency conversion is necessary and the release date is invalid, before 1999, or in the future.</p>",
            },
            contracts_value: {
                name: "Contract values are commensurate with award value",
                description: "<p>For each award, the sum of its contract's values isn't less than 50%, or more than 150%, of the award's value, after conversion to USD if necessary.</p><p>Since the test operates on all award and contract values, the test silently ignores any contract whose <code>awardID</code> doesn't match the <code>id</code> of exactly one award, if an amount is missing, zero or non-numeric, if a currency is missing or unknown, if the two amounts aren't both positive or both negative, or if currency conversion is necessary and the release date is invalid, before 1999, or in the future.</p>",
            },
            contracts_implementation_transactions_value: {
                name: "Transaction values are commensurate with contract value",
                description: "<p>For each contract, the sum of its transaction's values is less than or equal to the contract's value, after conversion to USD if necessary.</p><p>Since the test operates on all contract and transaction objects, the test silently ignores any missing or non-numeric amounts and any missing or unknown currencies. If currency conversion is necessary, but the release date is invalid, before 1999, or in the future, the test silently ignores the contract and its transactions.</p>",
            },
            parties_roles: {
                name: "Parties are referenced",
                description: "<p>For each role of each party, there is a referencing object. <i>Example</i>: If a party has the roles 'supplier' and 'payee', it is referenced by at least one award's <code>suppliers</code> entry and at least one transaction's <code>payee</code> field. The roles to test are:</p><ul><li>procuringEntity</li><li>tenderer</li><li>supplier</li><li>payer</li><li>payee</li></ul><p>The 'buyer' role is not tested, because there can be multiple buyers in the <code>parties</code> array, but there is only one <code>buyer</code> field for the primary buyer.</p><p>Since the test operates on all organization objects, the test silently ignores any party whose <code>id</code> field is missing, as it cannot be referenced.</p>",
            },
            period_duration_in_days: {
                name: "Period's duration is consistent with start and end dates",
                description: "<p>For each period, <code>durationInDays</code> is equal to the difference between <code>startDate</code> and <code>endDate</code>. If <code>endDate</code> is blank or unparseable, then <code>durationInDays</code> is equal to the difference between <code>startDate</code> and <code>maxExtentDate</code>.</p><p>Since the test operates on all period objects, the test silently ignores any dates that can't be parsed.</p>",
            },
            buyer_in_parties_roles: {
                name: "Buyer's role is set",
                description: "The party referenced by the <code>buyer</code> field has 'buyer' in its <code>roles</code> array.",
            },
            supplier_in_parties_roles: {
                name: "Supplier's role is set",
                description: "Each party referenced by a <code>awards[].suppliers</code> entry has 'supplier' in its <code>roles</code> array.",
            },
            tenderer_in_parties_roles: {
                name: "Tenderer's role is set",
                description: "Each party referenced by a <code>tender.tenderers</code> entry has 'tenderer' in its <code>roles</code> array.",
            },
            procuring_entity_in_parties_roles: {
                name: "Procuring entity's role is set",
                description: "The party referenced by the <code>tender.procuringEntity</code> field has 'procuringEntity' in its <code>roles</code> array.",
            },
            payer_in_parties_roles: {
                name: "Payer's role is set",
                description: "Each party referenced by a <code>contracts[].implementation.transactions[].payer</code> field has 'payer' in its <code>roles</code> array.",
            },
            payee_in_parties_roles: {
                name: "Payee's role is set",
                description: "Each party referenced by a <code>contracts[].implementation.transactions[].payee</code> field has 'payee' in its <code>roles</code> array.",
            },
            buyer_name_in_parties: {
                name: "Buyer's name is consistent",
                description: "<p>The <code>buyer</code> field has the same value for its <code>name</code> field as the party it references.</p><p>The test is skipped if the referencing <code>id</code> is missing or if it doesn't match the <code>id</code> of exactly one party.</p>",
            },
            payee_name_in_parties: {
                name: "Payee's name is consistent",
                description: "<p>Each <code>contracts[].implementation.transactions[].payee</code> field has the same value for its <code>name</code> field as the party it references.</p><p>The test is skipped if every referencing <code>id</code> is missing or if none matches the <code>id</code> of exactly one party.</p>",
            },
            payer_name_in_parties: {
                name: "Payer's name is consistent",
                description: "<p>Each <code>contracts[].implementation.transactions[].payer</code> field has the same value for its <code>name</code> field as the party it references.</p><p>The test is skipped if every referencing <code>id</code> is missing or if none matches the <code>id</code> of exactly one party.</p>",
            },
            procuring_entity_name_in_parties: {
                name: "Procuring entity's name is consistent",
                description: "<p>The <code>tender.procuringEntity</code> field has the same value for its <code>name</code> field as the party it references.</p><p>The test is skipped if the referencing <code>id</code> is missing or if it doesn't match the <code>id</code> of exactly one party.</p>",
            },
            supplier_name_in_parties: {
                name: "Supplier's name is consistent",
                description: "<p>Each <code>awards[].suppliers</code> entry has the same value for its <code>name</code> field as the party it references.</p><p>The test is skipped if every referencing <code>id</code> is missing or if none matches the <code>id</code> of exactly one party.</p>",
            },
            tenderer_name_in_parties: {
                name: "Tenderer's name is consistent",
                description: "<p>Each <code>tender.tenderers</code> entry has the same value for its <code>name</code> field as the party it references.</p><p>The test is skipped if every referencing <code>id</code> is missing or if none matches the <code>id</code> of exactly one party.</p>",
            },
        },
        reference: {
            categoryName: "Reference",
            buyer_in_parties: {
                name: "Buyer organization reference",
                description: "<code>buyer.id</code> is present and matches the <code>id</code> of exactly one party.",
            },
            payee_in_parties: {
                name: "Payee organization reference",
                description: "Every <code>contracts[].implementation.transactions[].payee.id</code> is present and matches the <code>id</code> of exactly one party.",
            },
            payer_in_parties: {
                name: "Payer organization reference",
                description: "Every <code>contracts[].implementation.transactions[].payer.id</code> is present and matches the <code>id</code> of exactly one party.",
            },
            procuring_entity_in_parties: {
                name: "Procuring entity organization reference",
                description: "<code>tender.procuringEntity.id</code> is present and matches the <code>id</code> of exactly one party.",
            },
            supplier_in_parties: {
                name: "Supplier organization references",
                description: "Each <code>awards[].suppliers[].id</code> is present and matches the <code>id</code> of exactly one party.",
            },
            tenderer_in_parties: {
                name: "Tenderer organization references",
                description: "Each <code>tender.tenderers[].id</code> is present and matches the <code>id</code> of exactly one party.",
            },
            contract_in_awards: {
                name: "Award reference",
                description: "<p>Each <code>contracts[].awardID</code> is present and matches the <code>awardID</code> of exactly one award.</p><p>The test is skipped if there are no awards.</p>",
            },
        },
    },
    overview: {
        collection_metadata: "Collection Metadata",
        kingfisher_metadata: "Kingfisher Metadata",
        dqt_metadata: "Data Quality Tool Metadata",
        compiled_releases: {
            title: "Compiled Releases",
            value_label: "Total Unique OCIDs",
        },
        prices: {
            title: "Contract Values",
            value_label: "Total Contract Value",
            contracts: "contracts",
            thead: {
                category: "Value range (USD)",
                count: "Contracts count",
                share: "% of total",
            },
            info: "All values are converted to USD as of the compiled release's <code>date</code>. This excludes: contract values with missing amounts, missing currencies, non-numeric amounts, negative amounts, and unknown currencies; and contract values occurring in compiled releases whose release date is invalid, before 1999, or in the future. To determine the number of excluded contract values, compare the number of contracts here to the number of objects in the contract stage, above."
        },
        period: {
            title: "Release Dates",
            subtitle: "Release Date Distribution",
            description: "The distribution of release dates of all compiled releases.",
        },
        filtered: {
            title: "Filtered from",
            info: "This dataset has been filtered from previously calculated dataset.",
            original: "Original dataset",
        },
        lifecycle: {
            title: "Objects per Stage",
            planning: "Planning",
            tender: "Tender",
            award: "Award",
            contract: "Contract",
            implementation: "Implementation",
            info: "In OCDS, data is organized into objects, for each stage of a contracting process. Each compiled release has: at most one Planning object, at most one Tender object, any number of Award objects, and any number of Contract objects. Each Contract object has at most one Implementation object. As such, the number of Award objects can exceed the number of unique OCIDs, but the number of Tender objects can't.",
        },
        publisher: "Publisher name",
        datalicense: "License",
        extensions: "Extensions",
        extensionsUnsupported: "Unsupported format",
        publishedFrom: "Published from",
        publishedTo: "Published to",
        collectionId: "Compiled Collection ID",
        processingFrom: "Started processing at",
        processingTo: "Finished processing at",
        kingfisher_processingFrom: "Started collecting at",
        kingfisher_processingTo: "Finished compiling at",
    },
    field: {
        title: "Field-Level Checks",
        description: "<p>These checks operate on individual fields within compiled releases; each occurrence of each field is analyzed in isolation. There are two types of checks:</p><ul><li><p><b>Coverage:</b> There is one check per field in the release schema. If a field is set, and its value is neither null nor empty (whether it is an object, array or string), then the coverage test passes.</p><p>If a field is on an object in an array, then the coverage test is run for each object in the array. <i>Example</i>: There are 100 compiled releases, all of which have 5 parties. The check for the <code>parties</code> field will be reported out of 100, but the checks for its child fields (like <code>parties.id</code>) will be reported out of 500.</p><p>Child fields are reported in the context of their parent field. <i>Example</i>: There are 100 compiled releases, 10 of which set <code>tender</code>. The check for the <code>tender</code> field will be reported out of 100, but the checks for its child fields (like <code>tender.id</code>) will be reported out of 10.</p></li><li><p><b>Quality:</b> If there is a quality check for the field, and if the coverage test passes, then the quality test is run. The quality checks differ per field, and are described in detail on sub-pages. <i>Examples</i>: <code>ocid</code> value has a registered prefix; release date is in the past.</p></li></ul>",
        all: "All Field-Level Checks",
        table: {
            head: {
                object: "Field path",
                coverage: "Coverage",
                quality: "Quality",
            },
        },
        search: "Search field by name",
        hidden: " {n} hidden",
    },
    fieldDetail: {
        checked: "checked",
        path: "Field path",
        coverage: {
            label: "Coverage",
            exists: {
                count_header: "Field is set",
                count_header_tooltip: "There is one test per <i>possible</i> occurrence of the field. <i>Example</i>: If the parent <code>tender</code> field is set in 10 compiled releases, then the child <code>tender.id</code> field is reported out of 10. If there are 100 entries across all <code>awards</code> arrays in all compiled releases, then the <code>awards.id</code> field is reported out of 100.",
            },
            non_empty: {
                count_header: "Field isn't null or empty",
                count_header_tooltip: "There is one test per <i>actual</i> occurrence of the field. The test passes if the field value is neither null nor empty (i.e. it is not an empty string, empty array or empty object). See the above check for other details.",
            },
        },
        quality: {
            label: "Quality",
            ocid_prefix_check: {
                count_header: "OCID prefix is registered",
                count_header_tooltip: "The value is a string and starts with a registered OCID prefix.",
            },
            date_time: {
                count_header: "Date is realistic",
                count_header_tooltip: "The value is a string, starts in YYYY-MM-DD format, isn't before 1970 and isn't after 2050.",
            },
            email: {
                count_header: "Email address is valid",
                count_header_tooltip: "The value is a valid address according to RFC 2822.",
            },
            identifier_scheme: {
                count_header: "Identifier scheme is recognized",
                count_header_tooltip: "The value is a string and is an org-id.guide code. (The codelist is open.)"
            },
            telephone: {
                count_header: "Phone number is possible",
                count_header_tooltip: "The value is a possible number according to Google's libphonenumber.",
            },
            document_description_length: {
                count_header: "Has 250 characters or less",
                count_header_tooltip: "The length of the value is less than or equal to 250.",
            },
            document_type: {
                count_header: "Document type is coherent",
                count_header_tooltip: "The document type is appropriate to the field path. Specifically, the value is a documentType code, and the code's 'Section' corresponds to the field's path. (The codelist is open.)"
            },
            document_format_codelist: {
                count_header: "Document format is recognized",
                count_header_tooltip: "The value is a string and is either an IANA Media Type or the 'offline/print' code. (The codelist is open.)"
            },
            number_checks: {
                count_header: "Number is non-negative",
                count_header_tooltip: "The value isn't a complex number, can be parsed as a floating-point number, and is non-negative.",
            },
            language: {
                count_header: "Language code is recognized",
                count_header_tooltip: "The value is a string and is a two-letter, lowercase, ISO 639-1 code. (The codelist is open.)"
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
            failed: "Not found",
        },
        check: {
            header: "Checking compiled release pairs:",
            header_tooltip: "Once a pair is found, the check is run. <i>Example</i>: The buyer should be invariant across time. If the two releases have different values for the <code>buyer</code> field, this test fails.",
            ok: "Passed",
            failed: "Failed",
        },
        phase_stable: {
            name: "Stage stability",
            description: "A compiled release in the newer collection should have at least the same number of <code>planning</code>, <code>tender</code>, <code>awards</code> and <code>contracts</code> objects as its pair in the older collection.",
            descriptionLong: "A compiled release in the newer collection should have at least the same number of <code>planning</code>, <code>tender</code>, <code>awards</code> and <code>contracts</code> objects as its pair in the older collection.",
        },
        ocid: {
            name: "OCID persistence",
            description: "All OCIDs in an older collection of a data source should be present in this newer collection of the same source.",
            descriptionLong: "<p>All OCIDs in an older collection of a data source should be present in this newer collection of the same source.</p><p>This check always has the same results for pairs found and pairs passed, because no further tests are run in the latter step.</p>",
        },
        tender_title: {
            name: "Tender title stability",
            description: "The tender title should be invariant across time.",
            descriptionLong: "<p>The tender title should be invariant across time.</p><p>If an older compiled release sets the <code>tender.title</code> field, then it is attempted to be paired with a newer compiled release. If the lowercased, whitespace-normalized values of the two <code>tender.title</code> fields in the two compiled releases are equal, the test passes.</p>",
        },
    },
};