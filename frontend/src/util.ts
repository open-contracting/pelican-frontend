import { EXAMPLE_KEYS } from "@/config.js";

export function orderedShares<T extends { count: number }>(shares: Record<string, T>): [string, T][] {
  const items: [string, T][] = Object.keys(shares).map((key) => [key, shares[key]]);
  items.sort((first, second) => second[1].count - first[1].count);
  return items;
}

export function withoutExamples(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(withoutExamples);
  }
  if (value !== null && typeof value === "object") {
    const result: Record<string, unknown> = {};
    for (const [key, entry] of Object.entries(value)) {
      if (!EXAMPLE_KEYS.has(key)) {
        result[key] = withoutExamples(entry);
      }
    }
    return result;
  }
  return value;
}
