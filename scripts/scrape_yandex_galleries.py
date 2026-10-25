import asyncio
import os
import re
import urllib.request
import io
from PIL import Image
from playwright.async_api import async_playwright

venues_ym = [
    ("par-ok", "https://yandex.ru/maps/org/par_ok/17839772163/gallery/"),
    ("medvezhka", "https://yandex.ru/maps/org/medvezhka/48231703474/gallery/"),
    ("terem", "https://yandex.ru/maps/org/terem/38575338422/gallery/"),
    ("elki-i-volki", "https://yandex.ru/maps/org/yolki_i_volki/1768216739/gallery/"),
    ("krasnoyarskaya-parilnya", "https://yandex.ru/maps/org/krasnoyarskaya_parilnya/145885239103/gallery/"),
    ("par-house", "https://yandex.ru/maps/org/par_house/116911681285/gallery/"),
    ("villa-parilla", "https://yandex.ru/maps/org/villa_parilla/19541571217/gallery/"),
    ("russkie-bani-na-drovah", "https://yandex.ru/maps/org/russkiye_bani_na_drovakh/1148408821/gallery/"),
    ("taiga", "https://yandex.ru/maps/org/tayga/1739266155/gallery/"),
    ("medvezhya-berloga", "https://yandex.ru/maps/org/medvezhya_berloga/147427181673/gallery/"),
    ("kurazh", "https://yandex.ru/maps/org/kurazh/1017042077/gallery/"),
    ("novaya-zhizn", "https://yandex.ru/maps/org/novaya_zhizn/176214534435/gallery/"),
    ("s-legkim-parom", "https://yandex.ru/maps/org/s_lyogkim_parom/1166705574/gallery/"),
    ("dom-na-vysote", "https://yandex.ru/maps/org/dom_na_vysote/234720979402/gallery/"),
    ("vremya-otdyha", "https://yandex.ru/maps/org/vremya_otdykha/132890533355/gallery/"),
    ("family-par", "https://yandex.ru/maps/org/family_par/83434600109/gallery/"),
    ("barbaris", "https://yandex.ru/maps/org/barbaris/149818816827/gallery/"),
    ("grenlandiya", "https://yandex.ru/maps/org/grenlandiya/1183556774/gallery/"),
    ("dlya-svoih", "https://yandex.ru/maps/org/dlya_svoikh/219665518337/gallery/"),
    ("landmaniya", "https://yandex.ru/maps/org/landmaniya/1179619129/gallery/"),
    ("admiralskaya-usadba", "https://yandex.ru/maps/org/admiralskaya_usadba/144728514936/gallery/"),
    ("grelka", "https://yandex.ru/maps/org/grelka/164741604104/gallery/"),
    ("u-dyadi-vovy", "https://yandex.ru/maps/org/u_dyadi_vovy/138139556111/gallery/")
]

out_base = "/Users/takanov/banya-base/scripts/scraped_raw"
os.makedirs(out_base, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        for slug, url in venues_ym:
            slug_dir = os.path.join(out_base, slug)
            os.makedirs(slug_dir, exist_ok=True)
            
            # Check if already has 5+ photos
            existing = [f for f in os.listdir(slug_dir) if f.endswith(".jpg")]
            if len(existing) >= 6:
                print(f"Skipping {slug}, already has {len(existing)} photos")
                continue
                
            print(f"\nScraping Yandex Gallery for {slug}: {url}")
            page = await context.new_page()
            try:
                await page.goto(url, timeout=18000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3500)
                
                # Scroll down slightly to trigger lazy-load
                await page.evaluate("window.scrollBy(0, 1000)")
                await page.wait_for_timeout(1500)
                
                imgs = await page.eval_on_selector_all("img", "els => els.map(e => e.src)")
                # Get unique altay IDs
                altay_urls = []
                for i in imgs:
                    if "avatars.mds.yandex.net/get-altay/" in i:
                        # Extract altay path
                        parts = i.split("/get-altay/")[1].split("/")
                        if len(parts) >= 2:
                            xxxl_url = f"https://avatars.mds.yandex.net/get-altay/{parts[0]}/{parts[1]}/XXXL"
                            if xxxl_url not in altay_urls:
                                altay_urls.append(xxxl_url)
                
                print(f"  Found {len(altay_urls)} XXXL photo candidates")
                saved = 0
                for idx, a_url in enumerate(altay_urls[:12]):
                    try:
                        req = urllib.request.Request(a_url, headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=10) as resp:
                            data = resp.read()
                            if len(data) > 20000:
                                img = Image.open(io.BytesIO(data))
                                w, h = img.size
                                if w >= 500 and h >= 350:
                                    fn = f"photo_{saved+1:02d}.jpg"
                                    if img.mode != "RGB":
                                        img = img.convert("RGB")
                                    img.save(os.path.join(slug_dir, fn), "JPEG", quality=90)
                                    saved += 1
                                    print(f"    Saved {fn} ({w}x{h})")
                                    if saved >= 8:
                                        break
                    except Exception as e:
                        pass
                print(f"  Total saved for {slug}: {saved}")
            except Exception as e:
                print(f"  Error on {slug}: {e}")
            finally:
                await page.close()
                
        await browser.close()

asyncio.run(main())
