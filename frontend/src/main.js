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
import Clipboard from "v-clipboard";
import Multiselect from "vue-multiselect";
import { messages as en } from "./messages/en.js";
import { Plugin } from "vue-fragment";
import DatePick from "vue-date-pick";

Vue.use(VueGoogleCharts);
Vue.use(Plugin);
Vue.use(BootstrapVue);
Vue.use(VueI18n);
Vue.use(VueSimpleAlert);
Vue.use(Clipboard);
Vue.use(Multiselect);
Vue.component("DatePick", DatePick);
Vue.component("Multiselect", Multiselect);
const i18n = new VueI18n({
    locale: "en",
    messages: {
        en: en
    }
});

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    i18n,
    render: h => h(App),
    created() {
        this.$store.dispatch("loadSettings");
    }
}).$mount("#app");
