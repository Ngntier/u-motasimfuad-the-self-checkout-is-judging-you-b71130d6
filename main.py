"""The Self-Checkout Is Judging You -- one funny line from a smug till.

Writes the entry to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Pure stdlib; validates the line before writing.
"""

import os

ENTRY = "Twelve yoghurts, no spoon, no dignity. Your loyalty card has filed this under 'a cry for help'."


def validate(line):
    """Check the entry meets the gate: 1-200 chars, single line, no control chars."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(line) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("entry must not contain control characters")
    # UTF-8 byte-length cap (gate counts characters, but the file is bytes:
    # keep the payload small and prove the text round-trips cleanly).
    encoded = line.encode("utf-8")
    if len(encoded) > 200:
        raise ValueError(f"entry must be at most 200 UTF-8 bytes, got {len(encoded)}")
    if encoded.decode("utf-8") != line:
        raise ValueError("entry failed UTF-8 round-trip")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    return line


def main():
    line = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    print(f"wrote {len(line)} chars to {path}")


if __name__ == "__main__":
    main()
