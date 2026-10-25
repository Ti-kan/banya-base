import os
import re
import urllib.request
import io
from PIL import Image

out_base = "/Users/takanov/banya-base/scripts/scraped_raw"
os.makedirs(out_base, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

def save_image_from_url(url, dest_path, min_w=400, min_h=300):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) > 15000:
                img = Image.open(io.BytesIO(data))
                w, h = img.size
                if w >= min_w and h >= min_h:
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(dest_path, "JPEG", quality=90)
                    return True, (w, h)
    except Exception as e:
        pass
    return False, None

# 1. Tridevyatoe Tsarstvo
trid_urls = [
    "https://p2.zoon.ru/preview/Lzmk0pljRsUQswRBVzhFmw/1200x800x85/1/a/8/original_641a45bce2a1f223e9048551_683420dd856af1.25010836.jpg",
    "https://p0.zoon.ru/preview/EMA9XXExFHSeJgDKOWBo4g/600x800x85/1/8/6/original_641a45bce2a1f223e9048551_687f340eea63c6.23289615.jpg",
    "https://p2.zoon.ru/preview/fhSWQvWUzW1VWcVawTfFXA/600x800x85/1/5/5/original_641a45bce2a1f223e9048551_687f340e7fdc34.89139253.jpg",
    "https://p1.zoon.ru/preview/aKWQBUbW8Q010qLy3Oqb6A/600x800x85/1/b/0/original_641a45bce2a1f223e9048551_68b9329c289137.61541600.jpg",
    "https://p0.zoon.ru/preview/VEn30a8WZwEskKax1gQk6A/600x800x85/1/b/a/original_641a45bce2a1f223e9048551_68b9329cb14614.55697085.jpg",
    "https://p0.zoon.ru/preview/FZfJyIWmHub9P8LoRAKTtg/672x378x85/1/a/1/original_641a45bce2a1f223e9048551_650af2190e4117.82618469.jpg",
    "https://p2.zoon.ru/preview/ov7gZSjk1jUFzq39gliS_Q/506x271x85/1/6/c/original_67a4641e769f447d370124d9_67a46518c10357.54171653.jpg",
    "https://p2.zoon.ru/preview/Gp6ss7c0e6cdtQgDMO-sZA/506x271x85/1/3/e/original_641a45bce2a1f223e9048551_65294f03d66b07.53643547.jpg",
    "https://p1.zoon.ru/preview/hzx9J-MuKuyxuIswwdcwdg/506x271x85/1/b/7/original_69cf4e65529eee71430bc3ad_69cf4ec115b515.87623157.jpg"
]
td = os.path.join(out_base, "tridevyatoe-tsarstvo")
os.makedirs(td, exist_ok=True)
c = 1
for u in trid_urls:
    ok, sz = save_image_from_url(u, os.path.join(td, f"photo_{c:02d}.jpg"), 450, 250)
    if ok:
        print(f"Tridevyatoe photo_{c:02d}.jpg: {sz}")
        c += 1

# 2. Banya-house (yu-24.ru)
bh_urls = [
    "https://static.tildacdn.com/tild3962-6639-4939-b965-303031626336/4.jpg",
    "https://static.tildacdn.com/tild6634-3830-4266-b734-333865376439/1631084114112_1.jpg",
    "https://static.tildacdn.com/tild3734-3730-4037-b964-353132633635/IMG_20230313_112550_.jpg",
    "https://static.tildacdn.com/tild6661-3331-4432-b437-353736626264/photo_2024-12-04_06-.jpg",
    "https://static.tildacdn.com/tild6531-3533-4131-a164-316466346537/photo_2024-12-05_08-.jpg",
    "https://static.tildacdn.com/tild3833-3663-4134-b135-323634383666/IMG_20210703_234045_.jpg",
    "https://static.tildacdn.com/tild3331-3134-4365-b133-656133656333/IMG_20210703_234048_.jpg",
    "https://static.tildacdn.com/tild3138-3534-4637-b161-333161353332/IMG_20230313_112540_.jpg"
]
bd = os.path.join(out_base, "banya-house")
os.makedirs(bd, exist_ok=True)
c = 1
for u in bh_urls:
    ok, sz = save_image_from_url(u, os.path.join(bd, f"photo_{c:02d}.jpg"), 450, 250)
    if ok:
        print(f"Banya-house photo_{c:02d}.jpg: {sz}")
        c += 1

# 3. Taiga 82 from banya-taiga82
import shutil
taiga_src = "/Users/takanov/banya-taiga82/img"
taiga_dst = os.path.join(out_base, "taiga-82")
os.makedirs(taiga_dst, exist_ok=True)
c = 1
for base in ["hero", "chan", "srub", "domik", "parnaya-a", "parnaya-b", "otdyh", "terrasa", "dush", "rituals"]:
    src_f = os.path.join(taiga_src, f"{base}-720.jpg")
    if os.path.exists(src_f):
        shutil.copy2(src_f, os.path.join(taiga_dst, f"photo_{c:02d}.jpg"))
        c += 1
print(f"Taiga 82 copied {c-1} photos")

# 4. Sudar from banya-sudar
sudar_src = "/Users/takanov/banya-sudar/img"
sudar_dst = os.path.join(out_base, "sudar")
os.makedirs(sudar_dst, exist_ok=True)
c = 1
for base in ["hero", "chan", "srub", "domik", "parnaya-a", "parnaya-b", "otdyh", "terrasa", "dush", "rituals"]:
    src_f = os.path.join(sudar_src, f"{base}-720.jpg")
    if os.path.exists(src_f):
        shutil.copy2(src_f, os.path.join(sudar_dst, f"photo_{c:02d}.jpg"))
        c += 1
print(f"Sudar copied {c-1} photos")

print("Batch downloaded successfully!")
