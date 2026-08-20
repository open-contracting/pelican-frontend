// biome-ignore assist/source/organizeImports: Import order affects preview pane sizing.
import { createRouter, createWebHistory } from "vue-router";
import store from "./store";
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

// The ID is a number in the store and a string in the route. A strict comparison always differs, which would reload
// the dataset on every navigation, resetting each page's search, sorting, filter and expansion.
function isDatasetLoaded(datasetId) {
  return String(store.getters.datasetId) === datasetId;
}

export default createRouter({
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
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId);
        }
        next();
      },
    },
    {
      path: "/field/:datasetId",
      name: "field",
      component: Field,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId);
        }
        next();
      },
    },
    {
      path: "/resource/:datasetId",
      name: "resource",
      component: Resource,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId);
        }
        next();
      },
    },
    {
      path: "/dataset/:datasetId",
      name: "dataset",
      component: Dataset,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId);
        }
        next();
      },
    },
    {
      path: "/time/:datasetId",
      name: "time",
      component: Time,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId);
        }
        next();
      },
    },
    {
      path: "/resource/:datasetId/detail/:check",
      name: "resourceCheckDetail",
      component: ResourceCheckDetail,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId).then(() => {
            store.dispatch("loadResourceLevelCheckDetail", to.params.check);
          });
        } else {
          store.dispatch("loadResourceLevelCheckDetail", to.params.check);
        }
        next();
      },
    },
    {
      path: "/dataset/:datasetId/detail/:check",
      name: "datasetCheckDetail",
      component: DatasetCheckDetail,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId);
        }
        next();
      },
    },
    {
      path: "/field/:datasetId/detail/:path",
      name: "fieldCheckDetail",
      component: FieldCheckDetail,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId).then(() => {
            store.dispatch("loadFieldLevelCheckDetail", to.params.path);
          });
        } else {
          store.dispatch("loadFieldLevelCheckDetail", to.params.path);
        }
        next();
      },
    },
    {
      path: "/time/:datasetId/detail/:check",
      name: "timeVarianceCheckDetail",
      component: TimeVarianceCheckDetail,
      beforeEnter: (to, _from, next) => {
        if (!isDatasetLoaded(to.params.datasetId)) {
          store.dispatch("loadDataset", to.params.datasetId);
        }
        next();
      },
    },
  ],
});
