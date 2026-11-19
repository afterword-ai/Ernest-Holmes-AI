import js from "@eslint/js";
import svelte from "eslint-plugin-svelte";
import globals from "globals";

// svelte.config.js is gone in SvelteKit 3; its contents moved into the
// sveltekit() plugin in vite.config.ts. eslint-plugin-svelte only needs the
// compiler options, and ours are "runes on for our own components" — which is
// every .svelte file this config lints, since node_modules is ignored.
const svelteConfig = { compilerOptions: { runes: true } };

export default [
  js.configs.recommended,
  ...svelte.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  {
    files: ["**/*.svelte", "**/*.svelte.js"],
    languageOptions: {
      parserOptions: {
        svelteConfig,
      },
    },
  },
  {
    ignores: ["build/", ".svelte-kit/", "node_modules/"],
  },
];
