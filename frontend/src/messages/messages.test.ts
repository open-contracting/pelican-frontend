import { describe, expect, it } from "vitest";
import en from "./en.json";
import es from "./es.json";

function keysOf(catalog: object, prefix = ""): string[] {
  return Object.entries(catalog).flatMap(([key, value]) =>
    value !== null && typeof value === "object" ? keysOf(value, `${prefix}${key}.`) : [`${prefix}${key}`],
  );
}

describe("message catalogs", () => {
  it("declare the same keys in every language", () => {
    expect(keysOf(es).sort()).toEqual(keysOf(en).sort());
  });
});
