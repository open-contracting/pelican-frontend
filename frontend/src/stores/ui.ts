import { defineStore } from "pinia";
import { ref, shallowRef } from "vue";
import type { FieldLevelCheck, Sorting } from "@/types.js";

export const useUiStore = defineStore("ui", () => {
  const datasetSearch = ref<string | null>(null);
  const datasetSorting = ref<Sorting | null>(null);
  const datasetLevelFilterIndex = ref(0);
  const fieldCheckExpandedNodes = ref(new Set<string>());
  const fieldCheckLayout = ref<"table" | "tree">("table");
  const fieldCheckSearch = ref<string | null>(null);
  const fieldCheckSorting = ref<Sorting | null>(null);
  // A predicate, not a value, so it must not be made reactive.
  const fieldLevelFilter = shallowRef<(check: FieldLevelCheck) => boolean>(() => true);
  const fieldLevelFilterIndex = ref(0);
  const resourceCheckExpandedNodes = ref(new Set<string>());
  const resourceLevelFilterIndex = ref(0);
  const timeLevelFilterIndex = ref(0);

  function isFieldCheckExpanded(path: string) {
    return fieldCheckExpandedNodes.value.has(path);
  }

  function expandFieldCheck(path: string) {
    fieldCheckExpandedNodes.value.add(path);
  }

  function collapseFieldCheck(path: string) {
    for (const node of [...fieldCheckExpandedNodes.value]) {
      if (node.startsWith(path)) {
        fieldCheckExpandedNodes.value.delete(node);
      }
    }
  }

  function isResourceCheckExpanded(section: string) {
    return resourceCheckExpandedNodes.value.has(section);
  }

  function expandResourceCheck(section: string) {
    resourceCheckExpandedNodes.value.add(section);
  }

  function collapseResourceCheck(section: string) {
    for (const node of [...resourceCheckExpandedNodes.value]) {
      if (node.startsWith(section)) {
        resourceCheckExpandedNodes.value.delete(node);
      }
    }
  }

  /** Restore the field check page's defaults, for a newly loaded dataset. */
  function resetForDataset() {
    fieldCheckExpandedNodes.value = new Set();
    fieldCheckLayout.value = "table";
    fieldCheckSearch.value = null;
    fieldCheckSorting.value = null;
  }

  /** Expand the field checks that the search matches, and their ancestors. */
  function setExpandedNodesForSearch(stats: FieldLevelCheck[] | null) {
    if (stats) {
      fieldCheckExpandedNodes.value = new Set();

      if (fieldCheckSearch.value) {
        const search = fieldCheckSearch.value.toLowerCase();
        const isPathSearched = (path: string) => path.toLowerCase().includes(search);

        let nodes = [];
        const remaining = [];
        // select paths that match the search
        for (const n of stats) {
          if (isPathSearched(n.path)) {
            nodes.push(n.path);
          } else {
            remaining.push(n.path);
          }
        }

        // add parents
        for (const n of remaining) {
          if (nodes.some((m) => m.startsWith(`${n}.`))) {
            nodes.push(n);
          }
        }

        // collapse matched nodes without matching child
        const matched = [...nodes];
        nodes = nodes.filter((n) => {
          return (
            // keep parent without match
            !isPathSearched(n) ||
            matched.some((m) => {
              return m.startsWith(`${n}.`) && isPathSearched(m.substr(n.length));
            })
          );
        });

        fieldCheckExpandedNodes.value = new Set(nodes);
      }
    }
  }

  return {
    datasetSearch,
    datasetSorting,
    datasetLevelFilterIndex,
    fieldCheckExpandedNodes,
    fieldCheckLayout,
    fieldCheckSearch,
    fieldCheckSorting,
    fieldLevelFilter,
    fieldLevelFilterIndex,
    resourceCheckExpandedNodes,
    resourceLevelFilterIndex,
    timeLevelFilterIndex,
    isFieldCheckExpanded,
    expandFieldCheck,
    collapseFieldCheck,
    isResourceCheckExpanded,
    expandResourceCheck,
    collapseResourceCheck,
    resetForDataset,
    setExpandedNodesForSearch,
  };
});
