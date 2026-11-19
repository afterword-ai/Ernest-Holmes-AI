# HolmesAI — Design System v1

Everything here is transcribed from what ships: `holmes-gpt/src/app.css` (the live definitions), the Svelte
components in `holmes-gpt/src/lib/components/`, and the deployed stylesheet at ernestholmes.us, which was fetched and
compared token for token. Where this document states a rule that the CSS does not enforce, the rule is marked as such.

The identity and the mark rules are in [BRAND.md](BRAND.md). The machine-readable form is
[`holmesai_tokens.css`](holmesai_tokens.css) and [`holmesai_tokens.json`](holmesai_tokens.json).

**The stack:** SvelteKit + Tailwind v4. Tokens are plain CSS custom properties on `:root`, re-exported to Tailwind
through `@theme inline` so `bg-paper`, `text-ink-3`, `border-line` work as utilities. Nothing is hard-coded in
components; a hex in a `.svelte` file is a bug.

---

## 1. Themes

Two themes, both first-class. `data-theme` on `<html>` is resolved before first paint by an inline script in
`app.html` reading `localStorage["holmes:theme"]` (`light` | `dark` | `system`), so there is no flash.

- **Light — "paper."** A warm off-white page under a four-corner pastel mesh (coral, pink, periwinkle, sky). Airy.
- **Dark — "twilight."** Deep teal-navy glass over a warm ember glow rising from the bottom edge.

The dark theme is **not** the light theme inverted. The paper is warm, the dark ground is cool, and the accent swaps
from a dark gold to a bright one. Anything built for one theme must be checked in the other.

---

## 2. Colour

### 2.1 Brand constants

These do not change with theme.

| Token | Hex | Role |
|---|---|---|
| `--logo-sun` | `#F7B500` | The sun in the mark. Never text. |
| *(brand indigo)* | `#3B2A6B` | The mark's body on light, the app-icon tile, `<meta name="theme-color">`. |

`--logo-body` is the one logo token that *does* flip: `#3B2A6B` on light, `#FFFFFF` on dark.

### 2.2 Semantic tokens

| Token | Light | Dark | Role |
|---|---|---|---|
| `--paper` | `#FAF9F7` | `#061A28` | Page ground, under the backdrop. |
| `--surface` | `#FFFFFF` | `#0F2A3D` | Opaque panels. |
| `--surface-glass` | `rgba(255,255,255,.72)` | `rgba(18,40,58,.62)` | Blurred chrome: header, chips, cards over the backdrop. |
| `--surface-sunken` | `#F1EFEC` | `rgba(255,255,255,.05)` | Inputs, soft buttons, wells. |
| `--ink` | `#0E0E11` | `#F3F6F9` | Primary text, headings. |
| `--ink-2` | `#34343D` | `#D3DCE6` | Body copy, long form. |
| `--ink-3` | `#4B4B57` | `#B0BDCB` | Muted: captions, placeholders, the tagline. |
| `--line` | `rgba(14,14,17,.12)` | `rgba(255,255,255,.14)` | Hairlines. |
| `--line-strong` | `rgba(14,14,17,.18)` | `rgba(255,255,255,.30)` | Input borders, hover borders. |
| `--accent` | `#8A5D00` | `#F4C24A` | **Gold as text.** Contrast-safe on its own ground. |
| `--accent-bright` | `#E8B100` | `#FFD36B` | **Gold as fill/stroke.** Selection, underline hover, emphasis. |
| `--focus` | `#B07A00` | `#F4C24A` | Focus ring. |
| `--btn-bg` / `--btn-ink` | `#0E0E11` / `#FFFFFF` | `#F3F6F9` / `#061A28` | Primary button. |
| `--user-bubble` / `--user-ink` | `#0E0E11` / `#FFFFFF` | `#F3F6F9` / `#061A28` | The user's own chat turn. |
| `--danger` | `#B42318` | `#FF8A7A` | Errors, destructive. |
| `--success` | `#12703B` | `#6FDC9A` | Confirmations. |

### 2.3 Contrast behaviour — the part that matters

Gold is the brand's weak point and the token set is built around it. **There are two golds and they are not
interchangeable.**

| Pair | Ratio | Verdict |
|---|---|---|
| `#8A5D00` on `#FAF9F7` (light `--accent`) | **5.5:1** | ✅ AA for body text |
| `#F4C24A` on `#061A28` (dark `--accent`) | **11.1:1** | ✅ AAA |
| `#F7B500` on `#FFFFFF` | **1.8:1** | ❌ never text, never a thin line |
| `#0E0E11` on `#F7B500` | **11.6:1** | ✅ this is how to use full gold — dark ink *on* it |
| `#FFFFFF` on `#3B2A6B` (brand indigo) | **11.9:1** | ✅ the indigo's text pairing is white |

