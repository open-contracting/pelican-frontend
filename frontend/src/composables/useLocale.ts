import { useI18n } from "vue-i18n";
import { LOCALES } from "@/config.js";

const STORAGE_KEY = "locale";
const FALLBACK = "en";

/**
 * Return the reader's language: the one they last chose, else the first their browser asks for that
 * Pelican has, else English. The browser's language is a poor proxy on its own, because an analyst
 * reviewing another country's data reads the interface in their own.
 */
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

  // Until #188 stores the preference against the reader's account, it lives in their browser.
  function setLocale(value: string) {
    locale.value = value;
    localStorage.setItem(STORAGE_KEY, value);
  }

  return { locale, setLocale };
}
