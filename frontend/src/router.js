// biome-ignore assist/source/organizeImports: Import order affects preview pane sizing.
import { createRouter, createWebHistory } from "vue-router";
import { useDatasetStore } from "./stores/dataset.js";
import { useErrorStore } from "./stores/error.js";
import Dataset from "./views/Dataset.vue";
import Field from "./views/Field.vue";
import Home from "./views/Home.vue";
import Overview from "./views/Overview.vue";
import Resource from "./views/Resource.vue";
import Time from "./views/Time.vue";

// If these are in the same group as above, the preview pane is incorrectly sized.
import DatasetCheckDetail from "./views/DatasetCheckDetail.vue";
import FieldCheckDetail from "./views/FieldCheckDetail.vue";
import ResourceCheckDetail from "./views/ResourceCheckDetail.vue";
import TimeVarianceCheckDetail from "./views/TimeVarianceCheckDetail.vue";

async function load(datasetId, after) {
  const datasetStore = useDatasetStore();

  try {
    // The ID is a number in the store and a string in the route. A strict comparison always differs, which would
    // reload the dataset on every navigation, resetting each page's search, sorting, filter and expansion.
    if (String(datasetStore.datasetId) !== datasetId) {
      await datasetStore.loadDataset(datasetId);
    }
    await after?.();
  } catch {
    // `beforeEnter` doesn't await this, so the rejection must be caught. api.js reported it, so this catch is empty.
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return {
      top: 0,
      left: 0,
    };
  },
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/overview/:datasetId",
      name: "overview",
      component: Overview,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId);
        next();
      },
    },
    {
      path: "/field/:datasetId",
      name: "field",
      component: Field,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId);
        next();
      },
    },
    {
      path: "/resource/:datasetId",
      name: "resource",
      component: Resource,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId);
        next();
      },
    },
    {
      path: "/dataset/:datasetId",
      name: "dataset",
      component: Dataset,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId);
        next();
      },
    },
    {
      path: "/time/:datasetId",
      name: "time",
      component: Time,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId);
        next();
      },
    },
    {
      path: "/resource/:datasetId/detail/:check",
      name: "resourceCheckDetail",
      component: ResourceCheckDetail,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId, () => useDatasetStore().loadResourceLevelCheckDetail(to.params.check));
        next();
      },
    },
    {
      path: "/dataset/:datasetId/detail/:check",
      name: "datasetCheckDetail",
      component: DatasetCheckDetail,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId);
        next();
      },
    },
    {
      path: "/field/:datasetId/detail/:path",
      name: "fieldCheckDetail",
      component: FieldCheckDetail,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId, () => useDatasetStore().loadFieldLevelCheckDetail(to.params.path));
        next();
      },
    },
    {
      path: "/time/:datasetId/detail/:check",
      name: "timeVarianceCheckDetail",
      component: TimeVarianceCheckDetail,
      beforeEnter: (to, _from, next) => {
        load(to.params.datasetId);
        next();
      },
    },
  ],
});

router.beforeEach(() => {
  useErrorStore().clear();
});

export default router;