Rules:

- `--accent` is for text and icons. `--accent-bright` is for fills, strokes and `color-mix()` washes. Swapping them
  is the standard way to break contrast here.
- **Never white-on-gold.** If something must sit on `#F7B500`, it is `--ink`.
- Gold is never a status colour, and no status is ever gold. `--danger` and `--success` own that job.
- `prefers-contrast: more` is handled: `--ink-2` collapses to `--ink`, `--ink-3` to `--ink-2`, `--line` to
  `--line-strong`. Keep new tokens inside that ladder so the override keeps working.
- Colour is never the only signal. Focus = ring + 3 px offset. Active nav = `--ink` + `aria-current="page"`.

### 2.4 The backdrop

`--backdrop` is a fixed, `z-index: -1`, `pointer-events: none` layer (`.backdrop`) of stacked radial gradients over
`--paper`. It is **decoration with no meaning** — never put information in it, never read a colour off it, never place
the transparent mark or unboxed text directly on it. Content sits on `--surface-glass` above it.

---

## 3. Type

**Satoshi**, self-hosted variable (`static/fonts/Satoshi-Variable.woff2` + italic), weights 300–900,
`font-display: swap`, under the ITF Free Font License (`static/fonts/FFL.txt`). There is no second family — no serif,
no mono. The legacy serif wordmark is artwork, not a typeface the brand owns.

```
--font-sans: "Satoshi", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
```

| Role | Size | Line height | Tracking | Weight |
|---|---|---|---|---|
| Display (hero) | `clamp(2.25rem, 1.2rem + 4.6vw, 4.25rem)` | `1.04` | `-0.035em` | 600 |
| `h1`–`h4` | Tailwind scale | `1.15` | `-0.02em` | 600 |
| Body | `1rem` | `1.6` | — | 400 |
| Long form (`.prose-holmes`) | `1rem` | `1.7` | — | 400, `--ink-2` |
| Button | `0.9375rem` | `1` | — | 500 |
| Small button / meta | `0.8125rem` | — | — | — |
| Caption, tagline | `0.75rem` | — | — | — |
| Eyebrow (`.eyebrow`) | `0.75rem` | — | `0.12em`, uppercase | 600, `--ink-3` |

Headings are tight (`-0.02em`); the display is tighter (`-0.035em`); nothing else is tracked except the eyebrow,
which is loose and uppercase. Body copy is never tracked and never uppercase.

`.prose-holmes` is the long-form block used by About, Privacy, Support and chat answers: `--ink-2` at `1.7`,
`0.9em` between blocks, `strong` promoted to `--ink` at 700, links underlined at `--line-strong` with a 3 px offset
that warms to `--accent-bright` on hover.

---

## 4. Space, radius, elevation

**Spacing** is Tailwind's 4 px scale, used as utilities. Page gutters step `1rem → 2rem → 3rem`
(`px-4 sm:px-8 lg:px-12`) inside `max-w-7xl`. Header height is the token `--header-h: 4rem`; sticky things offset from
it, never from a literal `64px`.

**Radius** — only three values exist:

| Token | Value | For |
|---|---|---|
| `--radius-card` | `1.5rem` | Cards, panels, dialogs |
| *(field)* | `0.9rem` | Inputs and textareas |
| `--radius-pill` | `999px` | Buttons, chips, toggles |

Buttons are pills. Cards are generously round. Inputs sit between. There is no square corner in this UI.

**Elevation** — three shadows, both themes. Light shadows are blue-tinted and soft; dark shadows are plain black and
deeper.

| Token | Light | Dark |
|---|---|---|
| `--shadow-sm` | `0 1px 2px rgba(20,20,30,.05), 0 1px 1px rgba(20,20,30,.03)` | `0 1px 2px rgba(0,0,0,.3)` |
| `--shadow-md` (`--shadow-card`) | `0 8px 30px rgba(30,30,60,.08), 0 1px 3px rgba(30,30,60,.05)` | `0 10px 34px rgba(0,0,0,.35)` |
| `--shadow-lg` (`--shadow-float`) | `0 24px 60px rgba(30,30,70,.16), 0 4px 12px rgba(30,30,70,.06)` | `0 28px 70px rgba(0,0,0,.5)` |

---

## 5. Components

Defined in `@layer components` in `app.css`. Build with these before writing new CSS.

