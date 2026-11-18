import type { Quote } from "$lib/types/chat";
import quotesData from "$lib/data/knowledge/quotes.json";

/**
 * Attribution note — read before changing `SOURCE`.
 *
 * These lines are NOT verbatim Ernest Holmes. They were composed for this
 * project in the idiom of his Science of Mind writing (see
 * `src/lib/data/knowledge/*.json` → `metadata.provenance`). Earlier versions of
 * this file attributed them to "The Science of Mind", which presented authored
 * paraphrase to users as quotation from a specific published edition.
 *
 * Until the lines are replaced with quotations sourced to a real page and
 * edition, they must be surfaced as what they are.
 */
const SOURCE = "in the Science of Mind tradition";

/**
 * Bundled at build time rather than read from disk.
 *
 * The previous loader did `readFileSync(join(process.cwd(), "downloads",
 * "training_data", ...))`. Those files ARE tracked in git (they were committed
 * before `downloads/` was added to .gitignore, and ignoring a path does not
 * untrack it) and the Dockerfile copied them in deliberately, so this was never
 * broken. But it made the quote list a runtime filesystem read keyed to the
 * process working directory, kept alive by a `COPY` line in the Dockerfile and
 * a `!downloads/training_data/` carve-out in .dockerignore. It also silently
 * degraded to an empty list if the path was ever wrong, and its first-choice
 * file, `holmes_powerful_quotes.json`, has never existed in this repo.
 *
 * A static import removes all of that: the data is part of the bundle, and a
 * missing file is a build error rather than a quiet empty panel.
 */
const quotes: Quote[] = (quotesData.quotes as string[]).map((quote) => ({
  quote,
  source: SOURCE,
}));

export function allQuotes(): Quote[] {
  return quotes;
}

/** Fisher–Yates; the old `sort(() => 0.5 - Math.random())` is biased. */
export function shuffle<T>(items: readonly T[]): T[] {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

const STOP_WORDS = new Set([
  "that",
  "this",
  "with",
  "have",
  "from",
  "what",
  "does",
  "about",
  "would",
  "could",
  "should",
  "there",
  "their",
  "which",
  "when",
  "your",
  "into",
  "than",
  "then",
  "them",
  "were",
  "been",
  "being",
  "will",
  "just",
  "like",
  "really",
]);

function words(text: string): string[] {
  return text
    .toLowerCase()
    .split(/[^a-z']+/)
    .filter((w) => w.length > 3 && !STOP_WORDS.has(w));
}

/** Picks the quotes that share the most vocabulary with the question. */
export function relevantQuotes(question: string, max: number): string[] {
  if (max <= 0) return [];
  const pool = allQuotes();
  if (pool.length === 0) return [];

  const terms = new Set(words(question));
  const scored = pool
    .map((q) => {
      const text = q.quote.toLowerCase();
      let score = 0;
      for (const term of terms) if (text.includes(term)) score += 2;
      return { quote: q.quote, score };
    })
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, max)
    .map((s) => s.quote);

  return scored.length > 0
    ? scored
    : shuffle(pool)
        .slice(0, max)
        .map((q) => q.quote);
}
