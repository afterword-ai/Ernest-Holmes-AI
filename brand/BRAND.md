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

Ray counts were then measured rather than eyeballed — every gold shape was extracted as a connected component (the
rays do not touch the disc, so each is its own blob) and its centroid angle computed. The method was validated
against a render of the known five-ray tile, which it scored 5. The result corrected an earlier claim in this file:

| File | Rays | Spacing | Status |
|---|---|---|---|
| `assets/holmesai-icon-indigo.svg`, `Logo.svelte` | **7** | 30° | ✅ canonical master |
| `assets/holmesai-icon-tile-512/192/180.png` | **7** | 30.0°, 30.1°, 29.9°, 29.9°, 30.1°, 30.0° | ✅ **already canonical** |
| `assets/holmesai-icon-tile.svg` (= `static/favicon.svg`) | 5 | 45° | re-cut, see below |
| `assets/holmesai-icon-tile-48.ico` (= `static/favicon.ico`) | 5 | 45° | re-cut, see below |

**The raster ladder was never wrong.** `icon-512/192/180.png` carry the canonical seven-ray geometry, uniformly
scaled — fitting their bounding box against the master's gives the same scale factor in x and y to five decimal
places (1.60976 / 1.60968), which only happens if they were cut from that master. The touch icon and the PWA icons
have been correct all along. An earlier revision of this file called them "~9 rays"; that was an eyeball count off a
downscaled preview, and it was wrong.

The two files that *were* non-conforming are the SVG favicon and the `.ico` cut from it — the `.ico` matched a
48 px render of the five-ray tile at RMS 7.6 against 48.8 for the seven-ray one, which settles its lineage.

### The re-cut (2026-11-18)

Ryan approved re-cutting. `static/favicon.svg` and `static/favicon.ico` — and their copies in `assets/` — are now
the seven-ray drawing. **The raster ladder was deliberately left untouched**, because it was already canonical and
re-rendering correct files only churns bytes and risks a quality regression.

This was composition, not drawing. The ray geometry is the master's verbatim; the container (`512×512`, `rx="112"`,
`#3B2A6B`) and the white book are the existing tile's; and the placement transform was *fitted to the shipped
`icon-512.png`* rather than invented — `translate(95.025 73.501) scale(1.60972)`, derived from that file's measured
bounding box. The rendered result differs from the shipped PNG in 0.48% of pixels at a mean absolute difference of
0.5/255, i.e. antialiasing only. The SVG favicon now agrees with the icons it always should have matched.

**One honest cost.** Seven thin rays survive 48 px and 32 px, but at **16 px they merge into a gold mound** — the
five-ray drawing, having fewer and fatter rays, held up slightly better there. This is the brand's own minimum-size
rule (below 24 px the rays merge) showing up in the favicon, and it is the price of the canonical drawing. If the
16 px favicon matters more than drawing fidelity, that is a new decision for Ryan, not something to quietly revert.

### Variants and which ground each is for

Artwork lives in [`assets/`](assets/). Every file except the re-cut tile and `.ico` is a byte-identical copy of what
ships; nothing was redrawn, recoloured or cropped.

**Every variant below is the canonical seven-ray drawing.**

| File | What it is | Use on |
|---|---|---|
| `holmesai-icon-tile.svg` | Indigo rounded-square tile, white book, gold sun. Self-grounded. | **Any ground.** The app icon, and the safe choice when the background is unknown or not ours (a helpdesk, a directory, an OAuth consent screen). |
| `holmesai-icon-indigo.svg` | Indigo book, gold sun, transparent ground. | **Light grounds only.** Paper, white, the light theme. |
| `holmesai-icon-tile-512.png` `-192` `-180` | Raster ladder of the tile. Canonical since before this document. | PWA icons, touch icon — where SVG is not accepted. |
| `holmesai-icon-tile-48.ico` | 16/32/48 px frames, re-cut from the tile. | The favicon. At 16 px the rays merge; see the re-cut note above. |
| `legacy-*` | The pre-redesign serif lockup and its square icon. | **Nothing new.** Kept for provenance; see *What is inconsistent* below. |

The in-product mark is not a file at all: `Logo.svelte` draws it inline and fills the book from `--logo-body`, which
is indigo on light and **white** on dark. That inline form is the only one that adapts to the page it sits on.

**For a dark or unknown ground, use the tile.** It is self-grounded — white book on its own indigo plate — so it
does not care what is behind it, and it is now the canonical drawing at every size. There is still no *transparent*
white-book file, and there does not need to be one: a transparent mark on a ground you do not control is the
failure mode the tile exists to prevent. If some surface genuinely needs a transparent white-book variant, that is a
question for Ryan, not a gap to fill here.

### Who else holds a copy

The mark is consumed outside this repository, and those consumers hold **byte-copies, not references**. A copy does
not know when the master changes, so anything that alters the tile has to be pushed to this list by hand:

| Consumer | What it holds | Where |
|---|---|---|
| OpenBroom support desk (`support.ernestholmes.us`) | `holmesai-icon-tile.svg`, copied byte-for-byte and served from the desk's own origin as `/brand/ernestholmes.svg`; also its favicon | `~/Sites/OpenBroom/support` |

The desk deliberately serves its own copy rather than hot-linking `ernestholmes.us`, so that the desk's branding
does not break if this site moves a path. That is the right trade, and the cost is this table: **re-cut the mark and
the desk keeps the old one until someone re-copies it.**

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

1. ~~**The mark is drawn three ways.**~~ **Resolved.** It was drawn two ways, not three: the seven-ray master
   (`Logo.svelte`, `Holmes-AI-mark.svg`, and the PNG icon ladder) and the five-ray `favicon.svg` with the `.ico` cut
   from it. Ryan ruled seven rays canonical on 2026-11-18 and the two non-conforming files were re-cut the same day.
   See *The canonical drawing* above for the measurements.
3. **The legacy lockup is still in the repo and still in the OG image.** `Holmes-AI-logo-horizontal.png`,
   `Holmes-AI-logo.png` and `og-default.png` carry the pre-redesign serif wordmark and a twelve-ray sun. Nothing in
   `src/` references them, but `og-default.png` is the shape of the file social cards expect, so the old brand is one
   careless `og:image` away from shipping.
4. **The About page points its `og:image` at a host that is not the brand host** — `holmes-ai.netdevs.net` — and at
   `holmes-ai-about.jpg`, which is not in `static/`.
5. ~~**No dark-ground mark file exists.**~~ **Withdrawn — this was wrong.** The tile is self-grounded and, as
   measured above, the PNG ladder was already the canonical drawing. A correct mark for a dark or unknown ground
   existed the whole time; the earlier claim came from the same mis-count as item 1.
6. **`static/images/logo.ico` duplicates the old `static/favicon.ico`** at the same 48 px. Nothing references it, and
   it was *not* re-cut, so it is now a stale copy of the five-ray drawing. Delete it rather than updating it.

Items 3, 4 and 6 are not visible on ernestholmes.us today in the light or dark theme — the live CSS matches
`src/app.css` token for token, verified against the deployed stylesheet. They are latent.

## Where this lives, and why

In the product repository, at `brand/`, rather than as a sibling of `~/Sites/aibacus_brand/`.

`aibacus_brand/` is a separate folder because Aibacus' identity spans decks, investor material and several surfaces
that have no single repository. HolmesAI is one product in one repository, the artwork already ships from
`holmes-gpt/static/`, and the tokens have to stay in lockstep with `src/app.css`. A sibling folder would drift from
the CSS within a release. Keeping the system beside the code it describes means a change to either shows up in the
same diff.
