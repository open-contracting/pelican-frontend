import { mount } from "@vue/test-utils";
import type { Plugin } from "vue";
import { createI18n } from "vue-i18n";
import en from "@/messages/en.json";
import es from "@/messages/es.json";

/** An i18n instance with the real catalogs, so tests exercise the strings that readers see. */
export function testI18n() {
  return createI18n({
    legacy: false,
    locale: "en",
    fallbackLocale: "en",
    warnHtmlMessage: false,
    messages: { en, es },
  });
}

/** Run a composable in a component's setup(), where its useX() calls can inject. */
export function mountComposable<T>(composable: () => T, plugins: Plugin[] = []): T {
  let result: T | undefined;
  mount(
    {
      setup() {
        result = composable();
        return () => null;
      },
    },
    { global: { plugins } },
  );
  return result as T;
}
