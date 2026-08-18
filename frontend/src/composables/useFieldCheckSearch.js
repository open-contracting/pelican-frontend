import { computed } from "vue";
import { useStore } from "vuex";

export function useFieldCheckSearch() {
  const store = useStore();

  const searchRaw = computed(() => store.getters.fieldCheckSearch);
  const search = computed(() => searchRaw.value?.toLowerCase());

  function comparator(by, asc) {
    if (by === "path") {
      return (a, b) => a.path.localeCompare(b.path);
    }

    if (by === "coverage") {
      return (a, b) => {
        let comparison = a.coverageOkRatio - b.coverageOkRatio;
        if (comparison === 0) {
          comparison = a.coverage.total_count - b.coverage.total_count;
        }
        if (comparison === 0) {
          comparison = a.path.localeCompare(b.path);
        }
        return comparison;
      };
    }

    if (by === "quality") {
      // Checks without a quality score sort last, whichever direction the rest sort in.
      return (a, b) => {
        if (a.quality.total_count === 0) {
          if (b.quality.total_count === 0) {
            return a.path.localeCompare(b.path);
          }
          return asc ? 1 : -1;
        }
        if (b.quality.total_count === 0) {
          return asc ? -1 : 1;
        }

        let comparison = a.qualityOkRatio - b.qualityOkRatio;
        if (comparison === 0) {
          comparison = a.quality.total_count - b.quality.total_count;
        }
        if (comparison === 0) {
          comparison = a.path.localeCompare(b.path);
        }
        return comparison;
      };
    }

    return (a, b) => a.processing_order - b.processing_order;
  }

  function sorted(checks, by, asc = true) {
    if (checks == null) {
      return [];
    }

    const compare = comparator(by, asc);
    return [...checks].sort((a, b) => (asc ? compare(a, b) : compare(b, a)));
  }

  function setSorting(by, asc = true) {
    store.commit("setFieldCheckSorting", { by, asc });
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
    sorted,
    setSorting,
    highlightSearch,
    highlightSearchLast,
    isPathSearched,
  };
}
