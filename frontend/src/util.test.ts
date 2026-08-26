import { describe, expect, it } from "vitest";
import type { FieldLevelCheck } from "@/types.js";
import { fieldCheckTree, orderedShares, withoutExamples } from "@/util.js";

describe("orderedShares", () => {
  it("orders entries by count, largest first", () => {
    const shares = { a: { count: 1 }, b: { count: 3 }, c: { count: 2 } };

    expect(orderedShares(shares)).toEqual([
      ["b", { count: 3 }],
      ["c", { count: 2 }],
      ["a", { count: 1 }],
    ]);
  });

  it("keeps insertion order between equal counts", () => {
    const shares = { late: { count: 1 }, early: { count: 1 } };

    expect(orderedShares(shares).map(([key]) => key)).toEqual(["late", "early"]);
  });

  it("returns an empty list for no shares", () => {
    expect(orderedShares({})).toEqual([]);
  });
});

describe("withoutExamples", () => {
  it("returns primitives and null unchanged", () => {
    expect(withoutExamples(5)).toBe(5);
    expect(withoutExamples("x")).toBe("x");
    expect(withoutExamples(true)).toBe(true);
    expect(withoutExamples(null)).toBeNull();
  });

  it("removes each example key, at any depth", () => {
    const value = {
      examples: [1],
      passed_examples: [2],
      failed_examples: [3],
      value: 1,
      shares: { USD: { count: 1, examples: [{ item_id: 1 }] } },
    };

    expect(withoutExamples(value)).toEqual({ value: 1, shares: { USD: { count: 1 } } });
  });

  it("recurses into arrays", () => {
    const value = [{ examples: [1], count: 1 }, [{ passed_examples: [], share: 0.5 }]];

    expect(withoutExamples(value)).toEqual([{ count: 1 }, [{ share: 0.5 }]]);
  });

  it("keeps keys that only resemble example keys", () => {
    expect(withoutExamples({ examples2: [1], my_examples: [2] })).toEqual({ examples2: [1], my_examples: [2] });
  });
});

describe("fieldCheckTree", () => {
  const check = (path: string) => ({ path }) as FieldLevelCheck;
  const segments = (node?: { children: Map<string, unknown> }) => [...(node?.children.keys() ?? [])];

  it("nests the checks by the segments of their paths", () => {
    const tree = fieldCheckTree([check("tender"), check("tender.items"), check("tender.items.id")]);

    expect(segments(tree)).toEqual(["tender"]);
    const tender = tree.children.get("tender");
    expect(tender?.check?.path).toBe("tender");
    expect(segments(tender)).toEqual(["items"]);
    expect(tender?.children.get("items")?.children.get("id")?.check?.path).toBe("tender.items.id");
  });

  it("creates the ancestors that no check occupies", () => {
    const tree = fieldCheckTree([check("tender.items.id")]);

    const tender = tree.children.get("tender");
    expect(tender?.check).toBeUndefined();
    expect(tender?.children.get("items")?.check).toBeUndefined();
    expect(tender?.children.get("items")?.children.get("id")?.check?.path).toBe("tender.items.id");
  });

  it("keeps the checks in the order given, at every depth", () => {
    const tree = fieldCheckTree([check("planning.budget"), check("awards"), check("planning.rationale")]);

    expect(segments(tree)).toEqual(["planning", "awards"]);
    expect(segments(tree.children.get("planning"))).toEqual(["budget", "rationale"]);
  });

  it("returns an empty tree for no checks", () => {
    expect(fieldCheckTree([]).children.size).toBe(0);
  });
});
