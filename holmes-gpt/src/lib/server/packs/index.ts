import { holmes } from "./holmes";
import { hopkins } from "./hopkins";
import type { Pack, PackPersona } from "./types";

export type { Pack, PackPersona, PackSource, PackSources } from "./types";

const PACKS: readonly Pack[] = [holmes, hopkins];

/** The pack ernestholmes.us serves. Until the picker lands, every conversation uses it. */
export const DEFAULT_PACK_ID = "holmes";

export function allPacks(): readonly Pack[] {
  return PACKS;
}

export function getPack(id: string): Pack | undefined {
  return PACKS.find((p) => p.id === id);
}

/** A pack may hold a conversation only when it is available and has a persona. */
export function isServable(
  pack: Pack,
): pack is Pack & { persona: PackPersona } {
  return pack.status === "available" && pack.persona !== undefined;
}

export function servablePacks(): (Pack & { persona: PackPersona })[] {
  return PACKS.filter(isServable);
}

export function defaultPack(): Pack & { persona: PackPersona } {
  const pack = getPack(DEFAULT_PACK_ID);
  if (!pack || !isServable(pack)) {
    throw new Error(
      `Default pack "${DEFAULT_PACK_ID}" is missing or not servable`,
    );
  }
  return pack;
}
