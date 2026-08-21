import { defineStore } from "pinia";
import { computed, ref } from "vue";
import api from "@/api.js";
import { CONFIG } from "@/config.js";
import { useUiStore } from "@/stores/ui.js";
import type {
  DataItem,
  Dataset,
  DatasetLevelCheck,
  DatasetLevelMeta,
  DatasetLevelReport,
  FieldLevelCheck,
  FieldLevelCheckDetail,
  FieldLevelReport,
  ResourceLevelCheck,
  ResourceLevelCheckDetail,
  ResourceLevelReport,
  TimeVarianceLevelCheck,
  TimeVarianceLevelReport,
} from "@/types.js";

export const useDatasetStore = defineStore("dataset", () => {
  const ui = useUiStore();

  const dataItems = ref<DataItem[]>([]);
  const dataset = ref<Dataset | null>(null);
  const datasetLevelStats = ref<DatasetLevelCheck[] | null>(null);
  const fieldLevelStats = ref<FieldLevelCheck[] | null>(null);
  const resourceLevelStats = ref<ResourceLevelCheck[] | null>(null);
  const timeVarianceLevelStats = ref<TimeVarianceLevelCheck[] | null>(null);

  // "[vue-router] missing param for named route "overview": Expected "datasetId" to be defined"
  // When refreshing a subpage, dataset is not set until loadDataset() is called.
  const datasetId = computed(() => dataset.value?.id);

  function resourceLevelStatsBySection(sectionName: string) {
    if (resourceLevelStats.value != null) {
      return resourceLevelStats.value.filter((item) => item.name.startsWith(sectionName));
    }

    return [];
  }

  function resourceLevelCheckByName(checkName: string) {
    return resourceLevelStats.value?.find((item) => item.name === checkName);
  }

  function datasetLevelCheckByName(checkName: string) {
    return datasetLevelStats.value?.find((item) => item.name === checkName);
  }

  function fieldLevelCheckByPath(path: string) {
    return fieldLevelStats.value?.find((item) => item.path === path);
  }

  function timeVarianceLevelCheckByName(checkName: string) {
    return timeVarianceLevelStats.value?.find((item) => item.name === checkName);
  }

  function dataItemById(itemId: number) {
    return dataItems.value.find((item) => item.id === itemId);
  }

  function dataItemJSON(itemId: number) {
    const dataItem = dataItemById(itemId);
    return dataItem ? JSON.stringify(dataItem.data, null, 2) : null;
  }

  function dataItemJSONLines(itemId: number) {
    return dataItemJSON(itemId)?.split("\n").length ?? null;
  }

  function reset() {
    fieldLevelStats.value = null;
    datasetLevelStats.value = null;
    resourceLevelStats.value = null;
    ui.resetForDataset();
  }

  async function loadDataset(id: number | string) {
    const data = await api.get<Dataset>(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}${id}`);

    reset();
    dataset.value = data;

    await Promise.all([
      loadResourceLevelStats(data.id),
      loadDatasetLevelStats(data.id),
      loadTimeVarianceLevelStats(data.id),
      loadFieldLevelStats(data.id),
    ]);
  }

  async function loadResourceLevelStats(datasetId: number) {
    resourceLevelStats.value = null;

    const formatted = CONFIG.apiEndpoints.resourceLevelReport.replace(/{id}/g, String(datasetId));
    const report = await api.get<ResourceLevelReport>(`${CONFIG.apiBaseUrl}${formatted}`);

    resourceLevelStats.value = Object.entries(report).map(([name, check]) => ({ ...check, name }));
  }

  async function loadResourceLevelCheckDetail(checkName: string) {
    const checkDetail = resourceLevelCheckByName(checkName);

    if (
      dataset.value == null ||
      resourceLevelStats.value == null ||
      checkDetail == null ||
      checkDetail.examples_filled
    ) {
      return;
    }

    const formatted = CONFIG.apiEndpoints.resourceLevelDetail
      .replace(/{id}/g, String(dataset.value.id))
      .replace(/{name}/g, checkName);
    const detail = await api.get<ResourceLevelCheckDetail>(`${CONFIG.apiBaseUrl}${formatted}`);

    detail.examples_filled = true;
    const updatedStats = [...resourceLevelStats.value];
    updatedStats.forEach((item, i) => {
      if (item.name === checkName) Object.assign(updatedStats[i], detail);
    });

    resourceLevelStats.value = updatedStats;
  }

  async function loadDatasetLevelStats(datasetId: number) {
    datasetLevelStats.value = null;

    const formatted = CONFIG.apiEndpoints.datasetLevelReport.replace(/{id}/g, String(datasetId));
    const report = await api.get<DatasetLevelReport>(`${CONFIG.apiBaseUrl}${formatted}`);

    datasetLevelStats.value = Object.entries(report).map(([name, check]) => ({
      ...check,
      name,
      meta: check.meta as DatasetLevelMeta,
    }));
  }

  async function loadDataItem(itemId: number) {
    if (dataItemById(itemId) != null) {
      return;
    }

    const formatted = CONFIG.apiEndpoints.dataItem.replace(/{id}/g, String(itemId));
    dataItems.value.push(await api.get<DataItem>(`${CONFIG.apiBaseUrl}${formatted}`));
  }

  async function loadFieldLevelStats(datasetId: number) {
    fieldLevelStats.value = null;

    const okRatio = (item: { passed_count: number; total_count: number }) => {
      const result = item.passed_count / item.total_count;
      return Number.isNaN(result) ? 0 : result;
    };

    const failedRatio = (item: { failed_count: number; total_count: number }) => {
      const result = item.failed_count / item.total_count;
      return Number.isNaN(result) ? 0 : result;
    };

    const formatted = CONFIG.apiEndpoints.fieldLevelReport.replace(/{id}/g, String(datasetId));
    const report = await api.get<FieldLevelReport>(`${CONFIG.apiBaseUrl}${formatted}`);

    fieldLevelStats.value = Object.entries(report).map(([path, check]) => ({
      ...check,
      path,
      coverageOkRatio: okRatio(check.coverage),
      coverageFailedRatio: failedRatio(check.coverage),
      qualityOkRatio: okRatio(check.quality),
      qualityFailedRatio: failedRatio(check.quality),
    }));
  }

  async function loadFieldLevelCheckDetail(path: string) {
    const checkDetail = fieldLevelCheckByPath(path);

    if (dataset.value == null || fieldLevelStats.value == null || checkDetail == null || checkDetail.examples_filled) {
      return;
    }

    const formatted = CONFIG.apiEndpoints.fieldLevelDetail
      .replace(/{id}/g, String(dataset.value.id))
      .replace(/{name}/g, path);
    const detail = await api.get<FieldLevelCheckDetail>(`${CONFIG.apiBaseUrl}${formatted}`);

    detail.examples_filled = true;
    const updatedStats = [...fieldLevelStats.value];
    updatedStats.forEach((item, i) => {
      if (item.path === path) Object.assign(updatedStats[i], detail);
    });

    fieldLevelStats.value = updatedStats;
  }

  async function loadTimeVarianceLevelStats(datasetId: number) {
    timeVarianceLevelStats.value = null;

    const formatted = CONFIG.apiEndpoints.timeVarianceLevelReport.replace(/{id}/g, String(datasetId));
    const report = await api.get<TimeVarianceLevelReport>(`${CONFIG.apiBaseUrl}${formatted}`);

    timeVarianceLevelStats.value = Object.entries(report).map(([name, check]) => ({ ...check, name }));
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
