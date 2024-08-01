import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path';

export default defineConfig({
    root: __dirname,
    cacheDir: "./node_modules/.vite/.",

    server: {
        port: 4200,
        host: "localhost",
    },

    preview: {
        port: 4300,
        host: "localhost",
    },

    plugins: [react()],
    resolve: {
        alias: {
            "@modules": path.resolve(__dirname, "src", "core"),
        },
    },

    build: {
        outDir: "./dist/frontend",
        reportCompressedSize: true,
        commonjsOptions: {
            transformMixedEsModules: true,
        },
    },
});