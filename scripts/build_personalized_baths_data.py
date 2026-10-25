"""
Master Personalization Generator for 50 Krasnoyarsk Bathhouses.
Creates:
1. banya_custom_data_50.json (rich structured venue dataset)
2. img/venues/<slug>/ (all 11 photos in responsive 480w, 720w, 1200w/800w in JPG & AVIF)
"""

import os
import json
import numpy as np
from PIL import Image, ImageEnhance

BASE_DIR = "/Users/takanov/banya-base"
RAW_DIR = os.path.join(BASE_DIR, "scripts/scraped_raw")
VENUES_IMG_DIR = os.path.join(BASE_DIR, "img/venues")
os.makedirs(VENUES_IMG_DIR, exist_ok=True)

# 1. Base Siberian high-res image pools
BASE_IMG_DIR = os.path.join(BASE_DIR, "img")
TAIGA_IMG_DIR = "/Users/takanov/banya-taiga82/img"
SUDAR_IMG_DIR = "/Users/takanov/banya-sudar/img"

# Collect all available source images to create an expansive curated bank
curated_bank = []

# Add all scraped raw images
for d in sorted(os.listdir(RAW_DIR)):
    dp = os.path.join(RAW_DIR, d)
    if os.path.isdir(dp):
        for f in sorted(os.listdir(dp)):
            if f.endswith(".jpg"):
                curated_bank.append(os.path.join(dp, f))

# Add Taiga images
for f in ["hero", "chan", "srub", "domik", "parnaya-a", "parnaya-b", "otdyh", "terrasa", "dush", "rituals", "veniki"]:
    fp = os.path.join(TAIGA_IMG_DIR, f"{f}-720.jpg")
    if os.path.exists(fp):
        curated_bank.append(fp)

# Add Sudar images
for f in ["hero", "chan", "srub", "domik", "parnaya-a", "parnaya-b", "otdyh", "terrasa", "dush", "rituals", "veniki"]:
    fp = os.path.join(SUDAR_IMG_DIR, f"{f}-720.jpg")
    if os.path.exists(fp):
        curated_bank.append(fp)

# Add base template images
for f in ["hero-1200", "chan-1200", "srub-1200", "domik-1200", "parnaya-a-1200", "parnaya-b-1200", "otdyh-1200", "terrasa-1200", "dush-1200", "rituals-1200", "veniki-1200"]:
    fp = os.path.join(BASE_IMG_DIR, f"{f}.jpg")
    if os.path.exists(fp):
        curated_bank.append(fp)

print(f"Curated Siberian Photo Bank contains {len(curated_bank)} high-res assets.")

def crop_and_save(src_path, target_w, target_h, out_prefix):
    img = Image.open(src_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
        
    # Check brightness
    np_arr = np.array(img)
    mean_lum = np.mean(0.299 * np_arr[:, :, 0] + 0.587 * np_arr[:, :, 1] + 0.114 * np_arr[:, :, 2])
    if mean_lum < 75:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.26)
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(1.08)
        
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        crop_box = (left, 0, left + new_w, src_h)
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        crop_box = (0, top, src_w, top + new_h)
        
    cropped = img.crop(crop_box)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    jpg_path = f"{out_prefix}.jpg"
    avif_path = f"{out_prefix}.avif"
    
    resized.save(jpg_path, "JPEG", quality=88, optimize=True)
    try:
        resized.save(avif_path, "AVIF", quality=80)
    except Exception:
        pass

def process_venue_photos(slug, real_photos, bank_offset):
    venue_dir = os.path.join(VENUES_IMG_DIR, slug)
    os.makedirs(venue_dir, exist_ok=True)
    
    # Needs 11 distinct unique photos:
    # 0: hero
    # 1: hall1_1 (steam)
    # 2: hall1_2 (lounge)
    # 3: hall1_3 (terrace)
    # 4: hall2_1 (chan/water)
    # 5: hall2_2 (steam-b)
    # 6: hall2_3 (cabin/srub)
    # 7: hall3_1 (guest house)
    # 8: hall3_2 (bedroom/lounge)
    # 9: hall3_3 (grill/patio)
    # 10: rituals
    
    chosen = []
    used_hashes = set()
    
    # Add real scraped photos first
    for p in real_photos:
        if os.path.exists(p) and p not in used_hashes:
            chosen.append(p)
            used_hashes.add(p)
            if len(chosen) == 11:
                break
                
    # Fill remaining from curated bank with offset to guarantee variety across venues
    bank_len = len(curated_bank)
    curr_idx = bank_offset % bank_len
    while len(chosen) < 11:
        cand = curated_bank[curr_idx]
        if cand not in used_hashes and os.path.exists(cand):
            chosen.append(cand)
            used_hashes.add(cand)
        curr_idx = (curr_idx + 1) % bank_len
        
    # Process 11 photos:
    # 0. Hero (1200x800, 720x480, 480x320)
    crop_and_save(chosen[0], 1200, 800, os.path.join(venue_dir, "hero-1200"))
    crop_and_save(chosen[0], 720, 480, os.path.join(venue_dir, "hero-720"))
    crop_and_save(chosen[0], 480, 320, os.path.join(venue_dir, "hero-480"))
    
    # 1..3: Hall 1 (720x540, 480x360)
    for i in range(1, 4):
        slot_name = f"hall1_{i}"
        crop_and_save(chosen[i], 720, 540, os.path.join(venue_dir, f"{slot_name}-720"))
        crop_and_save(chosen[i], 480, 360, os.path.join(venue_dir, f"{slot_name}-480"))
        
    # 4..6: Hall 2 (720x540, 480x360)
    for i in range(4, 7):
        slot_name = f"hall2_{i-3}"
        crop_and_save(chosen[i], 720, 540, os.path.join(venue_dir, f"{slot_name}-720"))
        crop_and_save(chosen[i], 480, 360, os.path.join(venue_dir, f"{slot_name}-480"))
        
    # 7..9: Hall 3 (720x540, 480x360)
    for i in range(7, 10):
        slot_name = f"hall3_{i-6}"
        crop_and_save(chosen[i], 720, 540, os.path.join(venue_dir, f"{slot_name}-720"))
        crop_and_save(chosen[i], 480, 360, os.path.join(venue_dir, f"{slot_name}-480"))
        
    # 10: Rituals (800x600, 480x360)
    crop_and_save(chosen[10], 800, 600, os.path.join(venue_dir, "rituals-800"))
    crop_and_save(chosen[10], 480, 360, os.path.join(venue_dir, "rituals-480"))
    
    return len(chosen)

# Load raw info
with open(os.path.join(BASE_DIR, "baths-krasnoyarsk.json"), "r", encoding="utf-8") as f:
    baths_list = json.load(f)

with open(os.path.join(BASE_DIR, "scripts/extracted_50_raw.json"), "r", encoding="utf-8") as f:
    raw_dict = {item["slug"]: item for item in json.load(f)}

print(f"Loaded {len(baths_list)} venues.")
