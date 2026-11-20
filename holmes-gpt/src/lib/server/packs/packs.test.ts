import { describe, expect, it } from "vitest";
import {
  HOLMES_COMPACT_PROMPT,
  HOLMES_SYSTEM_PROMPT,
  MODERN_COMPACT_PROMPT,
  MODERN_SYSTEM_PROMPT,
  TREATMENT_PROMPT,
} from "../prompts";
import { allPacks, defaultPack, getPack, isServable, servablePacks } from ".";

describe("teacher packs", () => {
  it("serves Holmes by default with exactly the prompts the app used before packs", () => {
    const pack = defaultPack();
    expect(pack.id).toBe("holmes");
    expect(pack.persona.full).toBe(HOLMES_SYSTEM_PROMPT);
    expect(pack.persona.compact).toBe(HOLMES_COMPACT_PROMPT);
    expect(pack.persona.modernFull).toBe(MODERN_SYSTEM_PROMPT);
    expect(pack.persona.modernCompact).toBe(MODERN_COMPACT_PROMPT);
    expect(pack.persona.treatment).toBe(TREATMENT_PROMPT);
  });

  it("never serves a pack that is in review or has no persona", () => {
    const hopkins = getPack("hopkins");
    expect(hopkins).toBeDefined();
    expect(isServable(hopkins!)).toBe(false);
    expect(servablePacks().map((p) => p.id)).toEqual(["holmes"]);
  });

  it("has unique ids", () => {
    const ids = allPacks().map((p) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

// Teacher policy §1–2, enforced on the recorded sources.
describe.each(allPacks().map((p) => [p.id, p] as const))(
  "pack %s sources",
  (_id, pack) => {
    it("names the teacher it belongs to", () => {
      expect(pack.sources.teacher).toBe(pack.name);
    });

    it("is a teacher who died at least 50 years ago", () => {
      expect(new Date().getFullYear() - pack.died).toBeGreaterThanOrEqual(50);
    });

    it("records at least one work", () => {
      expect(pack.sources.works.length).toBeGreaterThan(0);
    });

    it.each(pack.sources.works.map((w) => [w.slug, w] as const))(
      "%s has a valid public-domain record",
      (_slug, w) => {
        expect(w.sha256).toMatch(/^[0-9a-f]{64}$/);
        expect(w.words).toBeGreaterThan(0);
        expect(w.corpusFile).not.toMatch(/[\\/]/);

        // The basis must fit the year: "before 1931" only for pre-1931 printings,
        // the 1931–1963 renewal rule only inside that window, and nothing from
        // 1964 on, where renewal was automatic.
        if (w.pdBasis === "published-before-1931")
          expect(w.year).toBeLessThan(1931);
        if (w.pdBasis === "not-renewed") {
          expect(w.year).toBeGreaterThanOrEqual(1931);
          expect(w.year).toBeLessThanOrEqual(1963);
        }
        if (w.pdBasis === "published-without-notice") {
          expect(w.year).toBeGreaterThanOrEqual(1931);
          expect(w.year).toBeLessThanOrEqual(1977);
        }

        // A work the teacher only partly wrote must say so before anyone quotes it.
        if (w.authorship !== "teacher")
          expect(w.caveats?.length ?? 0).toBeGreaterThan(0);
      },
    );
  },
);
