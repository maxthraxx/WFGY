# verify_manifest.py

import os, sys

with open("manifest.txt") as f:
    expected = [l.strip() for l in f if l.strip() and not l.startswith("#")]

missing = [p for p in expected if not os.path.exists(p)]
if missing:
    print("Missing files:")
    for p in missing:
        print("  ", p)
    sys.exit(1)

print("All files are present.")
