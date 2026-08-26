import { beforeEach, describe, expect, it, vi } from "vitest";
import api from "@/api.js";
import { initialLocale, rememberLocale, useLocale } from "@/composables/useLocale.js";
import { mountComposable, testI18n } from "@/test/helpers.js";

vi.mock("@/api.js", () => ({ default: { patch: vi.fn(async () => {}) } }));

function setBrowserLanguages(languages: string[]) {
  Object.defineProperty(window.navigator, "languages", { value: languages, configurable: true });
}

beforeEach(() => {
  localStorage.clear();
  vi.mocked(api.patch).mockClear();
});

describe("initialLocale", () => {
  it("prefers the language the user last chose", () => {
    setBrowserLanguages(["en-US"]);
    rememberLocale("es");

    expect(initialLocale()).toBe("es");
  });

  it("ignores a stored language that Pelican does not have", () => {
    setBrowserLanguages(["es-MX"]);
    localStorage.setItem("locale", "fr");

    expect(initialLocale()).toBe("es");
  });

  it("takes the first of the browser's languages that Pelican has, without its region", () => {
    setBrowserLanguages(["fr-FR", "es-419", "en-US"]);

    expect(initialLocale()).toBe("es");
  });

  it("falls back to English", () => {
    setBrowserLanguages(["fr-FR", "de"]);

    expect(initialLocale()).toBe("en");
  });
});

describe("setLocale", () => {
  it("switches the interface, remembers the choice, and stores it on the account", () => {
    const i18n = testI18n();
    const { setLocale } = mountComposable(() => useLocale(), [i18n]);

    setLocale("es");

    expect(i18n.global.locale.value).toBe("es");
    expect(localStorage.getItem("locale")).toBe("es");
    expect(api.patch).toHaveBeenCalledWith("/api/settings/", { language: "es" });
  });

  it("keeps the choice when the account cannot store it", () => {
    vi.mocked(api.patch).mockRejectedValueOnce(new Error("403 Forbidden"));
    const i18n = testI18n();
    const { setLocale } = mountComposable(() => useLocale(), [i18n]);

    setLocale("es");

    expect(i18n.global.locale.value).toBe("es");
  });
});
