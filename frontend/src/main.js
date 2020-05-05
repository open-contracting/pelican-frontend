import Vue from "vue";
import "./plugins/fontawesome";
import "./plugins/numeral";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import BootstrapVue from "bootstrap-vue";
import VueI18n from "vue-i18n";
import VueGoogleCharts from "vue-google-charts";
import VueSimpleAlert from "vue-simple-alert";
import Clipboard from 'v-clipboard';
import VModal from 'vue-js-modal';
import Multiselect from 'vue-multiselect'
import { messages as en } from "./messages/en.js";
import { messages as cs } from "./messages/cs.js";
import Fragment from "vue-fragment";
import DatePick from "vue-date-pick";

if (window.navigator && navigator.serviceWorker) {
    navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for (let registration of registrations) {
            registration.unregister();
        }
    });
}

Vue.use(VueGoogleCharts);
Vue.use(Fragment.Plugin);
Vue.use(BootstrapVue);
Vue.use(VueI18n);
Vue.use(VueSimpleAlert);
Vue.use(Clipboard);
Vue.use(VModal);
Vue.use(Multiselect);
Vue.component('date-pick', DatePick);
Vue.component('multiselect', Multiselect);
const i18n = new VueI18n({
    locale: "en", // set locale
    messages: {
        en: en,
        cs: cs
    }
});

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
}).$mount("#app");
