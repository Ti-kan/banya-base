import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
}

targets = [
    ("medvezhka", "https://m.vk.com/medvezhka_krsk24"),
    ("terem", "https://m.vk.com/banya_terem_krsk"),
    ("par-ok", "https://m.vk.com/banyaparok"),
    ("elki-i-volki", "https://m.vk.com/club100310425"),
    ("banya-house", "https://m.vk.com/yu_24ru")
]

for name, url in targets:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
            # find userapi images
            imgs = re.findall(r'https://[^\s"\'\(\)]+userapi\.com/[^\s"\'\(\)]+\.(?:jpg|jpeg|webp)', html)
            print(f"{name} VK images found: {len(imgs)}")
            for img in imgs[:3]:
                print(f"  {img}")
    except Exception as e:
        print(f"{name} VK error: {e}")
