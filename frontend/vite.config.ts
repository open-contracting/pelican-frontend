/// <reference types="vitest/config" />
import { fileURLToPath, URL } from "node:url";
import vue from "@vitejs/plugin-vue";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  // A proxy must authenticate every request, and must set the X-Remote-User header to the username.
  // Here, the dev server sets it without authenticating, trusting whoever runs it.
  const { VITE_REMOTE_USER = "dev", VITE_BACKEND_URL = "http://127.0.0.1:8000" } = loadEnv(mode, process.cwd(), "");

  return {
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
      // Django serves /static in development, for the administration site.
      proxy: Object.fromEntries(
        ["/api", "/admin", "/static"].map((path) => [
          path,
          { target: VITE_BACKEND_URL, headers: { "X-Remote-User": VITE_REMOTE_USER } },
        ]),
      ),
    },
    build: {
      sourcemap: true,
    },
    test: {
      environment: "happy-dom",
      setupFiles: ["./src/test/setup.ts"],
    },
  };
});
