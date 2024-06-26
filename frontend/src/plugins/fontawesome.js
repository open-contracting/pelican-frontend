import { library } from "@fortawesome/fontawesome-svg-core";
import { far } from "@fortawesome/free-regular-svg-icons";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from "@fortawesome/vue-fontawesome";
import Vue from "vue";

library.add(fas);
library.add(far);

Vue.component("FontAwesomeIcon", FontAwesomeIcon);
Vue.component("FontAwesomeLayers", FontAwesomeLayers);
Vue.component("FontAwesomeLayersText", FontAwesomeLayersText);
