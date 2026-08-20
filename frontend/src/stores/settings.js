import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { CONFIG } from "@/config.js";

export const useSettingsStore = defineStore("settings", () => {
  const settings = ref({ template: {}, folder: null, user: null });

  async function load() {
    const response = await axios.get(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.settings}`);
    settings.value = response.data;
  }

  return { settings, load };
});
