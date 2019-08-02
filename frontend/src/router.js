import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Overview from './views/Overview.vue'
import Field from './views/Field.vue'
import Resource from './views/Resource.vue'
import Dataset from './views/Dataset.vue'
import Time from './views/Time.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
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
    }]
})