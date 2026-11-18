# HolmesAI — Brand

HolmesAI is "Ask Ernest Holmes": a conversational practitioner in the tradition of Ernest Holmes, founder of
Religious Science and author of *The Science of Mind*. It lives at **ernestholmes.us**, with a support desk at
**support.ernestholmes.us**.

This file is the source of truth for the identity. It was written by reading what the product actually ships —
`holmes-gpt/src/app.css`, `holmes-gpt/src/lib/components/Logo.svelte` and `holmes-gpt/static/` after the redesign that
landed in PR #19 — not by deciding what the brand ought to be. Where the shipped artwork disagrees with itself, this
file says so rather than picking a winner.

The design system (tokens, type scale, component conventions) is [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md). The token
files `holmesai_tokens.css` and `holmesai_tokens.json` are the machine-readable form. `holmes-gpt/src/app.css` is
currently the live definition and these tokens are transcribed from it — change one and change the other, or the next
surface built from this folder will disagree with the site.

## The idea

A sun rising out of an open book. The book is the *Science of Mind* text; the sun is the realisation that comes from
reading it. Holmes' own language is the brief: light, not fire. The mark is calm, frontal and symmetrical, and that
restraint is the brand — this is a teacher, not a product launch.

Indigo is the ground and the mark's body. Gold is the sun and the one accent. There is no third colour. Everything
else on the page is paper, ink and a decorative pastel wash that carries no meaning.

## The mark

**Name:** the Book Sunrise. Two facing pages below, a gold disc with rays above, no containing shape.

### The canonical drawing: seven rays

Ryan ruled on 2026-11-18 that the **seven-ray drawing is canonical** — the one in `Logo.svelte` and
`assets/holmesai-icon-indigo.svg`: seven rays fanned over 180°, disc radius 26, rays at radius 40, in the mark's own
200-unit coordinates.

Every other ray count in the repository is therefore **non-conforming artwork awaiting a re-cut**, not an
alternative:

| File | Rays | Status |
|---|---|---|
| `assets/holmesai-icon-indigo.svg`, `Logo.svelte` | **7** | ✅ canonical master |
| `assets/holmesai-icon-tile.svg` (= `static/favicon.svg`) | 5 | ⚠️ re-cut from the master |
| `assets/holmesai-icon-tile-512/192/180.png`, `-48.ico` | ~9 | ⚠️ re-cut from the master |

Re-cutting means compositing the seven-ray master into the existing indigo tile and re-rendering the raster ladder
from it. That is artwork generation, so it is **not done here** — it needs either the original vector source or
Ryan's explicit go-ahead, and it belongs to whoever owns the artwork. Until it happens, the tile and the raster
ladder stay in use because they are what ships and a product with no mark is worse than a product with a slightly
wrong one; they are simply known to be wrong.

**What the gap costs, practically.** The canonical seven-ray file has a **transparent ground and is light-grounds
only**. The only self-grounded artwork — the thing that survives a dark or unknown background — is the five-ray
tile. So until a seven-ray tile exists:

> **There is no correct mark for a dark or unknown ground.**

Every such placement is a choice between the right drawing on the wrong ground and the wrong drawing on the right
one. Any surface that themes itself dark, or that the brand does not control, hits this. Where the ground can be
pinned light, the canonical file is correct and should be used; where it cannot, say so rather than guessing.

### Variants and which ground each is for

Artwork lives in [`assets/`](assets/). The files are copies of what ships; none of them was redrawn here.

| File | What it is | Use on |
|---|---|---|
| `holmesai-icon-tile.svg` | Indigo rounded-square tile, white book, gold sun. Self-grounded. | **Any ground.** The app icon, and the safe choice when the background is unknown or not ours (a helpdesk, a directory, an OAuth consent screen). |
| `holmesai-icon-indigo.svg` | Indigo book, gold sun, transparent ground. | **Light grounds only.** Paper, white, the light theme. |
| `holmesai-icon-tile-512.png` `-192` `-180` `-48.ico` | Raster ladder of the tile. | PWA icons, touch icon, favicon — where SVG is not accepted. |
| `legacy-*` | The pre-redesign serif lockup and its square icon. | **Nothing new.** Kept for provenance; see *What is inconsistent* below. |

The in-product mark is not a file at all: `Logo.svelte` draws it inline and fills the book from `--logo-body`, which
is indigo on light and **white** on dark. That is the correct dark-ground treatment, but it exists only as a CSS
variable, not as artwork. **There is no white-book SVG or PNG to hand to anything outside the app.** Exporting one is
a question for Ryan, not a gap to fill here.

### Rules

- **Never redraw, recolour, crop or rotate the mark.** Use the files as they are. The rays' angles, the disc radius
  and the page curve are the drawing; a mark rebuilt by eye is a different mark.
