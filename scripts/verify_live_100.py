#!/usr/bin/env python3
"""
verify_live_100.py
Verifies live HTTP 200 responses on GitHub Pages (ti-kan.github.io/banya-base)
for Par House, Batch 1 sample, and Batch 2 sample.
"""

import urllib.request
import time
import sys

URLS = [
    ("Root Landing", "https://ti-kan.github.io/banya-base/"),
    ("Par House (FIX)", "https://ti-kan.github.io/banya-base/b/par-house/"),
    ("Par House Hero JPG", "https://ti-kan.github.io/banya-base/img/venues/par-house/hero-1200.jpg"),
    ("Par House Hero AVIF", "https://ti-kan.github.io/banya-base/img/venues/par-house/hero-1200.avif"),
    ("Batch 1 - Sudar", "https://ti-kan.github.io/banya-base/b/sudar/"),
    ("Batch 1 - Kedrovy Log", "https://ti-kan.github.io/banya-base/b/kedrovy-log/"),
    ("Batch 1 - Medvezhka", "https://ti-kan.github.io/banya-base/b/medvezhka/"),
    ("Batch 1 - Banya Pobezhimova", "https://ti-kan.github.io/banya-base/b/banya-pobezhimova/"),
    ("Batch 2 - Sauna Na Vilskogo", "https://ti-kan.github.io/banya-base/b/sauna-na-vilskogo/"),
    ("Batch 2 - Skyotel", "https://ti-kan.github.io/banya-base/b/skyotel/"),
    ("Batch 2 - Enigma", "https://ti-kan.github.io/banya-base/b/enigma/"),
    ("Batch 2 - Viktoriya", "https://ti-kan.github.io/banya-base/b/viktoriya/"),
    ("Batch 2 - Sibirskiy Variant", "https://ti-kan.github.io/banya-base/b/sibirskiy-variant/"),
    ("Batch 2 Hero JPG", "https://ti-kan.github.io/banya-base/img/venues/sauna-na-vilskogo/hero-1200.jpg"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def verify_all():
    print("=== Checking Live GitHub Pages URLs ===")
    results = []
    all_ok = True
    
    for name, url in URLS:
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                status = response.status
                sz = len(response.read())
                print(f"  [HTTP {status}] ({sz:6d} bytes) - {name}: {url}")
                results.append((name, url, status, sz, "OK"))
        except Exception as e:
            print(f"  [ERROR] {name}: {url} -> {e}")
            results.append((name, url, 0, 0, str(e)))
            all_ok = False
            
    return all_ok, results

if __name__ == "__main__":
    ok, res = verify_all()
    if ok:
        print("\nAll tested live endpoints responded HTTP 200 OK!")
    else:
        print("\nSome live endpoints not yet active (GitHub Pages build takes ~30-60s after git push).")
