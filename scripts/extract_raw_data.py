import json
import sqlite3
import pandas as pd

with open("/Users/takanov/banya-base/baths-krasnoyarsk.json") as f:
    baths = json.load(f)

conn = sqlite3.connect("/Users/takanov/zamer/zamer_baths.db")
c = conn.cursor()
df = pd.read_excel("/Users/takanov/zamer/krasnoyarsk_baths_saunas_merged.xlsx")

print(f"Total baths to process: {len(baths)}")

summary = []
for b in baths:
    slug = b["slug"]
    name = b["name"].strip()
    
    # DB match
    c.execute("SELECT id, name, phone, extra_json FROM targets WHERE lower(name)=lower(?)", (name,))
    row = c.fetchone()
    if not row:
        clean = name.replace(".", "").replace("-", " ").strip().lower()
        c.execute("SELECT id, name, phone, extra_json FROM targets WHERE lower(name) LIKE ?", (f"%{clean[:5]}%",))
        row = c.fetchone()
    
    target_id = row[0] if row else None
    
    transcripts = []
    if target_id:
        c.execute("SELECT transcript_json FROM touches WHERE target_id=? AND transcript_json IS NOT NULL", (target_id,))
        for (tj,) in c.fetchall():
            if tj and len(tj) > 20:
                try:
                    msgs = json.loads(tj)
                    them_msgs = [m["text"] for m in msgs if m.get("who") == "them"]
                    if them_msgs:
                        transcripts.append(" \n ".join(them_msgs))
                except:
                    pass
    
    # Excel match
    m = df[df["Название"].str.strip().str.lower() == name.lower()]
    if len(m) == 0:
        clean_name = name.replace(".", "").replace("-", " ").replace("«", "").replace("»", "").strip().lower()
        m = df[df["Название"].str.lower().apply(lambda x: clean_name in str(x).replace(".", "").replace("-", " ").lower())]
    if len(m) == 0 and b.get("address"):
        street = b["address"].split(",")[0] if "Красноярск" not in b["address"] else b["address"].split(",")[1]
        m = df[df["Адрес"].str.contains(street.strip().split()[-1], case=False, na=False)]
    
    ex_row = m.iloc[0].to_dict() if len(m) > 0 else {}
    
    summary.append({
        "slug": slug,
        "name": name,
        "phone": b.get("phone") or ex_row.get("Телефон 1"),
        "address": b.get("address") or ex_row.get("Адрес"),
        "price_raw": ex_row.get("Цена бани/сауны"),
        "steam_raw": ex_row.get("Парная"),
        "pool_raw": ex_row.get("Бассейн / купель"),
        "cap_raw": ex_row.get("Вместимость"),
        "site": ex_row.get("Сайт 1"),
        "vk": ex_row.get("VK"),
        "tgis": ex_row.get("2ГИС"),
        "transcripts": transcripts
    })

print(f"Summary extracted: {len(summary)} entries.")
with open("/Users/takanov/banya-base/scripts/extracted_50_raw.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print("Saved to extracted_50_raw.json")
