import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { TDesignResolver } from 'unplugin-vue-components/resolvers';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue(),
	AutoImport({
		resolvers: [TDesignResolver({
			library: 'vue-next'
		})],
	}),
	Components({
		resolvers: [TDesignResolver({
			library: 'vue-next'
		})],
	}),],
	build: {
		chunkSizeWarningLimit: 500,
		cssCodeSplit: false,
		rollupOptions: {
			output: {
				manualChunks: {
					vue: ["vue", "vue-router"],
					icons: ["tdesign-icons-vue-next"],
				},
				chunkFileNames: "assets/index-[hash].js",
			},
		},
		brotliSize: false,
	},
	server: {
		proxy: {
			'/api': {
				target: 'http://127.0.0.1:5000',
				changeOrigin: true,
			},
		},
	},
})
