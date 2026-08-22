<template>
  <header class="site_header">
    <RouterLink
      class="product"
      :to="{ name: 'home' }"
    >{{ $t("header") }}</RouterLink>

    <!-- #188 hangs the signed-in reader and a sign-out control here. -->

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
  </header>
</template>

<script setup lang="ts">
import { useLocale } from "@/composables/useLocale";
import { LOCALES } from "@/config.js";

const { locale, setLocale } = useLocale();
</script>

<style scoped lang="scss">
@import "@/scss/variables";

// No horizontal padding, so the header lines up with the content below it.
.site_header {
    align-items: center;
    display: flex;
    gap: 15px;
    justify-content: flex-end;
    padding: 10px 0;
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
</style>
