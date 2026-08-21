import { fileURLToPath, URL } from "node:url";
import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          whitespace: "preserve",
        },
      },
    }),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        // Variables and mixins only, so that components can use them without emitting Bootstrap's CSS.
        // Ours come first, so Bootstrap's !default values do not override them.
        additionalData:
          '@import "@/scss/_variables.scss"; @import "@/scss/_breakpoints.scss"; @import "bootstrap/scss/functions"; @import "bootstrap/scss/variables"; @import "bootstrap/scss/mixins";',
        // @use depends on Bootstrap 6. https://github.com/twbs/bootstrap/issues/29853
        silenceDeprecations: ["import"],
        quietDeps: true,
      },
    },
  },
  server: {
    port: 8080,
  },
  build: {
    sourcemap: true,
  },
});
