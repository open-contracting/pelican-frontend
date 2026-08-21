import { defineStore } from "pinia";
import { computed, ref } from "vue";
import api from "@/api.js";
import { CONFIG } from "@/config.js";
import { useUiStore } from "@/stores/ui.js";

export const useDatasetStore = defineStore("dataset", () => {
  const ui = useUiStore();

  const dataItems = ref([]);
  const dataset = ref(null);
  const datasetLevelStats = ref(null);
  const fieldLevelStats = ref(null);
  const resourceLevelStats = ref(null);
  const timeVarianceLevelStats = ref(null);

  // "[vue-router] missing param for named route "overview": Expected "datasetId" to be defined"
  // When refreshing a subpage, dataset is not set until loadDataset() is called.
  const datasetId = computed(() => dataset.value?.id);

  function resourceLevelStatsBySection(sectionName) {
    if (resourceLevelStats.value != null) {
      return resourceLevelStats.value.filter((item) => item.name.startsWith(sectionName));
    }

    return [];
  }

  function resourceLevelCheckByName(checkName) {
    return resourceLevelStats.value?.find((item) => item.name === checkName);
  }

  function datasetLevelCheckByName(checkName) {
    return datasetLevelStats.value?.find((item) => item.name === checkName);
  }

  function fieldLevelCheckByPath(path) {
    return fieldLevelStats.value?.find((item) => item.path === path);
  }

  function timeVarianceLevelCheckByName(checkName) {
    return timeVarianceLevelStats.value?.find((item) => item.name === checkName);
  }

  function dataItemById(itemId) {
    return dataItems.value.find((item) => item.id === itemId);
  }

  function dataItemJSON(itemId) {
    const dataItem = dataItemById(itemId);
    return dataItem ? JSON.stringify(dataItem.data, null, 2) : null;
  }

  function dataItemJSONLines(itemId) {
    return dataItemJSON(itemId)?.split("\n").length ?? null;
  }

  function reset() {
    fieldLevelStats.value = null;
    datasetLevelStats.value = null;
    resourceLevelStats.value = null;
    ui.resetForDataset();
  }

  async function loadDataset(id) {
    const data = await api.get(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}${id}`);

    reset();
    dataset.value = data;

    await Promise.all([
      loadResourceLevelStats(),
      loadDatasetLevelStats(),
      loadTimeVarianceLevelStats(),
      loadFieldLevelStats(),
    ]);
  }

  async function loadResourceLevelStats() {
    resourceLevelStats.value = null;

    const formatted = CONFIG.apiEndpoints.resourceLevelReport.replace(/{id}/g, dataset.value.id);
    const report = await api.get(`${CONFIG.apiBaseUrl}${formatted}`);

    const data = [];
    for (const key in report) {
      report[key].name = key;
      data.push(report[key]);
    }

    resourceLevelStats.value = data;
  }

  async function loadResourceLevelCheckDetail(checkName) {
    const checkDetail = resourceLevelCheckByName(checkName);

    if (checkDetail == null || checkDetail.examplesLoaded) {
      return;
    }

    const formatted = CONFIG.apiEndpoints.resourceLevelDetail
      .replace(/{id}/g, dataset.value.id)
      .replace(/{name}/g, checkName);
    const detail = await api.get(`${CONFIG.apiBaseUrl}${formatted}`);

    detail.examples_filled = true;
    const updatedStats = [].concat(resourceLevelStats.value);
    updatedStats.forEach((item, i) => {
      if (item.name === checkName) Object.assign(updatedStats[i], detail);
    });

    resourceLevelStats.value = updatedStats;
  }

  async function loadDatasetLevelStats() {
    datasetLevelStats.value = null;

    const formatted = CONFIG.apiEndpoints.datasetLevelReport.replace(/{id}/g, dataset.value.id);
    const report = await api.get(`${CONFIG.apiBaseUrl}${formatted}`);

    const data = [];
    for (const key in report) {
      report[key].name = key;
      data.push(report[key]);
    }

    datasetLevelStats.value = data;
  }

  async function loadDataItem(itemId) {
    if (dataItemById(itemId) != null) {
      return;
    }

    const formatted = CONFIG.apiEndpoints.dataItem.replace(/{id}/g, itemId);
    dataItems.value.push(await api.get(`${CONFIG.apiBaseUrl}${formatted}`));
  }

  async function loadFieldLevelStats() {
    fieldLevelStats.value = null;

    const okRatio = (item) => {
      const result = item.passed_count / item.total_count;
      return Number.isNaN(result) ? 0 : result;
    };

    const failedRatio = (item) => {
      const result = item.failed_count / item.total_count;
      return Number.isNaN(result) ? 0 : result;
    };

    const formatted = CONFIG.apiEndpoints.fieldLevelReport.replace(/{id}/g, dataset.value.id);
    const report = await api.get(`${CONFIG.apiBaseUrl}${formatted}`);

    const data = [];
    for (const key in report) {
      const item = report[key];
      data.push({
        ...item,
        path: key,
        coverageOkRatio: okRatio(item.coverage),
        coverageFailedRatio: failedRatio(item.coverage),
        qualityOkRatio: okRatio(item.quality),
        qualityFailedRatio: failedRatio(item.quality),
      });
    }

    fieldLevelStats.value = data;
  }

  async function loadFieldLevelCheckDetail(path) {
    const checkDetail = fieldLevelCheckByPath(path);

    if (checkDetail == null || checkDetail.examplesLoaded) {
      return;
    }

    const formatted = CONFIG.apiEndpoints.fieldLevelDetail.replace(/{id}/g, dataset.value.id).replace(/{name}/g, path);
    const detail = await api.get(`${CONFIG.apiBaseUrl}${formatted}`);

    detail.examples_filled = true;
    const updatedStats = [].concat(fieldLevelStats.value);
    updatedStats.forEach((item, i) => {
      if (item.path === path) Object.assign(updatedStats[i], detail);
    });

    fieldLevelStats.value = updatedStats;
  }

  async function loadTimeVarianceLevelStats() {
    timeVarianceLevelStats.value = null;

    const formatted = CONFIG.apiEndpoints.timeVarianceLevelReport.replace(/{id}/g, dataset.value.id);
    const report = await api.get(`${CONFIG.apiBaseUrl}${formatted}`);

    const data = [];
    for (const key in report) {
      report[key].name = key;
      data.push(report[key]);
    }

    timeVarianceLevelStats.value = data;
  }

  return {
    dataItems,
    dataset,
    datasetId,
    datasetLevelStats,
    fieldLevelStats,
    resourceLevelStats,
    timeVarianceLevelStats,
    dataItemById,
    dataItemJSON,
    dataItemJSONLines,
    datasetLevelCheckByName,
    fieldLevelCheckByPath,
    resourceLevelCheckByName,
    resourceLevelStatsBySection,
    timeVarianceLevelCheckByName,
    loadDataItem,
    loadDataset,
    loadFieldLevelCheckDetail,
    loadResourceLevelCheckDetail,
  };
});
