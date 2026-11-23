import type { Pack, PackSources } from "../types";
import sources from "./sources.json";

// In review: sources are recorded, the portrayal is not written yet. With no
// persona the loader never serves this pack to a conversation.
export const hopkins: Pack = {
  id: "hopkins",
  name: "Emma Curtis Hopkins",
  born: 1849,
  died: 1925,
  status: "in-review",
  summary:
    "New Thought teacher whose students went on to found much of the movement.",
  sources: sources as PackSources,
};
