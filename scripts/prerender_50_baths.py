#!/usr/bin/env python3
"""
Prerender all 50 Krasnoyarsk bathhouse landing pages and root index.html
with full scroll, text and photo reveal animation support.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from build_landing import main

if __name__ == "__main__":
    print("Running prerender for all Krasnoyarsk bathhouse routes...")
    main()
    print("Prerender finished successfully.")
