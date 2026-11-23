// A teacher pack: one historical teacher's eligible works plus the portrayal
// built on them. See policy/TEACHER-POLICY.md at the repository root for what
// may become a pack and how the app may present it.

/** Why a work is in the US public domain. Recorded per work, never assumed. */
export type PublicDomainBasis =
  /** Published in the US before 1 January 1931 (95-year term has run). */
  | "published-before-1931"
  /** Published 1931–1977 with no copyright notice (1909 Act: PD on publication). */
  | "published-without-notice"
  /** Published 1931–1963 and no renewal was found in the renewal records. */
  | "not-renewed";

/** Whether the teacher wrote the whole work or only part of it. */
export type Authorship = "teacher" | "introduction-only";

export interface PackSource {
  slug: string;
  title: string;
  /** Author as printed on the title page. */
  author: string;
  /** Year of the printing the text was taken from. */
  year: number;
  edition?: string;
  pages?: number;
  words: number;
  /** sha256 of the cleaned corpus file, so a citation can be tied to an exact text. */
  sha256: string;
  pdBasis: PublicDomainBasis;
  authorship: Authorship;
  sourceUrl?: string;
  /** File name inside the pack's corpus folder (kept outside this repo). */
  corpusFile: string;
  /** Anything a reviewer must know before quoting from this work. */
  caveats?: string[];
}

export interface PackSources {
  teacher: string;
  /** Where the cleaned texts live. Outside any git tree, by design. */
  corpusRoot: string;
  note?: string;
  works: PackSource[];
}

export interface PackPersona {
  /** Full and compact prompts for the teacher speaking in their own voice. */
  full: string;
  compact: string;
  /** Full and compact prompts for the plain-language "modern guide" style. */
  modernFull: string;
  modernCompact: string;
  /** Prompt for the treatment / practice writer, when the pack offers one. */
  treatment?: string;
}

export type PackStatus = "available" | "in-review";

export interface Pack {
  id: string;
  name: string;
  born: number;
  died: number;
  status: PackStatus;
  /** One factual line, safe for a teacher card. */
  summary: string;
  sources: PackSources;
  /** Absent until the pack's portrayal has been written and reviewed. */
  persona?: PackPersona;
}
