import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import react from "@astrojs/react";

// Import the Vercel adapter
import vercel from '@astrojs/vercel';

// https://astro.build/config
export default defineConfig({
  site: "https://positivustheme.vercel.app",
  integrations: [tailwind(),react()],
  output: 'server',
  adapter: vercel(),
  server: {
    host: '127.0.0.1',  // 这里设置
    port: 4321,         // 这里设置
    allowedHosts: ['csi6220-1-vm4.ucd.ie']
  },
  build: {
    sourcemap: false,
    minify: true
  },
  vite: {
    server: {
      hmr: false,
    }
  },
  prefetch: true,
  devToolbar: {
    enabled: false // 完全禁用工具栏
  }
});