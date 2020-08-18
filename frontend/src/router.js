import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Overview from "./views/Overview.vue";
import Field from "./views/Field.vue";
import Resource from "./views/Resource.vue";
import Dataset from "./views/Dataset.vue";
import Time from "./views/Time.vue";
import ResourceCheckDetail from "./views/ResourceCheckDetail.vue";
import DatasetCheckDetail from "./views/DatasetCheckDetail.vue";
import FieldCheckDetail from "./views/FieldCheckDetail.vue";
import TimeVarianceCheckDetail from "./views/TimeVarianceCheckDetail.vue";
import ExtensionPreview from "./views/ExtensionPreview.vue";
import store from "./store";

Vue.use(Router);

export default new Router({
    mode: "history",
    base: process.env.BASE_URL,
    scrollBehavior() {
        return {
            x: 0,
            y: 0
        };
    },
    routes: [
        {
            path: "/",
            name: "home",
            component: Home
        },
        {
            path: "/overview/:datasetId",
            name: "overview",
            component: Overview,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        },
        {
            path: "/field/:datasetId",
            name: "field",
            component: Field,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        },
        {
            path: "/resource/:datasetId",
            name: "resource",
            component: Resource,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        },
        {
            path: "/dataset/:datasetId",
            name: "dataset",
            component: Dataset,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        },
        {
            path: "/time/:datasetId",
            name: "time",
            component: Time,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        },
        {
            path: "/resource/:datasetId/detail/:check",
            name: "resourceCheckDetail",
            component: ResourceCheckDetail,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store
                        .dispatch("loadDataset", to.params.datasetId)
                        .then(() => {
                            store.dispatch(
                                "loadResourceLevelCheckDetail",
                                to.params.check
                            );
                        });
                } else {
                    store.dispatch(
                        "loadResourceLevelCheckDetail",
                        to.params.check
                    );
                }

                next();
            }
        },
        {
            path: "/dataset/:datasetId/detail/:check",
            name: "datasetCheckDetail",
            component: DatasetCheckDetail,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        },
        {
            path: "/field/:datasetId/detail/:path",
            name: "fieldCheckDetail",
            component: FieldCheckDetail,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store
                        .dispatch("loadDataset", to.params.datasetId)
                        .then(() => {
                            store.dispatch(
                                "loadFieldLevelCheckDetail",
                                to.params.path
                            );
                        });
                } else {
                    store.dispatch("loadFieldLevelCheckDetail", to.params.path);
                }

                next();
            }
        },
        {
            path: "/time/:datasetId/detail/:check",
            name: "timeVarianceCheckDetail",
            component: TimeVarianceCheckDetail,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        },
        {
            path: "/extensionPreview/:datasetId/:extensionName",
            name: "extensionPreview",
            component: ExtensionPreview,
            beforeEnter: (to, from, next) => {
                if (store.getters.datasetId != to.params.datasetId) {
                    store.dispatch("loadDataset", to.params.datasetId);
                }
                next();
            }
        }
    ]
});
