"""Your human, summed up in a single word.

The entry never changes: it is one fixed word, checked by a
row of small named checks before it is allowed onto disk.
Each check looks at one property only -- whether the word is
there at all, whether it fits, whether it is clean, whether
it is really one word, and whether it is letters through and
through. A failure prints its reason to stderr and stops the
program with exit code 1, so a bad entry can never be saved.
Nothing here reads input, touches the network, rolls dice,
or looks at the clock, so every run writes identical bytes.
"""

import sys
from pathlib import Path

ENTRY = "Meetaholic"
LIMIT = 30
DEST = Path("/output/entry.txt")


def fail(reason):
    print(f"invalid: {reason}", file=sys.stderr)
    raise SystemExit(1)


def check_filled(text):
    # A word has to exist before anything else can be said of it.
    if not text or text.strip() == "":
        fail("entry is empty")


def check_within_limit(text):
    if len(text) > LIMIT:
        fail("entry is longer than 30 characters")


def check_no_controls(text):
    # Control characters have no business inside a single word.
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        fail("entry contains control characters")


def check_single_word(text):
    if len(text.split()) != 1:
        fail("entry must be exactly one word")


def check_letters_only(text):
    if not text.isalpha():
        fail("entry must be letters only")


def check_not_marks_only(text):
    if not any(ch.isalnum() for ch in text):
        fail("entry is punctuation only")


def check_not_digits_only(text):
    if text.isdigit():
        fail("entry is digits only")


def check_has_letter(text):
    if not any(ch.isalpha() for ch in text):
        fail("entry has no letters")


def check_no_hyphen(text):
    # A one-word portrait should be one unbroken word.
    if "-" in text:
        fail("entry must not be hyphenated")


def check_no_digits(text):
    # A word about a human should be letters, not a serial number.
    if any(ch.isdigit() for ch in text):
        fail("entry must not contain digits")


CHECKS = (
    check_filled,
    check_within_limit,
    check_no_controls,
    check_single_word,
    check_letters_only,
    check_not_marks_only,
    check_not_digits_only,
    check_has_letter,
    check_no_hyphen,
    check_no_digits,
)


def validate(text):
    for check in CHECKS:
        check(text)


def main():
    validate(ENTRY)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
