/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    screens: {
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
      "2xl": "1536px",
    },
    extend: {
      blur: {
        xs: '2px',
      },
      fontFamily: {
        grotesk: ["Grotesk", "sans-serif"],
      },
      fontWeight: {
        regular: 400,
        medium: 500,
      },
      colors: {
        green: "var(--green)",
        realgreen: "var(--realgreen)",
        lightgreen: "var(--lightgreen)",
        black: "var(--black)",
        dark: "var(--dark)",
        darkgray: "var(--darkgray)",
        gray: "var(--gray)",
        white: "rgba(255, 255, 255, <alpha-value>)",
      },
    },
  },
  plugins: [],
};
