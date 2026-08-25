import { computed } from "vue";
import { useUiStore } from "@/stores/ui.js";
import type { FieldLevelCheck } from "@/types.js";

/** A slice of a field's path, marked if the search matches it. */
export interface PathSegment {
  text: string;
  matched: boolean;
}

const unmatched = (text: string): PathSegment[] => [{ text, matched: false }];

/** Split ``text`` around each occurrence of the lowercase ``search``, marking the occurrences. */
function markMatches(text: string, search: string): PathSegment[] {
  const lower = text.toLowerCase();
  const segments: PathSegment[] = [];
  let start = 0;

  for (let index = lower.indexOf(search); index !== -1; index = lower.indexOf(search, start)) {
    if (index > start) {
      segments.push({ text: text.slice(start, index), matched: false });
    }
    segments.push({ text: text.slice(index, index + search.length), matched: true });
    start = index + search.length;
  }
  if (start < text.length) {
    segments.push({ text: text.slice(start), matched: false });
  }

  return segments;
}

export function useFieldCheckSearch() {
  const ui = useUiStore();

  const searchRaw = computed(() => ui.fieldCheckSearch);
  const search = computed(() => searchRaw.value?.toLowerCase());

  function comparator(by: string, asc: boolean) {
    if (by === "path") {
      return (a: FieldLevelCheck, b: FieldLevelCheck) => a.path.localeCompare(b.path);
    }

    if (by === "coverage") {
      return (a: FieldLevelCheck, b: FieldLevelCheck) => {
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
      return (a: FieldLevelCheck, b: FieldLevelCheck) => {
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

    return (a: FieldLevelCheck, b: FieldLevelCheck) => a.processing_order - b.processing_order;
  }

  function sorted(checks: FieldLevelCheck[] | null | undefined, by: string, asc = true) {
    if (checks == null) {
      return [];
    }

    const compare = comparator(by, asc);
    return [...checks].sort((a, b) => (asc ? compare(a, b) : compare(b, a)));
  }

  function setSorting(by: string, asc = true) {
    ui.fieldCheckSorting = { by, asc };
  }

  function highlightSearch(path: string): PathSegment[] {
    if (!search.value) {
      return unmatched(path);
    }
    return markMatches(path, search.value);
  }

  function highlightSearchLast(path: string): PathSegment[] {
    const name = path.substring(path.lastIndexOf(".") + 1);

    if (!search.value || !isPathSearched(path)) {
      return unmatched(name);
    }

    // Only the search's last segment can match the path's last segment.
    const last = search.value.split(".").filter(Boolean).at(-1);
    if (!last) {
      return unmatched(name);
    }
    return markMatches(name, last);
  }

  function isPathSearched(path: string) {
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
