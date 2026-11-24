#!/usr/bin/env python3
"""Pack an already-cleaned corpus into a Shelf bundle, without changing a byte.

Usage:
    python3 -I scripts/pack_corpus.py hopkins|eddy [--out=DIR] [--no-import]

build_author_corpus.py fetches and cleans public-domain books itself. Hopkins
and Eddy were cleaned differently: by hand-checked scripts in the
new-thought-research repo, with every OCR fix logged in REPORT.md and checked
against page images. Their text must not be re-cleaned. This script copies
their source trees as they are, adds one reading page per work and a
corpus.json with a SHA-256 for every file, checks each copied file against its
original, and hands the bundle to `shelfctl corpus import`.

Only works the author wrote get a reading page, because a page in source
"hopkins" or "eddy" reads as theirs. Files by other people (the 1894 book
Hopkins only introduced; Eddy's "Fruitage" testimonial letters), duplicate
printings and unusable OCR stay in the bundle as provenance but get no page.

NEW_THOUGHT_RESEARCH, HOPKINS_ARCHIVE, SHELF_HOME and SHELFCTL override paths.
"""

import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

RESEARCH = Path(os.environ.get("NEW_THOUGHT_RESEARCH", Path.home() / "Sites/new-thought-research"))
# Page images and the descriptive manifest exist only in the old archive copy.
HOPKINS_ARCHIVE = Path(os.environ.get(
    "HOPKINS_ARCHIVE", "/Volumes/ExtremePro/ZiggyMirror/Sites/_Archive/hopkins-corpus"))
SHELFCTL = Path(os.environ.get(
    "SHELFCTL", Path.home() / "Sites/Shelf/mac/build/Shelf.app/Contents/MacOS/shelfctl"))

