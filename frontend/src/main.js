import { VueDatePicker } from "@vuepic/vue-datepicker";
import { useToast } from "bootstrap-vue-next";
import { createApp } from "vue";
import VueGoogleCharts from "vue-google-charts";
import { createI18n } from "vue-i18n";
import Multiselect from "vue-multiselect";
import App from "./App.vue";
import { useFormatters } from "./composables/useFormatters";
import { messages as en } from "./messages/en.js";
import { FontAwesomeIcon } from "./plugins/fontawesome";
import router from "./router";
import store from "./store";

const i18n = createI18n({
    legacy: false,
    locale: "en",
    messages: {
        en: en,
    },
});

const app = createApp(App);

app.config.globalProperties.$filters = useFormatters();

app.use(i18n);
app.use(router);
app.use(store);
app.use(VueGoogleCharts);

app.mixin({
    methods: {
        $toast(message, variant = "info") {
            const { show } = useToast();
            show({ body: message, variant, pos: "top-center" });
        },
    },
});

app.component("font-awesome-icon", FontAwesomeIcon);
app.component("Multiselect", Multiselect);
app.component("VueDatePicker", VueDatePicker);

app.mount("#app");

store.dispatch("loadSettings");
