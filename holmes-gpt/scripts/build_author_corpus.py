#!/usr/bin/env python3
"""Build a verified, stand-alone public-domain corpus for one author.

Usage:
    python3 -I scripts/build_author_corpus.py emerson [--fetch] [--shelf]
    python3 -I scripts/build_author_corpus.py thoreau [--fetch] [--shelf]

Each author is its own corpus, written to ~/Sites/_Archive/<author>-corpus/:
    raw/            the Project Gutenberg downloads, byte for byte
    clean/          one cleaned .txt per work
    manifest.json   word counts, SHA-256 of raw and clean, source URLs, markers

Same gate as build_corpus.py: nothing is written under a book's name until the
fetched file proves it is that book (must_match, checked against the raw file),
and editorial or boilerplate text proves absent from the output (must_not_match,
checked against the cleaned file). A failure is a hard stop, not a warning.

Editorial matter (introductions, biographical sketches, indexes) is cut, because
a corpus that claims to be one author's words must not carry another writer's.
Example: the Gutenberg "Excursions" opens with Emerson's sketch of Thoreau.
"""

import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ARCHIVE = Path(os.environ.get("CORPUS_ARCHIVE", Path.home() / "Sites/_Archive"))

# www.gutenberg.org rate-limits scripted clients (503); PGLAF is the official mirror.
MIRROR = "https://gutenberg.pglaf.org"

GUTENBERG_JUNK = ["project gutenberg", "gutenberg.org", "gutenberg-tm", "transcriber"]