- **The sun is always gold `#F7B500`.** It does not invert, tint, or follow the theme. Only the book changes ink.
- **The book follows the ground, never the other way round.** Indigo on light, white on dark. An indigo book on a
  dark ground disappears; that is the single most likely mistake.
- **Clear space: the radius of the sun's disc** (26 units in the mark's own coordinates, ≈ 16% of the mark's height)
  on all four sides. Nothing — type, rule, edge, another logo — enters it.
- **Minimum size: 24 px tall** for the transparent mark, **32 px** for the tile, where the rounded corner and the
  white book still read. Below 24 px the rays merge into the disc; use the tile, or no mark at all.
- **Never put the transparent mark on gold, on a photograph, or on the decorative backdrop wash.** It needs a plain
  light ground or its own tile.
- **Never add a containing shape, outline, shadow or glow** to the transparent mark. The tile is the only approved
  container.
- **The wordmark is live type, not artwork.** "HolmesAI" is set in Satoshi Bold with the tagline "Ernest Holmes AI
  Practitioner" in Satoshi at `0.75rem` in `--ink-3` beneath it. There is no horizontal lockup file for the current
  brand — the header composes mark + type at run time. The serif `legacy-holmesai-horizontal.png` is the *old*
  wordmark and must not be used as the current one.

## Colour, in one paragraph

Indigo `#3B2A6B` is the brand. It is the app-icon tile, the `theme-color`, the book. Gold `#F7B500` is the sun and
nothing else at full strength — as *text* or *UI accent* it is always a darkened or lightened derivative, because
`#F7B500` on white is 1.8:1 and unreadable. The page itself is warm paper and near-black ink. The full token set,
with the contrast behaviour that makes gold safe, is in [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) §Colour.

Three rules the compiler cannot enforce:

- **Gold is never text on a light ground.** Use `--accent` (`#8A5D00`), which is the same hue darkened to 5.5:1 on
  paper. `#F7B500` and `#E8B100` are fills and strokes only.
- **Gold is never a status.** There is no gold "warning". Status comes from `--danger` and `--success`, and gold
  stays the brand.
- **A colour is never the only signal.** Focus is a 2 px gold outline *and* an offset; the active nav item is
  `--ink` *and* `aria-current`.

## Voice

Plain, warm, unhurried, second person. Holmes' own register: declarative rather than hedged, instructive rather than
salesy. No exclamation marks, no "unlock", no "revolutionise". The product calls itself an *AI practitioner* and is
explicit that it is not Ernest Holmes — the identity never implies otherwise, and the mark is never presented as his
signature or portrait.

## What is inconsistent today

Found while reading the shipped artwork. Recorded, not fixed — each is a decision for Ryan.

1. **The mark is drawn three ways, with different ray counts.** `Logo.svelte` and `static/images/Holmes-AI-mark.svg`
   draw **7 rays** over 180°, disc r=26, rays at radius 40. `static/favicon.svg` — the app icon and the tile in this
   folder — draws **5 rays**, at radius 38, with heavier ray geometry. `icon-192/512.png` and
   `apple-touch-icon-180.png` show roughly **nine** and predate `favicon.svg`. The in-product mark, the favicon and
   the home-screen icon are three different pictures. **Resolved as to which is canonical** — seven rays, see above —
   but the re-cut of the other two has not been done.
3. **The legacy lockup is still in the repo and still in the OG image.** `Holmes-AI-logo-horizontal.png`,
   `Holmes-AI-logo.png` and `og-default.png` carry the pre-redesign serif wordmark and a twelve-ray sun. Nothing in
   `src/` references them, but `og-default.png` is the shape of the file social cards expect, so the old brand is one
   careless `og:image` away from shipping.
4. **The About page points its `og:image` at a host that is not the brand host** — `holmes-ai.netdevs.net` — and at
   `holmes-ai-about.jpg`, which is not in `static/`.
5. **No dark-ground mark file exists.** See above.
6. **`static/images/logo.ico` duplicates `static/favicon.ico`** at the same 48 px; only the latter is referenced.

None of these are visible on ernestholmes.us today in the light or dark theme — the live CSS matches
`src/app.css` token for token, verified against the deployed stylesheet. They are latent.

## Where this lives, and why

In the product repository, at `brand/`, rather than as a sibling of `~/Sites/aibacus_brand/`.

`aibacus_brand/` is a separate folder because Aibacus' identity spans decks, investor material and several surfaces
that have no single repository. HolmesAI is one product in one repository, the artwork already ships from
`holmes-gpt/static/`, and the tokens have to stay in lockstep with `src/app.css`. A sibling folder would drift from
the CSS within a release. Keeping the system beside the code it describes means a change to either shows up in the
same diff.
