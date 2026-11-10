#!/usr/bin/env python3
"""Find Mermaid diagram blocks in a Markdown notes file."""

import argparse
from pathlib import Path
import re

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    content = args.markdown.read_text(encoding="utf-8")
    blocks = re.findall(r"```mermaid\\s*\\n(.*?)```", content, flags=re.S | re.I)
    print(f"Found {len(blocks)} Mermaid diagram block(s).")
    for i, block in enumerate(blocks, 1):
        first = next((line.strip() for line in block.splitlines() if line.strip()), "(empty)")
        print(f"\\nDiagram {i}: {first}")
        print(block.strip())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
