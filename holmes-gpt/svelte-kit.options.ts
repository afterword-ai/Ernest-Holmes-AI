import adapter from "@sveltejs/adapter-node";
import type { Config } from "@sveltejs/kit/vite";

/**
 * Options for the `sveltekit()` Vite plugin.
 *
 * SvelteKit 3 removed `svelte.config.js` and takes configuration through the
 * plugin instead. Both `vite.config.ts` and `vitest.config.ts` instantiate that
 * plugin, so the options live here rather than being written out twice: when
 * only the Vite config carried the `$lib` alias, every test that imported
 * through `$lib` failed while the build still passed.
 */
export const kitOptions: Config = {
  adapter: adapter(),

  // SvelteKit 3 renamed `$lib` to `#lib`. Keeping the alias so the upgrade
  // stays a framework change rather than a rename across every import;
  // migrating to `#lib` is worth doing on its own, separately.
  alias: { $lib: "src/lib" },

  // Force runes for our own components only; leave node_modules alone.
  dynamicCompileOptions: ({ filename }) =>
    filename.includes("node_modules") ? undefined : { runes: true },

  // Moved verbatim from the old svelte.config.js. The headers the app serves
  // are unchanged; the upgrade PR records the before/after comparison.
  csp: {
    mode: "auto",
    directives: {
      "default-src": ["self"],
      "script-src": ["self"],
      "style-src": ["self", "unsafe-inline"],
      "img-src": ["self", "data:"],
      "font-src": ["self"],
      "connect-src": ["self"],
      "frame-ancestors": ["self"],
      "base-uri": ["self"],
      "form-action": ["self"],
    },
  },
};
