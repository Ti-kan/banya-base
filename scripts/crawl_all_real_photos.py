#!/usr/bin/env python3
"""
MASTER REAL PHOTO EXTRACTOR FOR 100 KRASNOYARSK BATHHOUSES
Fetches strictly real photos from Yandex Maps Gallery, VK, and Official Websites.
Zero stock photos, zero curated bank sharing!
"""

import asyncio
import io
import json
import os
import re
import ssl
import sys
import urllib.request
import pandas as pd
from PIL import Image
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

RAW_DIR = "/Users/takanov/banya-base/scripts/scraped_raw"
os.makedirs(RAW_DIR, exist_ok=True)

MASTER_EXCEL = "/Users/takanov/zamer/krasnoyarsk_baths_saunas_merged.xlsx"
BATCH1_JSON = "/Users/takanov/banya-base/batch1_remaining_queue.json"
BATCH2_JSON = "/Users/takanov/banya-base/batch2_candidates_50.json"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def save_image_url(url, dest_path, min_w=320, min_h=240):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            data = resp.read()
            if len(data) > 10000:
                im = Image.open(io.BytesIO(data))
                if im.size[0] >= min_w and im.size[1] >= min_h:
                    if im.mode != "RGB":
                        im = im.convert("RGB")
                    im.save(dest_path, "JPEG", quality=90)
                    return True, im.size
    except Exception:
        pass
    return False, None

async def extract_for_venue(page, slug, name, ya_url, vk_url, site_url):
    slug_dir = os.path.join(RAW_DIR, slug)
    os.makedirs(slug_dir, exist_ok=True)
    existing = len([f for f in os.listdir(slug_dir) if f.endswith(".jpg")])
    if existing >= 6:
        print(f"[{slug}] Already has {existing} real photos. Skipping.")
        return existing
        
    found_urls = []
    
    # 1. Yandex Maps Gallery
    if ya_url and str(ya_url) != "nan" and str(ya_url).startswith("http"):
        clean_ya = str(ya_url).replace("https://yandex.com", "https://yandex.ru").rstrip("/") + "/gallery/"
        try:
            await page.goto(clean_ya, wait_until="domcontentloaded", timeout=12000)
            await asyncio.sleep(2.0)
            for _ in range(2):
                await page.mouse.wheel(0, 1200)
                await asyncio.sleep(0.7)
            imgs = await page.eval_on_selector_all("img", "elements => elements.map(e => e.src)")
            for u in imgs:
                if "avatars.mds.yandex.net/get-altay" in u or "avatars.mds.yandex.net/get-tycoon" in u:
                    base = re.sub(r"/[A-Z0-9a-z_-]+$", "/XXXL", u)
                    if base not in found_urls:
                        found_urls.append(base)
        except Exception:
            pass
            
    # 2. VK
    if vk_url and str(vk_url) != "nan" and len(found_urls) < 6:
        clean_vk = str(vk_url).split(";")[0].strip().replace("https://vk.ru", "https://m.vk.com").replace("https://vk.com", "https://m.vk.com")
        try:
            req = urllib.request.Request(clean_vk, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
                html = r.read().decode("utf-8", errors="ignore")
            for u in re.findall(r"https://[^\s\"\'\(\)]+userapi\.com/[^\s\"\'\(\)]+\.(?:jpg|jpeg|webp)", html):
                if u not in found_urls:
                    found_urls.append(u)
        except Exception:
            pass
            
    # 3. Official Website
    if site_url and str(site_url) != "nan" and len(found_urls) < 6:
        clean_site = str(site_url).split(";")[0].strip()
        if clean_site.startswith("http"):
            try:
                req = urllib.request.Request(clean_site, headers=HEADERS)
                with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
                    html = r.read().decode("utf-8", errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup.find_all(["img", "a"]):
                    src = tag.get("src") or tag.get("href") or tag.get("data-src") or ""
                    if any(src.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]) and "logo" not in src.lower() and "icon" not in src.lower():
                        if src.startswith("/"):
                            base_root = "/".join(clean_site.split("/")[:3])
                            src = base_root + src
                        if src.startswith("http") and src not in found_urls:
                            found_urls.append(src)
            except Exception:
                pass
                
    # Save photos
    saved = existing
    for u in found_urls:
        dest = os.path.join(slug_dir, f"photo_{saved + 1:02d}.jpg")
        ok, sz = save_image_url(u, dest)
        if ok:
            saved += 1
            if saved >= 10:
                break
                
    print(f"[{slug}] Saved {saved} real photos (from {len(found_urls)} candidates)")
    return saved

async def main():
    print("=" * 80)
    print("STARTING BULK REAL PHOTO EXTRACTION FOR BANYA SITES")
    print("=" * 80)
    
    df = pd.read_excel(MASTER_EXCEL)
    def find_row(name):
        m = df[df["Название"].str.lower().str.strip() == name.lower().strip()]
        if len(m) == 0:
            clean = name.split()[0].lower().replace("«","").replace("»","")
            m = df[df["Название"].str.lower().str.contains(clean, na=False)]
        return m.iloc[0] if len(m) > 0 else None

    with open(BATCH1_JSON, "r", encoding="utf-8") as f:
        b1_items = [b for b in json.load(f) if b["status"] == "ready"]
        
    with open(BATCH2_JSON, "r", encoding="utf-8") as f:
        b2_items = json.load(f)
        
    queue = []
    for b in b1_items:
        r = find_row(b["name"])
        queue.append({
            "slug": b["slug"],
            "name": b["name"],
            "ya": r["Яндекс.Карты"] if r is not None and str(r["Яндекс.Карты"]) != "nan" else None,
            "vk": r["VK"] if r is not None and str(r["VK"]) != "nan" else None,
            "site": r["Сайт 1"] if r is not None and str(r["Сайт 1"]) != "nan" else None,
        })
        
    for b in b2_items:
        queue.append({
            "slug": b["slug"],
            "name": b["name"],
            "ya": b.get("ya_maps"),
            "vk": b.get("vk"),
            "site": b.get("site"),
        })
        
    print(f"Total venues in photo queue: {len(queue)}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = await browser.new_context(
            user_agent=HEADERS["User-Agent"],
            viewport={"width": 1366, "height": 768},
            locale="ru-RU"
        )
        page = await context.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        success = 0
        failed = []
        for idx, item in enumerate(queue, 1):
            slug = item["slug"]
            name = item["name"]
            print(f"[{idx}/{len(queue)}] Processing {slug} ({name})...")
            try:
                cnt = await extract_for_venue(page, slug, name, item["ya"], item["vk"], item["site"])
                if cnt >= 4:
                    success += 1
                else:
                    failed.append((slug, name, cnt))
            except Exception as e:
                print(f"  Error on {slug}: {e}")
                failed.append((slug, name, 0))
            await asyncio.sleep(1.2)
            
        await browser.close()
        
    print("\n" + "=" * 80)
    print(f"PHOTO EXTRACTION COMPLETE! Successfully acquired real photos for: {success}/{len(queue)} venues.")
    if failed:
        print(f"Venues with < 4 photos ({len(failed)}):")
        for s, n, c in failed:
            print(f"  - {s:25} | {n:25} | {c} photos")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
