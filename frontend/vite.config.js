import path from "node:path";
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
                additionalData: '@import "@/scss/_variables.scss"; @import "@/scss/_breakpoints.scss";',
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
