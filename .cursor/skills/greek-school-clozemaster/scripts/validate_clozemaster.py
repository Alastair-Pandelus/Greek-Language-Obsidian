# -*- coding: utf-8 -*-
"""Check a Clozemaster TSV: columns, unique cloze words, chunk length, lesson order."""
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"[^\s.,;:!?«»()]+")

MAX_WORDS = 10
NOTE_STARTS = ("n. ", "adj. ", "v. ", "adv.", "prep.", "conj.", "pron. ", "art. ", "num.", "part.", "intj.", "name ")


def main(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise SystemExit("File has a BOM. Save as UTF-8 without a BOM.")
    errors = []
    seen_cloze = set()
    tokens_seen = set()
    greeks = []
    rows = 0
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 5:
            errors.append(f"line {n}: expected 5 fields, got {len(parts)}")
            continue
        greek, english, cloze, _pron, note = parts
        rows += 1
        words = [w.casefold() for w in TOKEN.findall(greek)]
        if cloze.casefold() not in words:
            errors.append(f"line {n}: cloze {cloze!r} is not a whole word in the Greek")
        if len(greek.split()) > MAX_WORDS:
            errors.append(f"line {n}: {len(greek.split())} words, break it up: {greek}")
        key = cloze.casefold()
        if key in seen_cloze:
            errors.append(f"line {n}: cloze {cloze} already used")
        seen_cloze.add(key)
        tokens_seen.update(words)
        greeks.append(greek)
        if not note or note.startswith("L1 ") or len(note) > 200 or not note.startswith(NOTE_STARTS):
            errors.append(f"line {n}: note must be a dictionary line, got {note!r}")
    last_seen = {}
    for i, greek in enumerate(greeks):
        prev = last_seen.get(greek)
        if prev is not None and i - prev < 10 and prev + 10 < len(greeks):
            errors.append(f"line {i + 1}: same sentence as line {prev + 1}; bump it +10")
        last_seen[greek] = i
    missing = sorted(tokens_seen - seen_cloze)
    if missing:
        errors.append("words that appear but are never guessed: " + ", ".join(missing))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK {rows} rows, {len(seen_cloze)} words guessed, {path.name}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python validate_clozemaster.py <course.tsv>")
    raise SystemExit(main(Path(sys.argv[1])))
