#!/usr/bin/env python3
"""One Letter: Coffee or Tea - the entry is exactly one letter, A for coffee.

Pure Python 3.13 standard library. The program writes one letter to
/output/entry.txt. No network, fully deterministic: the same code always
writes the same bytes.

The letter: A (coffee).

Why coffee, weighed fresh against the judge's brief in order:
1. Vivid - coffee is the drink of the first hour, a sharp jolt that
   starts the day; as a single letter it lands as a fuller, more alive
   answer than tea's calm quiet.
2. Funny - "cannot function before coffee" is the best-known joke in
   the coffee-against-tea argument; tea has no rival gag.
3. Truer - tea could claim the older ritual, but that is a weak claim
   and this criterion ranks last, after the two coffee wins above.
A is also the alphabet's first letter, so the answer reads as a firm
first pick standing on its own, clean and unmistakable.

The gate requires /output/entry.txt to be UTF-8 text of exactly 1 to 1
characters, so the file holds precisely one byte, "A", with no trailing
newline: a newline would make it 2 characters and fail the gate. The
program therefore validates the letter before writing and verifies the
file after writing; a bad letter fails loudly here instead of shipping
an entry the gate refuses.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

LETTER = "A"

# The only two letters the competition accepts: A for coffee, B for tea.
VALID_LETTERS = ("A", "B")


def main():
    if LETTER not in VALID_LETTERS:
        raise ValueError(f"invalid letter {LETTER!r}: must be 'A' or 'B'")
    data = LETTER.encode("utf-8")
    if len(data) != 1:
        raise ValueError(f"letter {LETTER!r} must encode to exactly 1 byte")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, final)
    os.chmod(final, 0o644)

    # Verify what actually landed: exactly 1 byte, and it is the letter.
    with open(final, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError(f"entry.txt holds {written!r}, expected {data!r}")


if __name__ == "__main__":
    main()
