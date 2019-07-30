import Vue from 'vue'
import './plugins/fontawesome'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import BootstrapVue from 'bootstrap-vue'
import VueI18n from 'vue-i18n'
import {messages as en} from './messages/en.js'
import {messages as cs} from './messages/cs.js'


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(VueI18n);
const i18n = new VueI18n({
    locale: 'cs', // set locale
    messages: {
        en: en,
        cs: cs
    }
})

Vue.config.productionTip = false

new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
}).$mount('#app')