import { describe, expect, it } from "vitest";
import { orderedShares, withoutExamples } from "@/util.js";

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
