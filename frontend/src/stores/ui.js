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
  };
});
