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
