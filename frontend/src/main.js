import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import "./scss/main.scss";
import en from "./messages/en.json";
import es from "./messages/es.json";
import { FontAwesomeIcon } from "./plugins/fontawesome";
import router from "./router";
import store from "./store";

const i18n = createI18n({
  legacy: false,
  locale: "en",
  fallbackLocale: "en",
  warnHtmlMessage: false,
  messages: { en, es },
});

const app = createApp(App);

app.use(i18n);
app.use(router);
app.use(store);

app.component("FontAwesomeIcon", FontAwesomeIcon);

app.mount("#app");

store.dispatch("loadSettings");
