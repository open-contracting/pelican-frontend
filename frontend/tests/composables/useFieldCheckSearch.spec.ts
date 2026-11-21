import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it } from "vitest";
import { useFieldCheckSearch } from "@/composables/useFieldCheckSearch.js";
import { useUiStore } from "@/stores/ui.js";
import type { FieldLevelCheck } from "@/types.js";

interface CheckOptions {
  coverage?: [number, number];
  quality?: [number, number];
  order?: number;
}

/** A check whose groups pass ``passed`` of ``total`` times, with the ratios as the store derives them. */
function check(path: string, { coverage = [1, 1], quality = [1, 1], order = 0 }: CheckOptions = {}): FieldLevelCheck {
  const group = ([passed, total]: [number, number]) => ({
    passed_count: passed,
    failed_count: total - passed,
    total_count: total,
    checks: {},
  });
  const ratio = ([passed, total]: [number, number]) => (total === 0 ? 0 : passed / total);

  return {
    path,
    processing_order: order,
    examples_filled: false,
    coverage: group(coverage),
    quality: group(quality),
    coverageOkRatio: ratio(coverage),
    coverageFailedRatio: ratio([coverage[1] - coverage[0], coverage[1]]),
    qualityOkRatio: ratio(quality),
    qualityFailedRatio: ratio([quality[1] - quality[0], quality[1]]),
  };
}

const paths = (checks: FieldLevelCheck[]) => checks.map((item) => item.path);

beforeEach(() => {
  setActivePinia(createPinia());
});

describe("sorted", () => {
  it("returns an empty list for absent stats", () => {
    const { sorted } = useFieldCheckSearch();

    expect(sorted(null, "path")).toEqual([]);
    expect(sorted(undefined, "path")).toEqual([]);
  });

  it("sorts by path in either direction, without mutating the input", () => {
    const { sorted } = useFieldCheckSearch();
    const checks = [check("planning"), check("awards"), check("tender")];

    expect(paths(sorted(checks, "path"))).toEqual(["awards", "planning", "tender"]);
    expect(paths(sorted(checks, "path", false))).toEqual(["tender", "planning", "awards"]);
    expect(paths(checks)).toEqual(["planning", "awards", "tender"]);
  });

  it("sorts by coverage ratio, breaking ties by total count and then path", () => {
    const { sorted } = useFieldCheckSearch();
    const checks = [
      check("high", { coverage: [4, 5] }),
      check("low", { coverage: [1, 5] }),
      check("low-small", { coverage: [1, 5] }),
      check("low-large", { coverage: [2, 10] }),
    ];

    expect(paths(sorted(checks, "coverage"))).toEqual(["low", "low-small", "low-large", "high"]);
  });

  it("sorts by quality ratio, with unscored checks last in both directions", () => {
    const { sorted } = useFieldCheckSearch();
    const checks = [
      check("zero", { quality: [0, 0] }),
      check("high", { quality: [4, 4] }),
      check("also-zero", { quality: [0, 0] }),
      check("low", { quality: [1, 4] }),
    ];

    expect(paths(sorted(checks, "quality"))).toEqual(["low", "high", "also-zero", "zero"]);
    expect(paths(sorted(checks, "quality", false))).toEqual(["high", "low", "zero", "also-zero"]);
  });

  it("sorts by processing order otherwise", () => {
    const { sorted } = useFieldCheckSearch();
    const checks = [check("b", { order: 2 }), check("a", { order: 3 }), check("c", { order: 1 })];

    expect(paths(sorted(checks, "anything"))).toEqual(["c", "b", "a"]);
  });
});

describe("isPathSearched", () => {
  it("matches every path without a search", () => {
    expect(useFieldCheckSearch().isPathSearched("tender.items")).toBe(true);
  });

  it("matches case-insensitively", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = "ITEMS";

    expect(composable.isPathSearched("tender.items")).toBe(true);
    expect(composable.isPathSearched("awards.value")).toBe(false);
  });

  it("matches an empty path, whatever the search", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = "items";

    expect(composable.isPathSearched("")).toBe(true);
  });
});

const plain = (text: string) => ({ text, matched: false });
const marked = (text: string) => ({ text, matched: true });

describe("highlightSearch", () => {
  it("returns the path unmarked without a search", () => {
    expect(useFieldCheckSearch().highlightSearch("tender.items")).toEqual([plain("tender.items")]);
  });

  it("marks each match, case-insensitively, keeping the path's case", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = "TenDer";

    expect(composable.highlightSearch("tender.items")).toEqual([marked("tender"), plain(".items")]);
    expect(composable.highlightSearch("Tender.tender")).toEqual([marked("Tender"), plain("."), marked("tender")]);
  });

  it("treats regex special characters in the search as literal", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = ".";

    expect(composable.highlightSearch("a.b")).toEqual([plain("a"), marked("."), plain("b")]);
  });
});

describe("highlightSearchLast", () => {
  it("returns the path's last segment unmarked without a search", () => {
    expect(useFieldCheckSearch().highlightSearchLast("tender.items.id")).toEqual([plain("id")]);
  });

  it("marks the last segment of the search within the last segment of the path", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = "items.id";

    expect(composable.highlightSearchLast("tender.items.id")).toEqual([marked("id")]);
  });

  it("ignores the search's leading dots", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = ".id";

    expect(composable.highlightSearchLast("tender.items.id")).toEqual([marked("id")]);
  });

  it("leaves the segment unmarked when a trailing dot keeps the search from matching the path", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = ".id.";

    expect(composable.highlightSearchLast("tender.items.id")).toEqual([plain("id")]);
  });

  it("leaves the segment unmarked when the search matches an earlier segment only", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = "tender";

    expect(composable.highlightSearchLast("tender.items.id")).toEqual([plain("id")]);
  });

  it("leaves the segment unmarked when the search matches nothing", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = "awards";

    expect(composable.highlightSearchLast("tender.items.id")).toEqual([plain("id")]);
  });

  it("marks a partial match within a path without dots", () => {
    const composable = useFieldCheckSearch();
    useUiStore().fieldCheckSearch = "ten";

    expect(composable.highlightSearchLast("tender")).toEqual([marked("ten"), plain("der")]);
  });
});
