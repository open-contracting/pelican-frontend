import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it } from "vitest";
import { useUiStore } from "@/stores/ui.js";
import type { FieldLevelCheck } from "@/types.js";

const stats = (...paths: string[]) => paths.map((path) => ({ path }) as FieldLevelCheck);

beforeEach(() => {
  setActivePinia(createPinia());
});

describe("expanding and collapsing", () => {
  it("collapses a node together with its whole subtree", () => {
    const ui = useUiStore();
    ui.expandFieldCheck("tender");
    ui.expandFieldCheck("tender.items");
    ui.expandFieldCheck("awards");

    ui.collapseFieldCheck("tender");

    expect(ui.isFieldCheckExpanded("tender")).toBe(false);
    expect(ui.isFieldCheckExpanded("tender.items")).toBe(false);
    expect(ui.isFieldCheckExpanded("awards")).toBe(true);
  });

  it("collapses a sibling that extends the collapsed node's name", () => {
    const ui = useUiStore();
    ui.expandFieldCheck("tender");
    ui.expandFieldCheck("tenderers");

    ui.collapseFieldCheck("tender");

    expect(ui.isFieldCheckExpanded("tenderers")).toBe(false);
  });
});

describe("setExpandedNodesForSearch", () => {
  it("expands the ancestors of a match, not the match itself", () => {
    const ui = useUiStore();
    ui.fieldCheckSearch = "c";

    ui.setExpandedNodesForSearch(stats("a", "a.b", "a.b.c"));

    expect(ui.fieldCheckExpandedNodes).toEqual(new Set(["a", "a.b"]));
  });

  it("keeps a match collapsed when its whole subtree matches through it", () => {
    const ui = useUiStore();
    ui.fieldCheckSearch = "tender";

    ui.setExpandedNodesForSearch(stats("tender", "tender.items", "awards"));

    expect(ui.fieldCheckExpandedNodes).toEqual(new Set());
  });

  it("expands just enough to reveal the topmost match", () => {
    const ui = useUiStore();
    ui.fieldCheckSearch = "items";

    ui.setExpandedNodesForSearch(stats("tender", "tender.items", "tender.items.id", "awards"));

    expect(ui.fieldCheckExpandedNodes).toEqual(new Set(["tender"]));
  });

  it("collapses everything without a search", () => {
    const ui = useUiStore();
    ui.expandFieldCheck("tender");
    ui.fieldCheckSearch = null;

    ui.setExpandedNodesForSearch(stats("tender", "tender.items"));

    expect(ui.fieldCheckExpandedNodes).toEqual(new Set());
  });

  it("keeps the expanded nodes when the stats are not loaded", () => {
    const ui = useUiStore();
    ui.expandFieldCheck("tender");
    ui.fieldCheckSearch = "items";

    ui.setExpandedNodesForSearch(null);

    expect(ui.fieldCheckExpandedNodes).toEqual(new Set(["tender"]));
  });
});
