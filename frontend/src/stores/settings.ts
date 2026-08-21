import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api.js";
import { CONFIG } from "@/config.js";
import type { Settings } from "@/types.js";

export const useSettingsStore = defineStore("settings", () => {
  const settings = ref<Settings>({ template: {}, folder: "", user: "" });

  async function load() {
    settings.value = await api.get<Settings>(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.settings}`);
  }

  return { settings, load };
});
