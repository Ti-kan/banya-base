import urllib.request
import re
import ssl
import os
from PIL import Image
import io

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

targets = [
    ("tridevyatoe-tsarstvo", "https://tridevyatoe-tsarstvo.ru/"),
    ("pillars", "https://pillars24.ru/"),
    ("green-hall", "https://green-hall24.ru/"),
    ("kamennaya-rechka", "http://stone-river.ru/"),
    ("divny-bor", "http://divbor.ru/"),
    ("green-rancho", "https://green-rancho.ru/"),
    ("chaga", "http://chaga-complex.ru/"),
    ("manskiy-klyuch", "http://manakey.ru/"),
    ("joy-in-home", "http://joyinhome.ru/"),
    ("terem", "https://xn----7sba3aa2a2aq6b.xn--p1ai/"), # баня-теремъ.рф
    ("kedrovy-log", "https://kedrlog.ru/")
]

out_dir = "/Users/takanov/banya-base/scripts/scraped_raw"
os.makedirs(out_dir, exist_ok=True)

for slug, url in targets:
    print(f"\nFetching {slug} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
            
            # find all image urls
            matches = re.findall(r'["\'\(=]([^\s"\'\(\)]+\.(?:jpg|jpeg|png|webp))', html, re.I)
            clean_urls = []
            for m in matches:
                m = m.replace("\\/", "/")
                if m.startswith("//"):
                    m = "https:" + m
                elif m.startswith("/"):
                    # relative
                    base_root = "/".join(url.split("/")[:3])
                    m = base_root + m
                elif not m.startswith("http"):
                    m = url.rstrip("/") + "/" + m
                if "favicon" not in m and "logo" not in m and "icon" not in m and m not in clean_urls:
                    clean_urls.append(m)
            
            print(f"  Found {len(clean_urls)} candidate image URLs")
            slug_dir = os.path.join(out_dir, slug)
            os.makedirs(slug_dir, exist_ok=True)
            
            downloaded = 0
            for i, img_url in enumerate(clean_urls[:15]):
                try:
                    img_req = urllib.request.Request(img_url, headers=headers)
                    with urllib.request.urlopen(img_req, context=ctx, timeout=8) as img_resp:
                        data = img_resp.read()
                        if len(data) > 15000: # at least 15KB to avoid tiny icons
                            img = Image.open(io.BytesIO(data))
                            w, h = img.size
                            if w >= 400 and h >= 300: # real photo size
                                fn = f"photo_{downloaded+1:02d}.jpg"
                                if img.mode != "RGB":
                                    img = img.convert("RGB")
                                img.save(os.path.join(slug_dir, fn), "JPEG", quality=90)
                                downloaded += 1
                                print(f"    Saved {fn} ({w}x{h}) from {img_url[:60]}...")
                                if downloaded >= 10:
                                    break
                except Exception as ex:
                    pass
            print(f"  Total valid photos saved for {slug}: {downloaded}")
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
