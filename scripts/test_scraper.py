import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    ("tridevyatoe", "https://tridevyatoe-tsarstvo.ru"),
    ("pillars", "https://pillars24.ru"),
    ("green-hall", "https://green-hall24.ru"),
    ("yurta-banya", "https://xn----8sbgb4bldq2g.xn--p1ai/"),
    ("sudar", "https://xn----7sbbdm2drfs7grb.xn--p1ai/"),
    ("kamennaya-rechka", "http://stone-river.ru")
]

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

for name, url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
            imgs = re.findall(r'["\'\(=]([^\s"\'\(\)]+\.(?:jpg|jpeg|png|webp))', html, re.I)
            print(f"{name}: {len(imgs)} images found")
            for img in imgs[:3]:
                print(f"    {img}")
    except Exception as e:
        print(f"{name} error: {e}")
