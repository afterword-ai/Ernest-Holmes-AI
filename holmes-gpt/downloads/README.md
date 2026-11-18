# downloads/ — failed acquisition pipeline, kept for reference

This directory is **gitignored**. Nothing here is loaded at runtime any more.

## What this was

An attempt (2025) to download Ernest Holmes' books and build a training corpus
from them. **It did not succeed.** `download_correct_holmes_texts.py` hard-codes
Project Gutenberg IDs 67870 to 67874, each marked `# Verified correct ID`. None
of them is a Holmes work; they are unrelated books (a Crawford novel, a Lawson
novel, a gardening book, a volcanology textbook, an Epes Sargent novel). The
script's content check was loose enough that they passed, and they were written
out under the intended Holmes filenames.

`processed/` and `texts/` held those mislabeled files. They were removed on
2026-11-17 so nobody downstream mistakes them for source material. Copies are
preserved, with the full account, at:

    ~/Sites/_Archive/HolmesAI-training-corpus/

## The datasets that used to live here

`training_data/*.json` were never extracted from any text. They are paraphrases
composed for this project, emitted from Python list literals in
`create_training_dataset.py` and `enhance_training_dataset.py`.

They now live in `src/lib/data/knowledge/`, with honest provenance metadata,
and are bundled into the build.

Note: the copies here were **tracked in git** despite `downloads/` appearing in
.gitignore — they were committed before that rule was added, and ignoring a
path does not untrack it. The Dockerfile also copied them in deliberately. So
production was never one `git clean` from breaking. The move was made because
reading them at runtime from `process.cwd()` was needless indirection propped
up by a Dockerfile `COPY` and a .dockerignore carve-out, both now removed.

**Do not point runtime code at this directory again.**

## Before reusing any of these scripts

Add a verification step that the downloaded text is actually the intended book.
Its absence is what caused this whole failure. See `RETRAINING.md` in the
archive folder for the copyright position on each title — several are very
likely still in copyright, contrary to what `resources/holmes-texts-complete.md`
used to claim.
