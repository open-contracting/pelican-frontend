import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Overview from './views/Overview.vue'
import Field from './views/Field.vue'
import Resource from './views/Resource.vue'
import Dataset from './views/Dataset.vue'
import Time from './views/Time.vue'
import ResourceCheckDetail from './views/ResourceCheckDetail.vue'
import DatasetCheckDetail from './views/DatasetCheckDetail.vue'
import FieldCheckDetail from './views/FieldCheckDetail.vue'
import TimeVarianceCheckDetail from './views/TimeVarianceCheckDetail.vue'
import store from './store'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    scrollBehavior() {
        return {
            x: 0,
            y: 0
        };
    },
    routes: [{
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/overview',
            name: 'overview',
            component: Overview
        }, {
            path: '/field',
            name: 'field',
            component: Field
        }, {
            path: '/resource',
            name: 'resource',
            component: Resource
        }, {
            path: '/dataset',
            name: 'dataset',
            component: Dataset
        }, {
            path: '/time',
            name: 'time',
            component: Time
        }, {
            path: '/resource/detail/:check',
            name: 'resourceCheckDetail',
            component: ResourceCheckDetail,
            beforeEnter: (to, from, next) => {
                store.dispatch('loadResourceLevelCheckDetail', to.params.check);
                next();
            }
        }, {
            path: '/dataset/detail/:check',
            name: 'datasetCheckDetail',
            component: DatasetCheckDetail
        }, {
            path: '/field/detail/:path',
            name: 'fieldCheckDetail',
            component: FieldCheckDetail,
            beforeEnter: (to, from, next) => {
                store.dispatch('loadFieldLevelCheckDetail', to.params.path);
                next();
            }
        }, {
            path: '/time/detail/:check',
            name: 'timeVarianceCheckDetail',
            component: TimeVarianceCheckDetail
        },
    ]
})