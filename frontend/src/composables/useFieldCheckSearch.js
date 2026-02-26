import { computed } from "vue";
import { useStore } from "vuex";

export function useFieldCheckSearch() {
    const store = useStore();

    const searchRaw = computed(() => store.getters.fieldCheckSearch);
    const search = computed(() => searchRaw.value?.toLowerCase());

    function _sort(checks, comparator, sortedBy, asc = true) {
        if (checks != null) {
            checks.sort((a, b) => (asc ? comparator(a, b) : comparator(b, a)));
            store.commit("setFieldCheckSorting", { by: sortedBy, asc: asc });
        }
    }

    function sortBy(checks, by, asc) {
        if (by === "path") {
            sortByPath(checks, asc);
        } else if (by === "coverage") {
            sortByCoverage(checks, asc);
        } else if (by === "quality") {
            sortByQuality(checks, asc);
        } else if (by === "processingOrder") {
            sortByProcessingOrder(checks, asc);
        }
    }

    function sortByPath(checks, asc = true) {
        _sort(checks, (a, b) => a.path.localeCompare(b.path), "path", asc);
    }

    function sortByCoverage(checks, asc = true) {
        _sort(
            checks,
            (a, b) => {
                let comparison = a.coverageOkShare - b.coverageOkShare;
                if (comparison === 0) {
                    comparison = a.coverage.total_count - b.coverage.total_count;
                }
                if (comparison === 0) {
                    comparison = a.path.localeCompare(b.path);
                }
                return comparison;
            },
            "coverage",
            asc,
        );
    }

    function sortByQuality(checks, asc = true) {
        _sort(
            checks,
            (a, b) => {
                if (a.quality.total_count === 0) {
                    if (b.quality.total_count === 0) {
                        return a.path.localeCompare(b.path);
                    }
                    return asc ? 1 : -1;
                }
                if (b.quality.total_count === 0) {
                    return asc ? -1 : 1;
                }

                let comparison = a.qualityOkShare - b.qualityOkShare;
                if (comparison === 0) {
                    comparison = a.quality.total_count - b.quality.total_count;
                }
                if (comparison === 0) {
                    comparison = a.path.localeCompare(b.path);
                }
                return comparison;
            },
            "quality",
            asc,
        );
    }

    function sortByProcessingOrder(checks, asc = true) {
        _sort(checks, (a, b) => a.processing_order - b.processing_order, "processingOrder", asc);
    }

    function highlightSearch(path) {
        if (!search.value) {
            return path;
        }
        // escape regex special characters
        const search_esc = search.value.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
        return path.replace(new RegExp(`(${search_esc})`, "ig"), "<mark>$1</mark>");
    }

    function highlightSearchLast(path) {
        const name = path.substring(path.lastIndexOf(".") + 1);

        if (!search.value || !isPathSearched(path)) {
            return name;
        }

        let search_last = search.value.replace(/^[.]+|[.]+$/g, "");
        if (search_last.includes(".")) {
            search_last = search_last.split(".").slice(-1)[0];
        }
        // escape regex special characters
        const search_esc = search_last.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
        return name.replace(new RegExp(`(${search_esc})`, "ig"), "<mark>$1</mark>");
    }

    function isPathSearched(path) {
        return !search.value || !path || path.toLowerCase().includes(search.value);
    }

    return {
        search,
        searchRaw,
        sortBy,
        sortByPath,
        sortByCoverage,
        sortByQuality,
        sortByProcessingOrder,
        highlightSearch,
        highlightSearchLast,
        isPathSearched,
    };
}
