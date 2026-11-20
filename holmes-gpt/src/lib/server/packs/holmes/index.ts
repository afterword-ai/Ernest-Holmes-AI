import type { Pack, PackSources } from "../types";
import sources from "./sources.json";
import {
  HOLMES_COMPACT_PROMPT,
  HOLMES_SYSTEM_PROMPT,
  MODERN_COMPACT_PROMPT,
  MODERN_SYSTEM_PROMPT,
  TREATMENT_PROMPT,
} from "../../prompts";

// The prompts still live in server/prompts.ts so this move changes nothing the
// model sees. Phase 2 (portrayal rules from the teacher policy) rewrites them
// here, per pack.
export const holmes: Pack = {
  id: "holmes",
  name: "Ernest Holmes",
  born: 1887,
  died: 1960,
  status: "available",
  summary: "Founder of Religious Science and author of The Science of Mind.",
  sources: sources as PackSources,
  persona: {
    full: HOLMES_SYSTEM_PROMPT,
    compact: HOLMES_COMPACT_PROMPT,
    modernFull: MODERN_SYSTEM_PROMPT,
    modernCompact: MODERN_COMPACT_PROMPT,
    treatment: TREATMENT_PROMPT,
  },
};