AUTHORS = {
    "emerson": {
        "name": "Ralph Waldo Emerson",
        "lifespan": "1803-1882",
        "works": [
            {
                # Nature (1836) plus the addresses: The American Scholar, the
                # Divinity School Address, The Transcendentalist and others.
                # Supersedes the stand-alone Nature (#29433), which it contains.
                "slug": "nature-addresses-and-lectures-1849",
                "title": "Nature, Addresses, and Lectures", "year": 1849,
                "gutenberg_id": 71683, "file": "71683-0.txt",
                "must_match": ["emerson", "transparent eye-ball", "the american scholar",
                               "senior class in divinity college", "the transcendentalist"],
                "must_not_match": [],
                "start_at": "NATURE.", "start_occurrence": 1,
            },
            {
                "slug": "essays-first-series-1841", "title": "Essays: First Series",
                "year": 1841, "gutenberg_id": 2944, "file": "2944-0.txt",
                "must_match": ["ralph waldo emerson", "self-reliance", "the over-soul",
                               "compensation", "trust thyself"],
                "must_not_match": [],
            },
            {
                "slug": "essays-second-series-1844", "title": "Essays: Second Series",
                "year": 1844, "gutenberg_id": 2945, "file": "2945.txt",
                "must_match": ["ralph waldo emerson", "the poet", "experience",
                               "nominalist and realist"],
                "must_not_match": [],
            },
            {
                "slug": "representative-men-1850", "title": "Representative Men",
                "year": 1850, "gutenberg_id": 6312, "file": "6312.txt",
                "must_match": ["ralph waldo emerson", "swedenborg; or, the mystic",
                               "plato; or, the philosopher"],
                "must_not_match": [],
            },
            {
                "slug": "conduct-of-life-1860", "title": "The Conduct of Life",
                "year": 1860, "gutenberg_id": 39827, "file": "39827-0.txt",
                "must_match": ["ralph waldo emerson", "conduct of life", "fate",
                               "illusions"],
                "must_not_match": [],
            },
            {
                "slug": "english-traits-1856", "title": "English Traits", "year": 1856,
                "gutenberg_id": 39862, "file": "39862-0.txt",
                "must_match": ["emerson", "english traits", "stonehenge",
                               "first visit to england"],
                "must_not_match": [],
                "start_at": "ENGLISH TRAITS.", "start_occurrence": 2,
            },
            {
                "slug": "society-and-solitude-1870", "title": "Society and Solitude",
                "year": 1870, "gutenberg_id": 69258, "file": "69258-0.txt",
                "must_match": ["ralph waldo emerson", "society and solitude",
                               "civilization", "works and days"],
                "must_not_match": [],
                "start_at": "SOCIETY AND SOLITUDE.", "start_occurrence": 2,
            },
            {
                "slug": "letters-and-social-aims-1876", "title": "Letters and Social Aims",
                "year": 1876, "gutenberg_id": 71393, "file": "71393-0.txt",
                "must_match": ["ralph waldo emerson", "poetry and imagination",
                               "quotation and originality", "immortality"],
                "must_not_match": [],
                "start_at": "POETRY AND IMAGINATION.", "start_occurrence": 1,
            },
            # Posthumous volumes, assembled by J. E. Cabot and Edward W. Emerson.
            # Their prefaces, notes and footnotes are cut; Emerson's text stays.
            {
                "slug": "lectures-and-biographical-sketches-1884",
                "title": "Lectures and Biographical Sketches", "year": 1884,
                "gutenberg_id": 75942, "file": "75942-0.txt",
                "must_match": ["emerson", "demonology", "the sovereignty of ethics",
                               "the preacher"],
                "must_not_match": ["of the pieces included in this volume",
                                   "[footnote"],
                "start_at": "DEMONOLOGY.", "start_occurrence": 1,
                "drop_footnotes": True,
            },
            {
                "slug": "miscellanies-1884", "title": "Miscellanies", "year": 1884,
                "gutenberg_id": 71812, "file": "71812-0.txt",
                "must_match": ["emerson", "the lord’s supper", "historical discourse at concord",
                               "emancipation in the british west indies"],
                "must_not_match": ["the year after mr. emerson’s death",
                                   "mr. emerson did not wish to have his sermons published"],
                "start_at": "THE LORD’S SUPPER", "start_occurrence": 1,
                "stop_at": "NOTES", "stop_occurrence": 1,
                "drop_footnotes": True,
            },
            {
                "slug": "natural-history-of-intellect-1893",
                "title": "Natural History of Intellect, and Other Papers", "year": 1893,
                "gutenberg_id": 71558, "file": "71558-0.txt",
                "must_match": ["emerson", "natural history of intellect", "memory",
                               "michael angelo"],
                "must_not_match": ["the first two pieces in this volume are lectures"],
                "start_at": "NATURAL HISTORY OF INTELLECT.", "start_occurrence": 1,
                "drop_footnotes": True,
            },
        ],
    },
    "thoreau": {
        "name": "Henry David Thoreau",
        "lifespan": "1817-1862",
        "works": [
            {
                "slug": "week-on-concord-and-merrimack-1849",
                "title": "A Week on the Concord and Merrimack Rivers", "year": 1849,
                "gutenberg_id": 4232, "file": "4232-0.txt",
                "must_match": ["henry david thoreau", "concord river", "merrimack"],
                "must_not_match": [],
            },
            {
                "slug": "walden-and-civil-disobedience-1854",
                "title": "Walden; and On the Duty of Civil Disobedience",
                "year": 1854, "gutenberg_id": 205, "file": "205-0.txt",
                # Civil Disobedience (1849) ships in this file; the stand-alone
                # Gutenberg edition (#71) is left out to avoid a duplicate.
                "must_match": ["henry david thoreau", "walden", "economy",
                               "lives of quiet desperation", "civil disobedience",
                               "that government is best which governs least"],
                "must_not_match": [],
                # Title-case chapter lines; listed so Shelf splits passages on them.
                "chapter_titles": [
                    "Economy", "Where I Lived, and What I Lived For", "Reading",
                    "Sounds", "Solitude", "Visitors", "The Bean-Field", "The Village",
                    "The Ponds", "Baker Farm", "Higher Laws", "Brute Neighbors",
                    "House-Warming", "Former Inhabitants and Winter Visitors",
                    "Winter Animals", "The Pond in Winter", "Spring", "Conclusion",
                    "ON THE DUTY OF CIVIL DISOBEDIENCE",
                ],
            },
            {
                "slug": "excursions-1863", "title": "Excursions", "year": 1863,
                "gutenberg_id": 9846, "file": "9846-0.txt",
                "must_match": ["henry david thoreau", "walking", "wild apples",
                               "in wildness is the preservation of the world"],
                # Opens with Emerson's biographical sketch. Cut it, then prove it is gone.
                "must_not_match": ["by r.w. emerson", "biographical sketch",
                                   "last male descendant of a french ancestor"],
                "start_at": "EXCURSIONS", "start_occurrence": 1,
            },
            {
                "slug": "maine-woods-1864", "title": "The Maine Woods", "year": 1864,
                "gutenberg_id": 42500, "file": "42500-0.txt",
                "must_match": ["ktaadn", "chesuncook", "allegash", "thoreau"],
                # 1906 Houghton edition: editor's introductory note, appendix tables
                # and index are cut.
                "must_not_match": ["introductory note", "was the second volume collected"],
                "start_at": "KTAADN", "start_occurrence": 2,
                "stop_at": "APPENDIX", "stop_occurrence": 2,
            },
            {
                "slug": "cape-cod-1865", "title": "Cape Cod", "year": 1865,
                "gutenberg_id": 34392, "file": "34392-0.txt",
                "must_match": ["thoreau", "cape cod", "wellfleet oysterman",
                               "highland light"],
                # 1908 Crowell edition: Clifton Johnson's introduction is cut.
                "must_not_match": ["of the group of notables", "clifton johnson",
                                   "thomas y. crowell"],
                "start_at": "THE SHIPWRECK", "start_occurrence": 1,
            },
        ],
    },
}

