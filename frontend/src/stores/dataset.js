import axios from "axios";
import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { CONFIG } from "@/config.js";
import { useUiStore } from "@/stores/ui.js";

export const useDatasetStore = defineStore("dataset", () => {
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
    useUiStore().resetForDataset();
  }

  function loadDataset(id) {
    return new Promise((resolve) => {
      axios
        .get(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.dataset}${id}`)
        .then((response) => {
          reset();
          dataset.value = response.data;
          Promise.all([
            loadResourceLevelStats(),
            loadDatasetLevelStats(),
            loadTimeVarianceLevelStats(),
            loadFieldLevelStats(),
          ]).then(() => {
            resolve();
          });
        })
        .catch((error) => {
          throw new Error(error);
        });
    });
  }

  function loadResourceLevelStats() {
    return new Promise((resolve) => {
      resourceLevelStats.value = null;
      const formatted = CONFIG.apiEndpoints.resourceLevelReport.replace(/{id}/g, dataset.value.id);
      axios
        .get(`${CONFIG.apiBaseUrl}${formatted}`)
        .then((response) => {
          const data = [];
          for (const key in response.data) {
            response.data[key].name = key;
            data.push(response.data[key]);
          }
          resourceLevelStats.value = data;
          resolve();
        })
        .catch((error) => {
          throw new Error(error);
        });
    });
  }

  function loadResourceLevelCheckDetail(checkName) {
    return new Promise((resolve) => {
      const checkDetail = resourceLevelCheckByName(checkName);

      if (checkDetail != null && !checkDetail.examplesLoaded) {
        if (dataset.value != null && checkName != null) {
          const formatted = CONFIG.apiEndpoints.resourceLevelDetail
            .replace(/{id}/g, dataset.value.id)
            .replace(/{name}/g, checkName);
          axios
            .get(`${CONFIG.apiBaseUrl}${formatted}`)
            .then((response) => {
              response.data.examples_filled = true;
              const updatedStats = [].concat(resourceLevelStats.value);
              updatedStats.forEach((item, i) => {
                if (item.name === checkName) Object.assign(updatedStats[i], response.data);
              });
              resourceLevelStats.value = updatedStats;
              resolve();
            })
            .catch((error) => {
              throw new Error(error);
            });
        }
      }
    });
  }

  function loadDatasetLevelStats() {
    return new Promise((resolve) => {
      datasetLevelStats.value = null;
      const formatted = CONFIG.apiEndpoints.datasetLevelReport.replace(/{id}/g, dataset.value.id);
      axios
        .get(`${CONFIG.apiBaseUrl}${formatted}`)
        .then((response) => {
          const data = [];
          for (const key in response.data) {
            response.data[key].name = key;
            data.push(response.data[key]);
          }
          datasetLevelStats.value = data;
          resolve();
        })
        .catch((error) => {
          throw new Error(error);
        });
    });
  }

  function loadDataItem(itemId) {
    return new Promise((resolve, reject) => {
      if (dataItemById(itemId) == null) {
        const formatted = CONFIG.apiEndpoints.dataItem.replace(/{id}/g, itemId);
        axios
          .get(`${CONFIG.apiBaseUrl}${formatted}`)
          .then((response) => {
            dataItems.value.push(response.data);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      } else {
        resolve();
      }
    });
  }

  function loadFieldLevelStats() {
    return new Promise((resolve) => {
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
      axios
        .get(`${CONFIG.apiBaseUrl}${formatted}`)
        .then((response) => {
          const data = [];
          for (const key in response.data) {
            const item = response.data[key];
            data.push({
              ...item,
              path: key,
              coverageOkRatio: okRatio(item.coverage),
              coverageFailedRatio: failedRatio(item.coverage),
              qualityOkRatio: okRatio(item.quality),
              qualityFailedRatio: failedRatio(item.quality),
            });
            resolve();
          }

          fieldLevelStats.value = data;
          useUiStore().fieldCheckSorting = null;
        })
        .catch((error) => {
          throw new Error(error);
        });
    });
  }

  function loadFieldLevelCheckDetail(path) {
    const checkDetail = fieldLevelCheckByPath(path);

    if (checkDetail == null || (checkDetail != null && !checkDetail.examplesLoaded)) {
      if (dataset.value != null && path != null) {
        const formatted = CONFIG.apiEndpoints.fieldLevelDetail
          .replace(/{id}/g, dataset.value.id)
          .replace(/{name}/g, path);
        axios
          .get(`${CONFIG.apiBaseUrl}${formatted}`)
          .then((response) => {
            response.data.examples_filled = true;
            const updatedStats = [].concat(fieldLevelStats.value);
            updatedStats.forEach((item, i) => {
              if (item.path === path) Object.assign(updatedStats[i], response.data);
            });
            fieldLevelStats.value = updatedStats;
          })
          .catch((error) => {
            throw new Error(error);
          });
      }
    }
  }

  function loadTimeVarianceLevelStats() {
    return new Promise((resolve) => {
      timeVarianceLevelStats.value = null;
      const formatted = CONFIG.apiEndpoints.timeVarianceLevelReport.replace(/{id}/g, dataset.value.id);
      axios
        .get(`${CONFIG.apiBaseUrl}${formatted}`)
        .then((response) => {
          const data = [];
          for (const key in response.data) {
            response.data[key].name = key;
            data.push(response.data[key]);
          }
          timeVarianceLevelStats.value = data;
          resolve();
        })
        .catch((error) => {
          throw new Error(error);
        });
    });
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
    loadDatasetLevelStats,
    loadFieldLevelCheckDetail,
    loadFieldLevelStats,
    loadResourceLevelCheckDetail,
    loadResourceLevelStats,
    loadTimeVarianceLevelStats,
  };
});
