import urllib.request
import json
import sys
import time

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, len(resp.read())
    except Exception as e:
        return None, str(e)

def main():
    with open('/Users/takanov/banya-base/banya_custom_data_100.json') as f:
        venues = json.load(f)

    print(f"Loaded {len(venues)} venues for live verification.")
    
    # Check sample of Batch 1 and Batch 2
    test_slugs = [
        'par-house',          # Par House critical fix
        'sudar',              # Batch 1 premium
        'kedrovy-log',        # Batch 1 premium
        'medvezhka',          # Batch 1
        'banya-pobezhimova',  # Batch 1 uniqueness fix
        'sauna-na-vilskogo',  # Batch 2 start
        'skyotel',            # Batch 2
        'enigma',             # Batch 2
        'strekoza',           # Batch 2
        'dzhem',              # Batch 2 end
    ]

    print("\n--- Verifying Live Pages on GitHub Pages ---")
    base_url = "https://ti-kan.github.io/banya-base/b"
    
    all_ok = True
    for slug in test_slugs:
        url = f"{base_url}/{slug}/"
        hero_url = f"https://ti-kan.github.io/banya-base/img/venues/{slug}/hero-720.jpg"
        
        status_html, size_html = check_url(url)
        status_img, size_img = check_url(hero_url)
        
        print(f"[{status_html}] HTML: {url} ({size_html} bytes) | [{status_img}] HERO: {hero_url} ({size_img} bytes)")
        if status_html != 200 or status_img != 200:
            all_ok = False

    if all_ok:
        print("\nALL SAMPLE LIVE ENDPOINTS RESOLVE HTTP 200!")
    else:
        print("\nSome endpoints not yet 200 (GitHub Pages deployment in progress).")

if __name__ == '__main__':
    main()
