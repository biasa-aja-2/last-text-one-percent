"""Last Text at One Percent — make.fun entry (program/v1).

Writes exactly one text message to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output): the last text a phone sends at one percent battery,
in the dying phone's own voice. Pure Python stdlib only.
"""

import os
import sys

TEXT = (
    "Battery 1%. You spent my last moments watching a raccoon steal "
    "a sandwich. Honestly? Worth it. Tell the charger I loved it."
)


def gate(text):
    """Self-check matching the bounty gate: UTF-8 text of 1 to 200
    characters, not only white space, no leading/trailing whitespace.
    The 200-character cap is the gate in the bounty rules: the sealed
    scorer gives Valid 0 to anything longer, and only a valid entry
    goes before the judge, so the text must clear it with room to spare.
    """
    if not isinstance(text, str):
        return "text is not str"
    if not (1 <= len(text) <= 200):
        return "length %d outside 1-200" % len(text)
    if not text.strip():
        return "text is whitespace-only"
    if text != text.strip():
        return "leading/trailing whitespace"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return "not UTF-8: %s" % exc
    return None


def main():
    problem = gate(TEXT)
    if problem is not None:
        print("gate failed: %s" % problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(TEXT)
    os.chmod(path, 0o644)
    with open(path, "rb") as fh:
        data = fh.read()
    text_back = data.decode("utf-8")
    if text_back != TEXT:
        print("read-back mismatch", file=sys.stderr)
        return 1
    problem = gate(text_back)
    if problem is not None:
        print("gate failed on read-back: %s" % problem, file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (path, len(TEXT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
