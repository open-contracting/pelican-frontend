import { describe, expect, it } from "vitest";
import { shareStyle, useBarChart } from "@/composables/useBarChart.js";
import { mountComposable, testI18n } from "@/test/helpers.js";

describe("shareStyle", () => {
  it("colors a share within the check's thresholds as passing, inclusively", () => {
    expect(shareStyle(0.4, [0.4, 0.6])).toBe("color: #919C03");
    expect(shareStyle(0.6, [0.4, 0.6])).toBe("color: #919C03");
    expect(shareStyle(0.39, [0.4, 0.6])).toBe("color: #d0021b");
    expect(shareStyle(0.61, [0.4, 0.6])).toBe("color: #d0021b");
  });
});

describe("useBarChart", () => {
  const bars = () => [
    { key: "datasetLevel.charts.label_1", share: 0.5, count: 10 },
    { key: "datasetLevel.charts.label_2_20", share: 0.2, count: 5 },
  ];

  it("builds a header and, per bar, the translated label, share, annotation, and first-bar-only style", () => {
    const { chartData } = mountComposable(() => useBarChart({ ticks: [0, 0.4], showCount: true }, bars), [testI18n()]);

    expect(chartData.value).toEqual([
      ["Group", "Share", { role: "annotation" }, { role: "style" }],
      ["1", 0.5, "50% (10)", "color: #d0021b"],
      ["2 - 20", 0.2, "20% (5)", ""],
    ]);
  });

  it("annotates with the share alone, without showCount", () => {
    const { chartData } = mountComposable(() => useBarChart({ ticks: [0, 0.6] }, bars), [testI18n()]);

    expect(chartData.value[1]).toEqual(["1", 0.5, "50%", "color: #919C03"]);
  });
});