ILLUSTRATION_RE = re.compile(r"^\s*\[illustration[^\]]*\]?\s*$", re.I)

# Whole lines that are transcriber credits or printer imprints, not the author.
JUNK_LINE_RE = re.compile(
    r"^\s*(produced by\b.*|.*distributed proofreading.*|next volume"
    r"|the university press, cambridge.*|cambridge: (electrotyped|printed)\b.*)\s*$",
    re.I,
)
# Credits sit at the very start or end of a file; only look there, so a line of
# the author's own prose that begins "produced by" is never dropped.
EDGE_LINES = 40
GUTENBERG_JUNK += ["distributed proofreading", "university press, cambridge"]


def gutenberg_url(gid: int, fname: str) -> str:
    s = str(gid)
    path = "/".join(s[:-1]) if len(s) > 1 else "0"
    return f"{MIRROR}/{path}/{s}/{fname}"


def body(raw: str) -> str:
    """Text between Gutenberg's START and END markers."""
    start = re.search(r"^\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG.*$", raw, re.M | re.I)
    end = re.search(r"^\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG.*$", raw, re.M | re.I)
    if not start or not end:
        raise ValueError("Gutenberg START/END markers not found")
    text = raw[start.end():end.start()]
    # Older files close with "End of [the] Project Gutenberg's <title>..." inside the body.
    text = re.sub(r"^\s*End of (the )?Project Gutenberg.*$", "", text, flags=re.M | re.I)
    # A transcriber's note block at the end (errata, formatting notes) is cut from
    # its first line onward. Only the last 5% is searched, so the body is safe.
    tail_start = int(len(text) * 0.95)
    m = re.search(r"^.*transcriber.*$", text[tail_start:], re.M | re.I)
    if m:
        text = text[: tail_start + m.start()]
    return text


def nth_line(lines: list[str], marker: str, n: int) -> int:
    hits = [i for i, ln in enumerate(lines) if ln.strip() == marker]
    if len(hits) < n:
        raise ValueError(f"marker line {marker!r} occurrence {n} not found")
    return hits[n - 1]


