import sortMixins from "@/plugins/sortMixins.js";

export default {
    mixins: [sortMixins],
    computed: {
        search: function () {
            return this.searchRaw ? this.searchRaw.toLowerCase() : null;
        },
        searchRaw: function () {
            return this.$store.getters.fieldCheckSearch;
        },
    },
    methods: {
        _sort: function (checks, comparator, sortedBy, asc = true) {
            if (checks != null) {
                this.sort(checks, comparator, asc);
                this.$emit("field-check-table-sort", { by: sortedBy, asc: asc });
            }
        },
        sortBy: function (checks, by, asc) {
            if (by === "path") {
                this.sortByPath(checks, asc);
            } else if (by === "coverage") {
                this.sortByCoverage(checks, asc);
            } else if (by === "quality") {
                this.sortByQuality(checks, asc);
            } else if (by === "processingOrder") {
                this.sortByProcessingOrder(checks, asc);
            }
        },
        sortByPath: function (checks, asc = true) {
            this._sort(checks, (a, b) => a.path.localeCompare(b.path), "path", asc);
        },
        sortByCoverage: function (checks, asc = true) {
            this._sort(
                checks,
                (a, b) => {
                    var comparison = this.compareNumbers(a.coverageOkShare, b.coverageOkShare);
                    if (comparison === 0) {
                        comparison = this.compareNumbers(a.coverage.total_count, b.coverage.total_count);
                    }
                    if (comparison === 0) {
                        comparison = a.path.localeCompare(b.path);
                    }

                    return comparison;
                },
                "coverage",
                asc,
            );
        },
        sortByQuality: function (checks, asc = true) {
            this._sort(
                checks,
                (a, b) => {
                    if (a.quality.total_count === 0) {
                        if (b.quality.total_count === 0) {
                            return a.path.localeCompare(b.path);
                        }

                        return asc ? 1 : -1;
                    } else if (b.quality.total_count === 0) {
                        return asc ? -1 : 1;
                    }

                    var comparison = this.compareNumbers(a.qualityOkShare, b.qualityOkShare);
                    if (comparison === 0) {
                        comparison = this.compareNumbers(a.quality.total_count, b.quality.total_count);
                    }
                    if (comparison === 0) {
                        comparison = a.path.localeCompare(b.path);
                    }

                    return comparison;
                },
                "quality",
                asc,
            );
        },
        sortByProcessingOrder: function (checks, asc = true) {
            this._sort(
                checks,
                (a, b) => this.compareNumbers(a.processing_order, b.processing_order),
                "processingOrder",
                asc,
            );
        },
        highlightSearch: function (path) {
            if (!this.search) {
                return path;
            }

            // escape regex special characters
            var search_esc = this.search.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
            return path.replace(new RegExp(`(${search_esc})`, "ig"), "<mark>$1</mark>");
        },
        highlightSearchLast: function (path) {
            var name = path.substring(path.lastIndexOf(".") + 1);

            if (!this.search || !this.isPathSearched(path)) {
                return name;
            }

            var search_last = this.search.replace(/^[.]+|[.]+$/g, "");
            if (search_last.includes(".")) {
                search_last = search_last.split(".").slice(-1)[0];
            }
            // escape regex special characters
            var search_esc = search_last.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
            return name.replace(new RegExp(`(${search_esc})`, "ig"), "<mark>$1</mark>");
        },
        isPathSearched: function (path) {
            if (this.search && path) {
                var path_lc = path.toLowerCase();
                return path_lc.includes(this.search);
            }

            return true;
        },
    },
};
