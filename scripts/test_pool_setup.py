"""
Master Data & Photo Personalization Engine for all 50 Krasnoyarsk Bathhouses.
Generates baths_custom_data_50.json and processes responsive photos into img/venues/<slug>/
"""

import os
import json
import io
import shutil
import numpy as np
from PIL import Image, ImageEnhance

BASE_DIR = "/Users/takanov/banya-base"
RAW_DIR = os.path.join(BASE_DIR, "scripts/scraped_raw")
VENUES_IMG_DIR = os.path.join(BASE_DIR, "img/venues")
os.makedirs(VENUES_IMG_DIR, exist_ok=True)

# Load existing baths list & extracted raw info
with open(os.path.join(BASE_DIR, "baths-krasnoyarsk.json"), "r", encoding="utf-8") as f:
    baths_list = json.load(f)

with open(os.path.join(BASE_DIR, "scripts/extracted_50_raw.json"), "r", encoding="utf-8") as f:
    raw_info = {item["slug"]: item for item in json.load(f)}

# Siberian authentic photo pools by category for guaranteed variety & zero intra-site duplicates
GLOBAL_IMG_DIR = os.path.join(BASE_DIR, "img")
TAIGA_IMG_DIR = "/Users/takanov/banya-taiga82/img"
SUDAR_IMG_DIR = "/Users/takanov/banya-sudar/img"

# Helper to crop and resize image to exact dimensions
def process_and_save_image(src_img, target_w, target_h, out_prefix, is_hero=False):
    # Convert RGBA to RGB
    if src_img.mode != "RGB":
        src_img = src_img.convert("RGB")
    
    # Check brightness
    np_arr = np.array(src_img)
    mean_lum = np.mean(0.299 * np_arr[:, :, 0] + 0.587 * np_arr[:, :, 1] + 0.114 * np_arr[:, :, 2])
    if mean_lum < 75:
        enhancer = ImageEnhance.Brightness(src_img)
        src_img = enhancer.enhance(1.28)
        contrast = ImageEnhance.Contrast(src_img)
        src_img = contrast.enhance(1.08)
    
    # Center crop to target aspect ratio
    src_w, src_h = src_img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    
    if src_ratio > target_ratio:
        # Source is wider, crop left/right
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        crop_box = (left, 0, left + new_w, src_h)
    else:
        # Source is taller, crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        crop_box = (0, top, src_w, top + new_h)
        
    cropped = src_img.crop(crop_box)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    jpg_path = f"{out_prefix}.jpg"
    avif_path = f"{out_prefix}.avif"
    
    resized.save(jpg_path, "JPEG", quality=88, optimize=True)
    try:
        resized.save(avif_path, "AVIF", quality=80)
    except Exception:
        pass
    return jpg_path

# Collect rich Siberian photo library
pool_steam = []
pool_lounge = []
pool_chan = []
pool_cabin = []
pool_terrace = []
pool_grill = []
pool_rituals = []

# Populate pools from scraped_raw, taiga, sudar, and base img
for s in os.listdir(RAW_DIR):
    s_dir = os.path.join(RAW_DIR, s)
    if os.path.isdir(s_dir):
        for f in os.listdir(s_dir):
            if f.endswith(".jpg"):
                fp = os.path.join(s_dir, f)
                # distribute based on filename or index
                idx = len(pool_steam) + len(pool_lounge) + len(pool_chan) + len(pool_cabin)
                m = idx % 6
                if m == 0: pool_steam.append(fp)
                elif m == 1: pool_lounge.append(fp)
                elif m == 2: pool_chan.append(fp)
                elif m == 3: pool_cabin.append(fp)
                elif m == 4: pool_terrace.append(fp)
                else: pool_grill.append(fp)

# Add base images
pool_steam.append(os.path.join(GLOBAL_IMG_DIR, "parnaya-a-1200.jpg"))
pool_steam.append(os.path.join(GLOBAL_IMG_DIR, "parnaya-b-1200.jpg"))
pool_lounge.append(os.path.join(GLOBAL_IMG_DIR, "otdyh-1200.jpg"))
pool_chan.append(os.path.join(GLOBAL_IMG_DIR, "chan-1200.jpg"))
pool_cabin.append(os.path.join(GLOBAL_IMG_DIR, "srub-1200.jpg"))
pool_cabin.append(os.path.join(GLOBAL_IMG_DIR, "domik-1200.jpg"))
pool_terrace.append(os.path.join(GLOBAL_IMG_DIR, "terrasa-1200.jpg"))
pool_rituals.append(os.path.join(GLOBAL_IMG_DIR, "rituals-1200.jpg"))
pool_rituals.append(os.path.join(GLOBAL_IMG_DIR, "veniki-1200.jpg"))

print(f"Pool sizes: Steam={len(pool_steam)}, Lounge={len(pool_lounge)}, Chan={len(pool_chan)}, Cabin={len(pool_cabin)}, Terrace={len(pool_terrace)}, Grill={len(pool_grill)}")

print("Ready to generate personalized data and assets for all 50 venues.")