# Editors' footnotes in the posthumous volumes: inline markers like [12] or
# [Footnote 3], and "FOOTNOTES:" blocks of bracketed paragraphs.
FOOTNOTE_REF_RE = re.compile(r"\[(Footnote )?\d+\]")


def drop_footnotes(lines: list[str]) -> list[str]:
    out, skipping, in_note = [], False, False
    for ln in lines:
        s = ln.strip()
        if s == "FOOTNOTES:":
            skipping, in_note = True, False
            continue
        if skipping:
            if not s:
                in_note = False
                continue
            if s.startswith("[") or in_note:
                in_note = True
                continue
            skipping = False
        out.append(ln)
    return out


def clean(raw: str, w: dict) -> str:
    lines = body(raw).split("\n")
    if w.get("stop_at"):
        lines = lines[: nth_line(lines, w["stop_at"], w.get("stop_occurrence", 1))]
    if w.get("start_at"):
        lines = lines[nth_line(lines, w["start_at"], w.get("start_occurrence", 1)):]
    n = len(lines)
    lines = [ln.rstrip() for i, ln in enumerate(lines)
             if not ILLUSTRATION_RE.match(ln)
             and not ((i < EDGE_LINES or i >= n - EDGE_LINES) and JUNK_LINE_RE.match(ln))]
    head = "\n".join(lines[:EDGE_LINES]).lower()
    if "produced by" in head:
        raise ValueError("transcriber credit survived at head of file")
    if w.get("drop_footnotes"):
        lines = drop_footnotes(lines)
    out = "\n".join(lines)
    if w.get("drop_footnotes"):
        out = FOOTNOTE_REF_RE.sub("", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip() + "\n"


SHELF_LIBRARY = Path(os.environ.get(
    "SHELF_LIBRARY", Path.home() / "Library/Application Support/Shelf/library"))
SHELFCTL = Path(os.environ.get(
    "SHELFCTL", Path.home() / "Sites/Shelf/mac/build/Shelf.app/Contents/MacOS/shelfctl"))

# A chapter heading in these editions: a short line in capitals, alone in its paragraph.
ROMAN_RE = re.compile(r"^[IVXLC]{1,6}\.?$")
HEADING_RE = re.compile(r"^[A-Z0-9][A-Z0-9 .,;:’'\"“”&—–-]{2,79}$")


def to_markdown(text: str, w: dict, author: dict, url: str) -> str:
    """One Shelf page per book. Chapter lines become ## headings so Shelf's
    passages split per chapter; the words themselves are unchanged."""
    titles = set(w.get("chapter_titles", []))
    paras = text.split("\n\n")
    out = []
    for p in paras:
        s = p.strip()
        parts = s.split("\n")
        if len(parts) == 2 and ROMAN_RE.match(parts[0].strip()):
            s = parts[1].strip()  # "II\nSTAGE COACH VIEWS"
            parts = [s]
        if len(parts) == 1 and (s in titles or (
                HEADING_RE.match(s) and sum(c.isalpha() for c in s) >= 3)):
            out.append("## " + s.rstrip("."))
        else:
            out.append(p)
    meta = {
        "title": f"{w['title']} ({w['year']}) - {author['name']}",
        "url": url,
        "fetched": date.today().isoformat() + "T00:00:00",
        "description": f"{author['name']}, {w['title']} ({w['year']}). "
                       f"Project Gutenberg #{w['gutenberg_id']}, verified and cleaned.",
    }
    return ("---\n" + json.dumps(meta, ensure_ascii=False) + "\n---\n\n"
            f"# {w['title']}\n\n" + "\n\n".join(out).strip() + "\n")


def export_to_shelf(key: str, author: dict, manifest: list[dict], clean_dir: Path) -> None:
    dest = SHELF_LIBRARY / key
    dest.mkdir(parents=True, exist_ok=True)
    works = {w["slug"]: w for w in author["works"]}
    keep = set()
    for m in manifest:
        page = f"https://www.gutenberg.org/ebooks/{m['gutenberg_id']}"
        text = (clean_dir / f"{m['slug']}.txt").read_text(encoding="utf-8")
        (dest / f"{m['slug']}.md").write_text(
            to_markdown(text, works[m["slug"]], author, page), encoding="utf-8")
        keep.add(f"{m['slug']}.md")
    # Drop pages for works no longer in the corpus (e.g. a superseded edition).
    for old in dest.glob("*.md"):
        if old.name not in keep:
            old.unlink()
    import subprocess
    subprocess.run([str(SHELFCTL), "index"], check=True)
    print(f"Shelf: {len(keep)} pages in source '{key}' -> {dest}")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or args[0] not in AUTHORS:
        print(f"usage: build_author_corpus.py {{{'|'.join(AUTHORS)}}} [--fetch] [--shelf]", file=sys.stderr)
        return 2
    key = args[0]
    author = AUTHORS[key]
    root = ARCHIVE / f"{key}-corpus"
    raw_dir, clean_dir = root / "raw", root / "clean"
    raw_dir.mkdir(parents=True, exist_ok=True)
    clean_dir.mkdir(exist_ok=True)

    manifest, failures = [], []
    for w in author["works"]:
        src = raw_dir / w["file"]
        url = gutenberg_url(w["gutenberg_id"], w["file"])
        if "--fetch" in sys.argv and not src.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "corpus-builder"})
            with urllib.request.urlopen(req, timeout=60) as r:
                src.write_bytes(r.read())
        if not src.exists():
            failures.append(f"{w['slug']}: raw file missing ({src}); rerun with --fetch")
            continue

        raw = src.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
        try:
            cleaned = clean(raw, w)
        except ValueError as e:
            failures.append(f"{w['slug']}: {e}")
            continue

        # Markers can wrap across lines, so match against whitespace-collapsed text.
        flat = " ".join(raw.lower().split())
        missing = [m for m in w["must_match"] if m not in flat]
        forbidden = GUTENBERG_JUNK + w["must_not_match"]
        present = [m for m in forbidden if m in cleaned.lower()]
        if missing or present:
            failures.append(f"{w['slug']}: VERIFICATION FAILED -- "
                            f"missing_in_source={missing} forbidden_in_output={present}")
            continue

        words = len(cleaned.split())
        if words < 5_000:
            failures.append(f"{w['slug']}: too short after cleaning ({words} words)")
            continue

        dest = clean_dir / f"{w['slug']}.txt"
        dest.write_text(cleaned, encoding="utf-8")
        manifest.append({
            "slug": w["slug"],
            "title": w["title"],
            "author": author["name"],
            "year": w["year"],
            "file": f"clean/{dest.name}",
            "words": words,
            "sha256": sha(dest),
            "raw_file": f"raw/{src.name}",
            "raw_sha256": sha(src),
            "source_url": url,
            "gutenberg_id": w["gutenberg_id"],
            "rights": "US public domain (published before 1931)",
            "verified_markers": w["must_match"],
            "excluded_markers": forbidden,
        })
        print(f"OK   {w['slug']:42} {words:>8,} words")

    for f in failures:
        print(f"FAIL {f}", file=sys.stderr)

    (root / "manifest.json").write_text(json.dumps({
        "corpus": f"{author['name']} ({author['lifespan']}), public-domain works",
        "built": date.today().isoformat(),
        "builder": "HolmesAI holmes-gpt/scripts/build_author_corpus.py",
        "note": (f"Stand-alone corpus of {author['name']}'s own words. Editorial "
                 "introductions, sketches by other writers, indexes and Gutenberg "
                 "boilerplate are cut, and each file is checked for their absence."),
        "total_words": sum(m["words"] for m in manifest),
        "works": manifest,
    }, indent=2), encoding="utf-8")

    print(f"\n{len(manifest)} works, {sum(m['words'] for m in manifest):,} words -> {root}")
    if failures:
        return 1
    if "--shelf" in sys.argv:
        export_to_shelf(key, author, manifest, clean_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
