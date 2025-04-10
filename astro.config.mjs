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
    allowedHosts: ['csi6220-1-vm4.ucd.ie'],
    hmr: false
  }
});