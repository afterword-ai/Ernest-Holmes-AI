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
python3 -I scripts/build_author_corpus.py emerson
python3 -I scripts/build_author_corpus.py thoreau
python3 -I scripts/build_author_corpus.py troward
python3 -I scripts/build_author_corpus.py quimby
python3 -I scripts/pack_corpus.py hopkins
python3 -I scripts/pack_corpus.py eddy
```

Output: each author is a corpus in the Shelf app (`~/Library/Application Support/Shelf/corpora/<author>/`):
`raw/` (downloads, untouched), `clean/` (one file per work), `shelf/` (one reading page per work, indexed as
source `<author>`) and `corpus.json` (works, source URLs, markers, SHA-256 of every file). The builder
assembles the bundle in a temporary folder and runs `shelfctl corpus import`, which checks every
checksum before storing it. Raw files are reused from the stored bundle; missing ones are downloaded
from the PGLAF mirror, because www.gutenberg.org answers scripted clients with 503.

Same gate as above, plus: editorial matter by anyone else is cut and checked
absent. *Excursions* opens with Emerson's biographical sketch of Thoreau; the
Maine Woods and Cape Cod editions carry editors' introductions. None of that may
sit in a corpus that claims to be one author's words.

| Corpus | Works | Words |
|---|---|---|
| Emerson | All published prose: Nature, Addresses, and Lectures (1849, incl. The American Scholar and the Divinity School Address), Essays I and II, Representative Men, English Traits, The Conduct of Life, Society and Solitude, Letters and Social Aims; posthumous: Lectures and Biographical Sketches, Miscellanies, Natural History of Intellect | ~794k |
| Troward | Edinburgh Lectures (1904), Doré Lectures (1909), The Creative Process in the Individual (1910), Bible Mystery and Bible Meaning (1913), The Law and the Word (1917), The Hidden Power (1921) | ~265k |
| Quimby | His writings from The Quimby Manuscripts (1921): early writings, letters to patients, Questions and Answers, and the essays of chapters XIV-XIX | ~129k |
| Thoreau | A Week on the Concord and Merrimack (1849), Walden + Civil Disobedience (1854), Excursions (1863), The Maine Woods (1864), Cape Cod (1865) | ~469k |

In the posthumous Emerson volumes the editors' prefaces, notes and footnotes (J. E.
Cabot, Edward W. Emerson) are cut; Emerson's own footnotes in the lifetime books stay.

Troward's own forewords are kept; Paul Derrick's "Appreciation" (Law and the Word)
and the publishers' notes are cut. *Bible Mystery and Bible Meaning* is not on
Gutenberg, so it comes from Internet Archive OCR (Cornell's 1913 copy,
`cu31924029276710`). The OCR pass collapses spacing, drops running page headers
and rejoins hyphenated words; scattered OCR misreadings remain, including about 15
garbled running headers.

Quimby published no books; his writings survive in *The Quimby Manuscripts* (1921),
edited by Horatio W. Dresser, which interleaves them with Dresser's own narrative,
patients' testimony and letters, and the Eddy chapter. Only Quimby's chapters are
kept (`segments`). Dresser's bracketed notes are cut, including multi-paragraph
ones, and eight note tails whose brackets the OCR lost are cut by their wording
(`drop_paragraphs`, each must match exactly one paragraph). Short bracketed words
are Dresser's readings of illegible manuscript and stay bracketed. Quimby often
refers to himself as "Dr. Quimby" or "P. P. Q.", so third-person mentions alone
are not a sign of editorial text. Some patients' accounts that Quimby himself
included in his pieces remain.

Not yet included: Emerson's poems, journals and letters; Thoreau's journals.

### Shelf is where corpora live

Shelf holds every corpus: the reading pages it indexes and searches, and the bundle behind them
(scans, raw and cleaned text, reports, checksums). Nothing is kept under `~/Sites/_Archive`.
`shelfctl corpus list` shows them, `shelfctl corpus verify <name>` re-checks every file, and the
Shelf MCP tool `list_corpora` gives an assistant the works and provenance (read-only).

Hopkins and Eddy were cleaned by hand-checked scripts in `new-thought-research`, so they are not
re-cleaned. `pack_corpus.py` copies their `sources/` trees byte for byte (plus Hopkins' page images
and archive manifest, and both research notes as `provenance/`), checks each copy against its
original, and imports. Only works the author wrote get a reading page: Hopkins' 1894 *Spiritual Law*
(by "Eleve"), Eddy's *Fruitage* testimonials, the 1898 *Pulpit and Press* cross-check copy and *Christ
and Christmas* (unusable OCR) stay in the bundle as files only.

`SHELF_HOME`, `SHELFCTL`, `NEW_THOUGHT_RESEARCH` and `HOPKINS_ARCHIVE` override paths.
