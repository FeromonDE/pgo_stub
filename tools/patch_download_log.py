#!/usr/bin/env python3
"""Keep diagnostic logs outside read-only mounted game images."""
import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = root / "library.cpp"
data = source.read_bytes()
pattern = rb'fopen\("(/[^"\r\n]*/playlgo\.log)", "(?:wb|ab)"\)'
matches = list(re.finditer(pattern, data))
if len(matches) != 2:
    raise SystemExit("PlayGo log implementation changed; review before building")
target = b"/download/playlgo.log"
paths = {match.group(1) for match in matches}
if args.check:
    if paths != {target}:
        raise SystemExit(f"Unexpected diagnostic log paths: {paths!r}")
else:
    for path in paths:
        data = data.replace(path, target)
    source.write_bytes(data)
print("Diagnostic log: /download/playlgo.log")
