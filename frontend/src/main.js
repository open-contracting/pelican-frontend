import { useToast } from "bootstrap-vue-next";
import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import { useFormatters } from "./composables/useFormatters";
import { messages as en } from "./messages/en.js";
import { FontAwesomeIcon } from "./plugins/fontawesome";
import router from "./router";
import store from "./store";

const i18n = createI18n({
    legacy: false,
    locale: "en",
    warnHtmlMessage: false,
    messages: {
        en: en,
    },
});

const app = createApp(App);

app.config.globalProperties.$filters = useFormatters();

app.use(i18n);
app.use(router);
app.use(store);

app.mixin({
    methods: {
        $toast(message, variant = "info") {
            const { show } = useToast();
            show({ body: message, variant, pos: "top-center" });
        },
    },
});

app.component("FontAwesomeIcon", FontAwesomeIcon);

app.mount("#app");

store.dispatch("loadSettings");
