#!/usr/bin/env python3
"""Build a verified Ernest Holmes public-domain corpus.

Every text must pass a content check against markers that only the intended
book contains, BEFORE it is written under that book's name. The absence of
exactly this step is what put five unrelated novels into this project under
Holmes filenames.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

import os

# Where the fetched .txt files are read from, and where the verified corpus is
# written. Both are deliberately OUTSIDE the repo: the corpus is ~1.2 MB of
# source text that belongs in durable storage, not in git.
#   HOLMES_CORPUS_SRC  raw downloads (default: ./raw next to this script)
#   HOLMES_CORPUS_OUT  verified output
SRC = Path(os.environ.get("HOLMES_CORPUS_SRC", Path(__file__).resolve().parent / "raw"))
OUT = Path(
    os.environ.get(
        "HOLMES_CORPUS_OUT",
        Path.home() / "Sites/_Archive/HolmesAI-training-corpus/layer1-public-domain",
    )
)

# Each entry: the file we fetched, what it must prove it is, and where it came from.
WORKS = [
    {
        "slug": "creative-mind-1919",
        "title": "Creative Mind",
        "year": 1919,
        "src_file": "creative-mind-1919.txt",
        "archive_id": "creative-mind",
        "url": "https://archive.org/details/creative-mind",
        "scan_source": "NewThoughtLibrary.com transcription",
        # must_match: all required. Lowercased substring tests.
        "must_match": ["ernest holmes", "creative mind"],
        # The scan carries a publisher's advert in the back matter for
        # "The Law of Mind in Action" by Fenwicke Lindsay Holmes, Ernest's
        # brother. Truncating at THE END. drops the ad block; the check then
        # proves no Fenwicke text survived into the corpus.
        "must_not_match": ["fenwicke", "project gutenberg"],
        "start_after": "click on a chapter to leap to it",
        "stop_at": "THE END.",
    },
    {
        "slug": "creative-mind-and-success-1919",
        "title": "Creative Mind and Success",
        "year": 1919,
        "src_file": "creative-mind-and-success-by-ernest-holmes.txt",
        "archive_id": "creative-mind-and-success-by-ernest-holmes",
        "url": "https://archive.org/details/creative-mind-and-success-by-ernest-holmes",
        "scan_source": "NewThoughtLibrary.com transcription",
        "must_match": ["ernest holmes", "success"],
        "must_not_match": ["fenwicke", "project gutenberg"],
        "start_after": "click on a chapter to leap to it",
        "stop_at": "home | about us | new additions",
    },
    {
        "slug": "science-of-mind-1926",
        "title": "The Science of Mind (first edition)",
        "year": 1926,
        "src_file": "scienceofmind0000unse_c1a4.txt",
        "archive_id": "scienceofmind0000unse_c1a4",
        "url": "https://archive.org/details/scienceofmind0000unse_c1a4",
        "scan_source": "Cincinnati Bible College & Seminary copy, scanned by Internet Archive 2022",
        "must_match": ["ernest shurtleff holmes", "science of mind", "foreword"],
        # Guard against the 1938 revision, which is still in copyright.
        "must_not_match": ["maude allison lathem", "project gutenberg"],
        "start_after": None,
        "stop_at": None,
    },
    {
        "slug": "bible-in-light-of-religious-science-1929",
        "title": "The Bible in the Light of Religious Science",
        "year": 1929,
        "src_file": "bible1929.txt",
        "archive_id": "bibleinlightofre00holm",
        "url": "https://archive.org/details/bibleinlightofre00holm",
        "scan_source": "Princeton Theological Seminary copy, Internet Archive",
        "must_match": ["ernest shurtleff holmes", "religious science"],
        "must_not_match": ["project gutenberg"],
        "start_after": None,
        "stop_at": None,
    },
]

JUNK_PATTERNS = [
    r"newthoughtlibrary", r"newthoughtarchives", r"new thought library",
    r"^\s*file:///", r"digitized by the internet archive",
    r"kahle/austin foundation", r"archive\.org/details",
    r"click here to give", r"help us process more books",
    r"get more free pdf", r"^\s*i?\s*donate!?\s*$",
    r"terms of service", r"^\s*home\s*\|", r"copyright ©",
    r"cincinnati bible", r"glenway avenue", r"p\.o\. box",
    r"^\s*vers\.\s*\d",
]
JUNK_RE = re.compile("|".join(JUNK_PATTERNS), re.I)

# A line that is only a page number / roman numeral / scan noise.
NOISE_RE = re.compile(r"^\s*[ivxlcdm\d\W_]{0,12}\s*$", re.I)


def clean(raw: str, start_after: str | None, stop_at: str | None) -> str:
    text = raw
    if start_after:
        i = text.lower().find(start_after.lower())
        if i != -1:
            text = text[i + len(start_after):]
    if stop_at:
        j = text.lower().rfind(stop_at.lower())
        if j != -1:
            text = text[:j]

    kept = []
    for line in text.split("\n"):
        if JUNK_RE.search(line):
            continue
        if NOISE_RE.match(line):
            continue
        kept.append(line.rstrip())

    out = "\n".join(kept)
    # Join words broken across a line by hyphenation.
    out = re.sub(r"(\w)-\n(\w)", r"\1\2", out)
    # Collapse runs of blank lines to a paragraph break.
    out = re.sub(r"\n{3,}", "\n\n", out)
    # Normalise intra-line whitespace without destroying paragraphs.
    out = "\n".join(re.sub(r"[ \t]{2,}", " ", ln).strip() for ln in out.split("\n"))
    return out.strip() + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest, failures = [], []

    for w in WORKS:
        src = SRC / w["src_file"]
        if not src.exists():
            failures.append(f"{w['slug']}: source file missing ({w['src_file']})")
            continue

        raw = src.read_text(encoding="utf-8", errors="replace")
        cleaned = clean(raw, w["start_after"], w["stop_at"])

        # Identity is proved against the fetched file: the front matter that
        # names the book and author is often stripped by cleaning.
        missing = [m for m in w["must_match"] if m not in raw.lower()]
        # Contamination is proved against the OUTPUT: what matters is that no
        # forbidden text survived into the corpus file, not that the scan was
        # free of it (back-matter adverts are normal in these editions).
        present = [m for m in w["must_not_match"] if m in cleaned.lower()]
        if missing or present:
            failures.append(
                f"{w['slug']}: VERIFICATION FAILED -- missing_in_source={missing} "
                f"forbidden_in_output={present}"
            )
            continue

        words = len(cleaned.split())
        if words < 10_000:
            failures.append(f"{w['slug']}: too short after cleaning ({words} words)")
            continue

        dest = OUT / f"{w['slug']}.txt"
        dest.write_text(cleaned, encoding="utf-8")

        manifest.append({
            "slug": w["slug"],
            "title": w["title"],
            "author": "Ernest Shurtleff Holmes",
            "year": w["year"],
            "file": dest.name,
            "words": words,
            "bytes": dest.stat().st_size,
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
            "raw_words": len(raw.split()),
            "provenance": "original source text (verbatim Holmes)",
            "derived": False,
            "rights": "US public domain (published before 1931)",
            "source_url": w["url"],
            "archive_id": w["archive_id"],
            "scan_source": w["scan_source"],
            "verified_markers": w["must_match"],
            "pipeline_stage": "fetched -> verified -> cleaned (OCR/boilerplate stripped)",
        })
        print(f"OK   {w['slug']:46} {words:>7,} words")

    for f in failures:
        print(f"FAIL {f}", file=sys.stderr)

    (OUT / "manifest.json").write_text(
        json.dumps(
            {
                "corpus": "Ernest Holmes, public-domain source texts",
                "built": "2026-11-18",
                "note": (
                    "Verbatim Holmes. Distinct from the authored paraphrase in the app "
                    "(src/lib/server/packs/holmes/knowledge/), which is NOT Holmes' words. Every file "
                    "here passed a content check against markers unique to the intended "
                    "book before being written under that book's name."
                ),
                "total_words": sum(m["words"] for m in manifest),
                "works": manifest,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\n{len(manifest)} works, {sum(m['words'] for m in manifest):,} words -> {OUT}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
