# Building the Holmes source corpus

`build_corpus.py` fetches, **verifies**, cleans and records provenance for Ernest
Holmes' public-domain writing.

The corpus itself is not in this repo. It is ~1.2 MB of source text written to
durable storage outside any git tree, by default
`~/Sites/_Archive/HolmesAI-training-corpus/layer1-public-domain/`.

## Why the verification step exists

This project previously shipped five files named after Ernest Holmes titles that
contained five unrelated Project Gutenberg books — a Crawford novel under
`creative-mind-success-1919.txt`, a Lawson novel under `science-of-mind-1938.txt`,
and so on. The downloader hard-coded Gutenberg IDs annotated `# Verified correct ID`
and accepted whatever came back if the page merely mentioned "science of mind"
anywhere.

So this script will not write a file under a book's name until the fetched text
proves it is that book:

- `must_match` — markers the real book contains, checked against the **fetched**
  source (front matter naming author and title is often removed by cleaning).
- `must_not_match` — markers that must not survive into the **output**, checked
  against the cleaned result.

A failure is a hard stop for that work, not a warning. The build exits non-zero.

That gate has already earned its place: the *Creative Mind* scan carries a
publisher's advert for a book by **Fenwicke** Holmes, Ernest's brother and also a
"science of mind" author. The check rejected the file. The fix was to truncate the
back matter, not to relax the check.

## Usage

```bash
HOLMES_CORPUS_SRC=/path/to/downloads python3 -I scripts/build_corpus.py
```

`HOLMES_CORPUS_SRC` holds the raw `.txt` downloads (default: `scripts/raw/`).
`HOLMES_CORPUS_OUT` sets the destination.

Run with `-I` — the files it reads are untrusted downloads, and isolated mode keeps
the interpreter from importing anything out of their directory.

Output: one cleaned `.txt` per work, plus `manifest.json` with word counts, SHA-256
checksums, source URLs, scan provenance and the markers each file was verified
against.

## Rights

Everything this script collects was published **before 1931** and is US public
domain outright.

Works from **1931–1963** depend on copyright renewal and are handled separately —
see `layer2-restricted/README.md` in the corpus folder. The 1938 revised
*Science of Mind* was renewed (R384162) and is in copyright until 2034; it must not
be added here. Works from **1964 onward** had automatic renewal and are in copyright
regardless of what any renewal database shows.

## Relationship to `src/lib/data/knowledge/`

Unrelated, and the distinction matters. Those JSON files are paraphrases composed
for this project, marked `"verbatim_holmes": false`. This corpus is Holmes' actual
words. Do not blend them.

## Other authors: `build_author_corpus.py`

Each author gets a stand-alone corpus of their own, named for them and kept apart
from Holmes' and from each other's. Relationships between authors are a later,
separate step; nothing here mixes them.

```bash
python3 -I scripts/build_author_corpus.py emerson --fetch
python3 -I scripts/build_author_corpus.py thoreau --fetch
```

Output: `~/Sites/_Archive/<author>-corpus/` with `raw/` (Gutenberg downloads,
untouched), `clean/` (one file per work) and `manifest.json` (SHA-256 of raw and
clean, source URL, markers). Downloads come from the PGLAF mirror because
www.gutenberg.org answers scripted clients with 503.

Same gate as above, plus: editorial matter by anyone else is cut and checked
absent. *Excursions* opens with Emerson's biographical sketch of Thoreau; the
Maine Woods and Cape Cod editions carry editors' introductions. None of that may
sit in a corpus that claims to be one author's words.

| Corpus | Works | Words |
|---|---|---|
| Emerson | Nature (1836), Essays I (1841), Essays II (1844), Representative Men (1850), The Conduct of Life (1860) | ~273k |
| Thoreau | A Week on the Concord and Merrimack (1849), Walden + Civil Disobedience (1854), Excursions (1863), The Maine Woods (1864), Cape Cod (1865) | ~469k |

Not yet included: Emerson's addresses ("The American Scholar", the Divinity
School Address) and his journals; Thoreau's journals.
