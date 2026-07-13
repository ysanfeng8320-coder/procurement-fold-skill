#!/usr/bin/env python3
"""CLI — Procurement Fold v2 (species-first)."""
import os
import sys

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
KG = os.path.join(REPO, "kg_engine")
sys.path.insert(0, KG)

from fold.run_v2 import main

if __name__ == "__main__":
    main()