### `.glass`
`--surface-glass` + 1 px `--line` + `blur(22px) saturate(1.4)` + `--shadow-md`. The house surface: header, chips,
floating panels. It assumes the backdrop is behind it — on a plain `--surface` ground it reads as a flat tint.

### `.card`
`--radius-card`, `1.25rem` padding. Carries no background of its own; compose with `.glass` or `bg-surface`.

### `.btn` + variant
Pill, `min-height: 2.75rem`, `0 1.25rem`, weight 500, `0.9375rem`, `scale(.97)` on press, `opacity .45` disabled.

| Variant | Appearance |
|---|---|
| `.btn-primary` | `--btn-bg` / `--btn-ink`; hover drops to `opacity .88`. The one emphatic action per view. |
| `.btn-soft` | `--surface-sunken` + `--line`; hover strengthens the border. |
| `.btn-ghost` | Transparent, `--ink-2`; hover fills `--surface-sunken`. Nav and toolbars. |
| `.btn-danger` | Transparent with a `--danger` border and label. Never a filled red button. |
| `.btn-sm` | `2.25rem` tall, `0.8125rem`. |
| `.btn-icon` | `2.5rem` square, no padding. Always needs an `aria-label`. |

The primary button is **ink, not gold.** Gold is not a call to action in this system; it is the sun in the mark and
the focus ring.

### `.chip`
Pill, `.glass`-like, `2.25rem`, `--ink-2`; hover lifts `1px` and strengthens the border. Suggested prompts, filters.

### `.field`
`min-height: 2.75rem`, `0.9rem` radius, `--surface-sunken` on a `--line-strong` border. Focus drops the outline and
uses `--focus` border + a 3 px `color-mix(--focus 25%)` ring — the only place a glow is allowed.

### `.eyebrow`, `.sr-only`, `.rise`
Section kicker; the standard visually-hidden helper; and the entrance animation — `rise`, 450 ms
`cubic-bezier(.2,.7,.2,1)`, 8 px up with a fade. One motion curve, one distance; do not invent a second.

### The brand mark
`Logo.svelte` draws the mark inline and themes the book via `--logo-body`. It is the **seven-ray** drawing, which is
correct because the header renders it at 34 px.

**The mark has two drawings and the size decides which.** Seven rays at **32 px and above**, five rays **below
32 px** and in every favicon/`.ico`. The reasoning, the measurements and the file-by-file assignment are in
[BRAND.md](BRAND.md) §*Two drawings, one mark*. In practice:

- Anything in-product — header, empty states, about page — is well above 32 px, so it is the seven-ray drawing, and
  `Logo.svelte` is already that. Nothing to decide.
- The only five-ray surfaces are `static/favicon.svg` and `static/favicon.ico`. If you touch either, keep them on
  the small variant (`brand/assets/holmesai-icon-tile-small.svg`).
- Rendering the mark below 24 px transparent, or below 16 px at all, is out of range — use no mark instead.

Never recolour the mark in CSS beyond `--logo-body`, and never re-point `Logo.svelte` at an SVG file; the inline
form is what lets the book follow the theme.

### Icons
**Lucide** (`@lucide/svelte`), default stroke, sized in px at the call site (16 for inline, 20–24 for controls).
There is no custom icon set and none should be drawn.

---

## 6. Accessibility floor

- `:focus-visible` is global: `2px solid var(--focus)`, `3px` offset, `0.5rem` radius. Never remove it; `.field`
  replaces it with an equivalent, which is the only exception.
- Touch targets are `2.75rem` (`2.25rem` for `-sm`, which is for dense toolbars, not primary actions).
- `prefers-reduced-motion: reduce` kills every animation and transition globally. New motion inherits this only if it
  uses `animation`/`transition` — JS-driven motion must check the query itself.
- `prefers-contrast: more` tightens the ink and line ladder (§2.3).
- `color-scheme` is declared per theme so native form controls and scrollbars follow.

---

## 7. Building a new page so it belongs

1. `<Header />`, then content in `mx-auto max-w-7xl px-4 sm:px-8 lg:px-12`.
2. `.backdrop` is already mounted globally; do not add a second one and do not set a page background.
3. Section opens with an `.eyebrow`, then an `h1`/`h2` at `-0.02em`, then `.prose-holmes` for the copy.
4. Panels are `.glass .card`. Actions are `.btn`; exactly one `.btn-primary` in view.
5. Colour comes from tokens only. If a value is not in §2, it does not belong on the page.
6. Check it in both themes and at 320 px before calling it done.
