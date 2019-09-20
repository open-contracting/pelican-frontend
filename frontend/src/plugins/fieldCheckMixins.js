export default {
    data: function() {
        return {
        };
    },
    methods: {
        sort: function(checks, comparator, sortedBy, asc = true) {
            if (checks != null) {
                checks.sort(comparator)
                if (!asc) {
                    checks.reverse()
                }

                this.$emit('field-check-table-sort', {by: sortedBy, asc: asc})
            }
        },
        sortBy: function(checks, by, asc) {
            if (by == "path") {
                this.sortByPath(checks, asc)
            } else if (by == "coverage") {
                this.sortByCoverage(checks, asc)
            } else if (by == "quality") {
                this.sortByQuality(checks, asc)
            } else if (by == "processingOrder") {
                this.sortByProcessingOrder(checks, asc)
            }
        },
        sortByPath: function(checks, asc = true) {        
            this.sort(checks, (a, b) => a.path.localeCompare(b.path), "path", asc)
        },
        sortByCoverage: function(checks, asc = true) {
            this.sort(checks, (a, b) => {
                var comparison = this.compareNumbers(a.coverageOkShare, b.coverageOkShare)
                if (comparison == 0) {
                    comparison = this.compareNumbers(a.coverage.total_count, b.coverage.total_count)
                }
                if (comparison == 0) {
                    comparison = a.path.localeCompare(b.path)
                }

                return comparison
            }, "coverage", asc)
        },
        sortByQuality: function(checks, asc = true) {            
            this.sort(checks, (a, b) => {
                if (a.quality.total_count == 0) {
                    if (b.quality.total_count == 0) {
                        a.path.localeCompare(b.path)
                    }

                    return asc ? 1 : -1;                        
                }

                var comparison = this.compareNumbers(a.qualityOkShare, b.qualityOkShare)
                if (comparison == 0) {
                    comparison = this.compareNumbers(a.quality.total_count, b.quality.total_count)
                }
                if (comparison == 0) {
                    comparison = a.path.localeCompare(b.path)
                }
                
                return comparison
            }, "quality", asc)
        },
        sortByProcessingOrder: function(checks, asc = true) {
            this.sort(checks, (a, b) => this.compareNumbers(a.processing_order, b.processing_order), "processingOrder", asc)
        },
        compareNumbers: function(a, b) {
            return a - b
        }
    },
};