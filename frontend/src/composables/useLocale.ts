import { useI18n } from "vue-i18n";
import api from "@/api.js";
import { CONFIG, isLocale } from "@/config.js";

const STORAGE_KEY = "locale";
const FALLBACK = "en";

/** Remember the choice, which the next page load reads before the account's settings arrive. */
export function rememberLocale(value: string) {
  localStorage.setItem(STORAGE_KEY, value);
}

/** Return the language the user last chose, or the first of the browser's languages that Pelican has, or English. */
export function initialLocale(): string {
  const chosen = localStorage.getItem(STORAGE_KEY);
  if (chosen && isLocale(chosen)) {
    return chosen;
  }
  for (const language of navigator.languages) {
    const locale = language.split("-")[0];
    if (isLocale(locale)) {
      return locale;
    }
  }
  return FALLBACK;
}

export function useLocale() {
  const { locale } = useI18n();

  function setLocale(value: string) {
    locale.value = value;
    rememberLocale(value);
    // The account is the source of truth, so that the choice follows the user between browsers.
    api.patch(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.settings}`, { language: value }).catch(() => {});
  }

  return { locale, setLocale };
}
