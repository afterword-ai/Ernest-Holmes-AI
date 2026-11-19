import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";
import { kitOptions } from "./svelte-kit.options";

export default defineConfig({
  // Same options as the build: a plugin configured differently here meant tests
  // resolved imports differently from production, which is how the $lib alias
  // was missed during the SvelteKit 3 upgrade.
  plugins: [sveltekit(kitOptions)],
  test: {
    include: ["src/**/*.{test,spec}.{js,ts}"],
    environment: "node",
  },
});
