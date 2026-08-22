import { useI18n } from "vue-i18n";
import { LOCALES } from "@/config.js";

const STORAGE_KEY = "locale";
const FALLBACK = "en";

/** Return the language the user last chose, or the first of the browser's languages that Pelican has, or English. */
export function initialLocale(): string {
  const chosen = localStorage.getItem(STORAGE_KEY);
  if (chosen && chosen in LOCALES) {
    return chosen;
  }
  for (const language of navigator.languages) {
    const locale = language.split("-")[0];
    if (locale in LOCALES) {
      return locale;
    }
  }
  return FALLBACK;
}

export function useLocale() {
  const { locale } = useI18n();

  function setLocale(value: string) {
    locale.value = value;
    localStorage.setItem(STORAGE_KEY, value);
  }

  return { locale, setLocale };
}
