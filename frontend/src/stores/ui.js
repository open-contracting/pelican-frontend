import { defineStore } from "pinia";
import { ref, shallowRef } from "vue";

export const useUiStore = defineStore("ui", () => {
  const datasetSearch = ref(null);
  const datasetSorting = ref(null);
  const datasetLevelFilterIndex = ref(0);
  const fieldCheckExpandedNodes = ref([]);
  const fieldCheckLayout = ref("table");
  const fieldCheckSearch = ref(null);
  const fieldCheckSorting = ref(null);
  // A predicate, not a value, so it must not be made reactive.
  const fieldLevelFilter = shallowRef(() => true);
  const fieldLevelFilterIndex = ref(0);
  const resourceCheckExpandedNodes = ref([]);
  const resourceLevelFilterIndex = ref(0);
  const timeLevelFilterIndex = ref(0);

  function isFieldCheckExpanded(path) {
    return fieldCheckExpandedNodes.value.includes(path);
  }

  function expandFieldCheck(path) {
    if (!isFieldCheckExpanded(path)) {
      fieldCheckExpandedNodes.value.push(path);
    }
  }

  function collapseFieldCheck(path) {
    fieldCheckExpandedNodes.value = fieldCheckExpandedNodes.value.filter((v) => !v.startsWith(path));
  }

  function isResourceCheckExpanded(section) {
    return resourceCheckExpandedNodes.value.includes(section);
  }

  function expandResourceCheck(section) {
    if (!isResourceCheckExpanded(section)) {
      resourceCheckExpandedNodes.value.push(section);
    }
  }

  function collapseResourceCheck(section) {
    resourceCheckExpandedNodes.value = resourceCheckExpandedNodes.value.filter((v) => !v.startsWith(section));
  }

  /** Restore the field check page's defaults, for a newly loaded dataset. */
  function resetForDataset() {
    fieldCheckExpandedNodes.value = [];
    fieldCheckLayout.value = "table";
    fieldCheckSearch.value = null;
    fieldCheckSorting.value = null;
  }

  /** Expand the field checks that the search matches, and their ancestors. */
  function setExpandedNodesForSearch(stats) {
    const isPathSearched = (path) => {
      return !!path?.toLowerCase().includes(fieldCheckSearch.value.toLowerCase());
    };

    if (stats) {
      fieldCheckExpandedNodes.value = [];

      if (fieldCheckSearch.value) {
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

        fieldCheckExpandedNodes.value = nodes;
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