CORPORA = {
    "hopkins": {
        "author": "Emma Curtis Hopkins",
        "lifespan": "1849-1925",
        "person": "emma-curtis-hopkins",
        "description": (
            "Emma Curtis Hopkins' writings, cleaned conservatively from scans (IAPSOP, TruthUnity). "
            "Every OCR fix is listed in clean/REPORT.md with the page image that confirms it (probe/). "
            "The 1894 Spiritual Law in the Natural World is by 'Eleve'; Hopkins wrote only its "
            "introduction, so it is kept as a file but has no reading page."),
        "extra": {  # bundle path -> source outside the research repo
            "probe": HOPKINS_ARCHIVE / "probe",
            "provenance/archive-MANIFEST.md": HOPKINS_ARCHIVE / "MANIFEST.md",
        },
        "works": [
            ("1958__hopkins___scientific_christian_mental_practice", "Scientific Christian Mental Practice", 1958,
             "No copyright notice in the 1958 High Watch printing (1909 Act); see provenance/archive-MANIFEST.md",
             "https://s3.amazonaws.com/truthunity/assets/books/emma-curtis-hopkins-scientific-christian-mental-practice/emma-curtis-hopkins-scientific-christian-mental-practice.pdf"),
            ("1921__hopkins___resume", "Resume: Practice Book for the Twelve Chapters in High Mysticism", 1921,
             "US public domain (published before 1931)", "http://iapsop.com/ssoc/1921__hopkins___resume.pdf"),
            ("1921__hopkins___high_mysticism_eighth_study", "High Mysticism, Eighth Study: Ministry", 1921,
             "US public domain (published before 1931)", "http://iapsop.com/ssoc/1921__hopkins___high_mysticism_eighth_study.pdf"),
            ("1924__hopkins___high_mysticism_first_study", "High Mysticism, First Study: The Silent Edict", 1924,
             "US public domain (published before 1931)", "http://iapsop.com/ssoc/1924__hopkins___high_mysticism_first_study.pdf"),
        ],
    },
    "eddy": {
        "author": "Mary Baker Eddy",
        "lifespan": "1821-1910",
        "person": "mary-baker-eddy",
        "description": (
            "Mary Baker Eddy's writings from archive.org scans, cleaned conservatively (clean/REPORT.md). "
            "Science and Health is the 1910 printing, included on the owner's decision recorded in "
            "provenance/sourcing.md. Not given reading pages: the Fruitage chapter (readers' testimonial "
            "letters, never to be attributed to Eddy), the 1898 Pulpit and Press cross-check copy, and "
            "Christ and Christmas (OCR too poor)."),
        "extra": {},
        "works": [
            ("sciencehealthwit00eddy_9", "Science and Health with Key to the Scriptures", 1910,
             "1910 final edition; see provenance/sourcing.md (owner's approval, 2026-11-20)", None),
            ("miscellaneouswri00eddy_2", "Miscellaneous Writings, 1883-1896", 1897,
             "US public domain (published before 1931)", None),
            ("christianhealing0000eddy", "Christian Healing and Other Writings", 1908,
             "Text public domain; this scan is a modern reprint whose own matter was dropped", None),
            ("christianscience00eddy", "Christian Science versus Pantheism, with Messages 1900-1902", 1898,
             "US public domain (published before 1931)", None),
            ("pulpitpress00eddy_0", "Pulpit and Press", 1906, "US public domain (published before 1931)", None),
            ("retrospectionint00eddy", "Retrospection and Introspection", 1892,
             "US public domain (published before 1931)", None),
            ("rudimentaldivine00eddy_0", "Rudimental Divine Science", 1908,
             "US public domain (published before 1931)", None),
            ("unityofgoodunrea00eddy", "Unity of Good and Unreality of Evil", 1888,
             "US public domain (published before 1931)", None),
            ("messagetomother00eddygoog", "Message to the Mother Church, June 1900", 1900,
             "US public domain (published before 1931)", None),
        ],
    },
}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def page(stem: str, title: str, year: int, author: str, url: str, text: str) -> str:
    meta = {"title": f"{title} ({year}) - {author}", "url": url,
            "fetched": date.today().isoformat() + "T00:00:00",
            "description": f"{author}, {title} ({year}). Cleaned text, unchanged from the corpus file clean/{stem}.txt."}
    # The text goes in as it is: Hopkins' files already carry their ## chapter markers.
    return "---\n" + json.dumps(meta, ensure_ascii=False) + "\n---\n\n" + f"# {title}\n\n" + text.strip() + "\n"


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_arg = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), None)
    if len(args) != 1 or args[0] not in CORPORA:
        print(f"usage: pack_corpus.py {{{'|'.join(CORPORA)}}} [--out=DIR] [--no-import]", file=sys.stderr)
        return 2
    name = args[0]
    c = CORPORA[name]
    person = RESEARCH / "people" / c["person"]
    bundle = Path(out_arg) if out_arg else Path(tempfile.mkdtemp(prefix=f"{name}-corpus-"))
    if bundle.exists():
        shutil.rmtree(bundle)

    # The research repo's sources/ tree, byte for byte, plus its research notes as provenance.
    shutil.copytree(person / "sources", bundle, ignore=shutil.ignore_patterns(".DS_Store"))
    for md in sorted((person / "research").glob("*.md")):
        (bundle / "provenance").mkdir(exist_ok=True)
        shutil.copy2(md, bundle / "provenance" / md.name)
    for dest, src in c["extra"].items():
        if not src.exists():
            print(f"FAIL extra source missing: {src}", file=sys.stderr)
            return 1
        (bundle / dest).parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, bundle / dest, ignore=shutil.ignore_patterns(".DS_Store"))
        else:
            shutil.copy2(src, bundle / dest)

    # Every copied file must equal its original.
    copies = [(person / "sources", bundle)] + [(s, bundle / d) for d, s in c["extra"].items()]
    for src_root, dst_root in copies:
        pairs = ([(src_root, dst_root)] if src_root.is_file() else
                 [(p, dst_root / p.relative_to(src_root)) for p in src_root.rglob("*")
                  if p.is_file() and p.name != ".DS_Store"])
        for s, d in pairs:
            if not filecmp.cmp(s, d, shallow=False):
                print(f"FAIL copy differs: {d}", file=sys.stderr)
                return 1

    (bundle / "shelf").mkdir()
    works = []
    for stem, title, year, rights, url in c["works"]:
        clean = bundle / "clean" / f"{stem}.txt"
        text = clean.read_text(encoding="utf-8")
        src_url = url or f"https://archive.org/details/{stem}"
        (bundle / "shelf" / f"{stem}.md").write_text(page(stem, title, year, c["author"], src_url, text), encoding="utf-8")
        works.append({"slug": stem, "title": title, "year": year, "page": f"shelf/{stem}.md",
                      "clean": f"clean/{stem}.txt", "words": len(text.split()),
                      "source_url": src_url, "rights": rights})
        print(f"OK   {stem:56} {len(text.split()):>8,} words")

    files = {p.relative_to(bundle).as_posix(): sha(p) for p in sorted(bundle.rglob("*"))
             if p.is_file() and p.name not in ("corpus.json", ".DS_Store")}
    total = sum(w["words"] for w in works)
    (bundle / "corpus.json").write_text(json.dumps({
        "name": name, "author": c["author"], "lifespan": c["lifespan"], "description": c["description"],
        "built": date.today().isoformat(),
        "builder": f"HolmesAI holmes-gpt/scripts/pack_corpus.py from new-thought-research/people/{c['person']}",
        "total_words": total, "works": works, "files": files,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(works)} works with pages, {total:,} words, {len(files)} files -> bundle {bundle}")

    if "--no-import" in sys.argv:
        return 0
    subprocess.run([str(SHELFCTL), "corpus", "import", str(bundle)], check=True)
    if not out_arg:
        shutil.rmtree(bundle)
    return 0


if __name__ == "__main__":
    sys.exit(main())
