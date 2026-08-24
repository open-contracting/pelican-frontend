<template>
  <header class="site_header">
    <div class="site_header_row">
      <RouterLink
        class="product"
        :to="{ name: 'home' }"
      >{{ $t("header") }}</RouterLink>

      <slot />

      <span
        v-if="settings.username"
        class="username"
      >{{ $t("signedInAs", { username: settings.username }) }}</span>

      <label
        class="visually-hidden"
        for="locale_select"
      >{{ $t("language") }}</label>
      <select
        id="locale_select"
        class="form-select locale_select"
        :value="locale"
        @change="setLocale(($event.target as HTMLSelectElement).value)"
      >
        <option
          v-for="(name, code) in LOCALES"
          :key="code"
          :value="code"
        >{{ name }}</option>
      </select>
    </div>
  </header>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useLocale } from "@/composables/useLocale";
import { LOCALES } from "@/config.js";
import { useSettingsStore } from "@/stores/settings.js";

const { locale, setLocale } = useLocale();
const { settings } = storeToRefs(useSettingsStore());
</script>

<style scoped lang="scss">
@import "@/scss/variables";

.site_header {
    padding: 10px 0 30px;
}

.site_header_row {
    align-items: center;
    display: flex;
    gap: 15px;
    justify-content: flex-end;
}

.product {
    color: $headings_light_color;
    font-family: $font-family-sans-serif;
    font-size: 15px;
    margin-right: auto;
    text-decoration: none;
}

.locale_select {
    font-size: 13px;
    width: auto;
}

.username {
    color: $headings_light_color;
    font-family: $font-family-thin;
    font-size: 13px;
}
</style>
