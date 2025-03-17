import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";

// Import the Vercel adapter
import vercel from '@astrojs/vercel';

// https://astro.build/config
export default defineConfig({
  site: "https://positivustheme.vercel.app",
  integrations: [tailwind()],
  output: 'server',
  adapter: vercel(),
  server: {
    allowedHosts: ['csi6220-1-vm4.ucd.ie']
  }
});