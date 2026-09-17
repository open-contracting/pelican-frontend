import { describe, expect, it } from "vitest";
import { useFormatters } from "@/composables/useFormatters.js";
import { mountComposable, testI18n } from "@/test/helpers.js";

function formatters(locale = "en") {
  const i18n = testI18n();
  i18n.global.locale.value = locale as "en" | "es";
  return { i18n, ...mountComposable(() => useFormatters(), [i18n]) };
}

describe("formatNumber", () => {
  it("groups digits in the reader's language", () => {
    expect(formatters("en").formatNumber(12047)).toBe("12,047");
    expect(formatters("es").formatNumber(12047)).toBe("12.047");
  });

  it("rounds to an integer", () => {
    expect(formatters().formatNumber(12047.6)).toBe("12,048");
  });

  it("passes undefined through, for absent counts", () => {
    expect(formatters().formatNumber(undefined)).toBeUndefined();
  });

  it("reformats when the reader switches language", () => {
    const { i18n, formatNumber } = formatters("en");

    expect(formatNumber(12047)).toBe("12,047");
    i18n.global.locale.value = "es";
    expect(formatNumber(12047)).toBe("12.047");
  });
});

describe("formatPercentage", () => {
  it("rounds a ratio to a whole percentage", () => {
    const { formatPercentage } = formatters();

    expect(formatPercentage(0)).toBe("0%");
    expect(formatPercentage(0.25)).toBe("25%");
    expect(formatPercentage(0.005)).toBe("1%");
    expect(formatPercentage(1)).toBe("100%");
  });

  it("reports a share that rounds to 0% without being 0% as short of it", () => {
    expect(formatters().formatPercentage(0.004)).toBe(">0%");
  });

  it("reports a share that rounds to 100% without being 100% as short of it", () => {
    expect(formatters().formatPercentage(0.996)).toBe("<100%");
  });
});

describe("formatPercentage2D", () => {
  it("rounds a ratio to two decimals, in the reader's language, with the sign attached", () => {
    expect(formatters("en").formatPercentage2D(0.123456)).toBe("12.35%");
    expect(formatters("es").formatPercentage2D(0.123456)).toBe("12,35%");
  });

  it("keeps exact bounds exact", () => {
    const { formatPercentage2D } = formatters();

    expect(formatPercentage2D(0)).toBe("0.00%");
    expect(formatPercentage2D(1)).toBe("100.00%");
  });

  it("reports near-0% and near-100% shares as short of them", () => {
    const { formatPercentage2D } = formatters();

    expect(formatPercentage2D(0.0000049)).toBe(">0.00%");
    expect(formatPercentage2D(0.9999999)).toBe("<100.00%");
  });
});
