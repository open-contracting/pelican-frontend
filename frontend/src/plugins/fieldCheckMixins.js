export default {
    data: function() {
        return {
        };
    },
    methods: {
        sort: function(comparator, sortedBy, asc = true) {
            if (this.stats != null) {
                this.stats.sort(comparator)
                if (!asc) {
                    this.stats.reverse()
                }

                this.$emit('field-check-table-sort', {by: sortedBy, asc: asc})
            }
        },
        sortBy: function(by, asc) {
            if (by == "path") {
                this.sortByPath(asc)
            } else if (by == "coverage") {
                this.sortByCoverage(asc)
            } else if (by == "quality") {
                this.sortByQuality(asc)
            } else if (by == "processingOrder") {
                this.sortByProcessingOrder(asc)
            }
        },
        sortByPath: function(asc = true) {        
            this.sort((a, b) => a.path.localeCompare(b.path), "path", asc)
        },
        sortByCoverage: function(asc = true) {
            this.sort((a, b) => {
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
        sortByQuality: function(asc = true) {            
            this.sort((a, b) => {
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
        sortByProcessingOrder: function(asc = true) {
            this.sort((a, b) => this.compareNumbers(a.processing_order, b.processing_order), "processingOrder", asc)
        },
        compareNumbers: function(a, b) {
            return a - b
        }
    },
};