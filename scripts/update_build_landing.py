"""
Unified Script to inject banya_custom_data_50.json into build_landing.py
"""

BUILD_SCRIPT = "/Users/takanov/banya-base/scripts/build_landing.py"

with open(BUILD_SCRIPT, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace the if-slug hall vars block (lines 138-189)
old_halls_block = """    if slug == "taiga-82":
        small_name = "Комплекс «Тайга 82»"
        small_cap = 8
        small_max = 12
        small_wd = 2750
        small_we = 3250
        big_name = "Большой комплекс «Тайга 1913»"
        big_cap = 8
        big_max = 15
        big_wd = 3250
        big_we = 3750
        house_name = "Пакет «Таёжный вечер (5 часов)»"
        house_cap = 6
        house_max = 6
        house_wd = 11000
        house_we = 15000
        chan_val = 5000
    elif slug == "kedrovy-log":
        small_name = "Одноэтажная баня на Базаихе"
        small_cap = 8
        small_max = 8
        small_wd = 2550
        small_we = 3500
        big_name = "Двухэтажная баня на дровах"
        big_cap = 8
        big_max = 8
        big_wd = 3800
        big_we = 5800
        house_name = "Пакет «Таёжный вечер — Базаиха Релакс (3+1 час в подарок)»"
        house_cap = 8
        house_max = 8
        house_wd = 2550 * 3
        house_we = 3500 * 3
        chan_val = 5500
    else:
        small_name = f"Сруб «{name}»"
        small_cap = cap
        small_max = cap + 4
        small_wd = price_wd
        small_we = price_we
        big_name = f"Большой комплекс «{name}» с чаном"
        big_cap = cap
        big_max = cap + 7
        big_wd = price_wd + 500
        big_we = price_we + 500
        house_name = "Пакет «Таёжный вечер (5 часов)»"
        house_cap = 6
        house_max = 6
        house_wd = price_wd * 4
        house_we = price_we * 4
        chan_val = chan_price"""

new_halls_block = """    c_data = CUSTOM_DATA.get(slug, {})
    if c_data:
        name = c_data.get("name", name)
        address = c_data.get("address", address)
        phone = c_data.get("phone", phone)
        rating = c_data.get("rating", 5.0)
        reviews_count = c_data.get("reviews_count", rev2gis)
        halls = c_data.get("halls", [])
        hall1 = halls[0] if len(halls) > 0 else {}
        hall2 = halls[1] if len(halls) > 1 else {}
        hall3 = halls[2] if len(halls) > 2 else {}

        small_name = hall1.get("title", f"Сруб «{name}»")
        small_cap = hall1.get("cap", cap)
        small_max = hall1.get("cap", cap) + 4
        small_wd = hall1.get("price_wd", price_wd)
        small_we = hall1.get("price_we", price_we)
        small_min = hall1.get("min_hours", "от 2 часов")
        small_desc = hall1.get("desc", "Парная на дровах, комната отдыха, душ, мангал.")
        small_btn = hall1.get("btn_text", "Забронировать сруб")

        big_name = hall2.get("title", f"Большой комплекс с чаном")
        big_cap = hall2.get("cap", cap)
        big_max = hall2.get("cap_max", cap + 6)
        big_wd = hall2.get("price_wd", price_wd + 500)
        big_we = hall2.get("price_we", price_we + 500)
        big_water = hall2.get("water_note", "Горячий чан на дровах")
        big_desc = hall2.get("desc", f"Просторная парная, {big_water.lower()}, трапезная, мангал.")
        big_btn = hall2.get("btn_text", "Забронировать с чаном")

        house_name = hall3.get("title", f"Пакет «Таёжный отдых в {name}»")
        house_cap = hall3.get("cap", cap)
        house_max = hall3.get("cap_max", cap + 6)
        house_wd = hall3.get("price_wd", small_wd * 4)
        house_we = hall3.get("price_we", small_we * 4)
        house_dur = hall3.get("duration", "5 часов отдыха")
        house_inc = hall3.get("included", "Мангал, чай, веник")
        house_desc = hall3.get("desc", "5 часов отдыха: растопленная парная, мангальная зона, сибирский травяной чай, веник в подарок.")
        house_btn = hall3.get("btn_text", "Выбрать таёжный пакет")

        chan_note = c_data.get("chan_note", big_water)
        chan_price_str = c_data.get("chan_price", "3 000 ₽ / топка")
        chan_val = 3000 if "3" in chan_price_str else 4000
        brooms_note = c_data.get("brooms_note", "Свежие таёжные веники (от 450 ₽)")
        master_note = c_data.get("master_note", "Банный ритуал и парение от пармейстера (2 000 ₽)")
        extra_guest_str = c_data.get("extra_guest", "300 ₽ / час (свыше нормы)")
        included_list = c_data.get("included_list", [
            "Зона барбекю, решётки, шампуры и посуда",
            "Таёжный чай с сибирским мёдом",
            "Охраняемая парковка на территории",
            "Банные простыни и шапочки"
        ])
    else:
        small_name = f"Сруб «{name}»"
        small_cap = cap
        small_max = cap + 4
        small_wd = price_wd
        small_we = price_we
        small_min = "от 2 часов"
        small_desc = "Парная на дровах, комната отдыха, душ, чайник, посуда, зона барбекю."
        small_btn = "Забронировать сруб"

        big_name = f"Большой комплекс «{name}» с чаном"
        big_cap = cap
        big_max = cap + 7
        big_wd = price_wd + 500
        big_we = price_we + 500
        big_water = chan_note
        big_desc = "Кедровая парная, просторная трапезная, горячий уличный чан на дровах, мангал."
        big_btn = "Забронировать с чаном"

        house_name = "Пакет «Таёжный вечер (5 часов)»"
        house_cap = 6
        house_max = 6
        house_wd = price_wd * 4
        house_we = price_we * 4
        house_dur = "5 часов отдыха"
        house_inc = "Мангал, чай, веник"
        house_desc = "Полные 5 часов аренды комплекса, мангальная зона, сибирский травяной чай, банный веник в подарок."
        house_btn = "Заказать пакет 5 часов"

        chan_val = chan_price
        chan_price_str = f"{chan_price:,}&nbsp;₽ / топка"
        brooms_note = "Свежий пихтовый или дубовый веник (от 400 ₽)"
        master_note = "Банный ритуал и таёжные запарки (2 000 ₽)"
        extra_guest_str = f"{extra_guest:,}&nbsp;₽ / за всё время"
        included_list = [
            "Зона барбекю, решётки, шампуры и посуда",
            "Таёжный чай с сибирским мёдом",
            "Охраняемая парковка на территории",
            "Питьевая артезианская вода"
        ]"""

assert old_halls_block in text, "old_halls_block not found in build_landing.py!"
text = text.replace(old_halls_block, new_halls_block, 1)

# 2. Replace the ptable_rows & extra_services block (lines 241-306)
old_ptable_block = """    if slug == "kedrovy-log":
        ptable_rows = f\"\"\"
          <tr><td>Одноэтажная баня на Базаихе<span class="sub">Русская парная на дровах, комната отдыха, мангал</span></td><td>{price_wd:,}&nbsp;₽</td><td>3 500&nbsp;₽</td><td>до {cap} гостей</td><td>2 часа</td></tr>
          <tr><td>Двухэтажная баня на дровах<span class="sub">Просторная парная, гостиная, веранда у реки Базаиха</span></td><td>3 800&nbsp;₽</td><td>{price_we:,}&nbsp;₽</td><td>до {cap} гостей</td><td>3 часа</td></tr>
          <tr><td>Пакет «Таёжный вечер — Базаиха Релакс»<span class="sub">В четверг при заказе 3 часов — 4-й час в подарок!</span></td><td>{price_wd * 3:,}&nbsp;₽</td><td>10 500&nbsp;₽</td><td>до {cap} гостей</td><td>4 часа</td></tr>
        \"\"\"
        extra_services = f\"\"\"
          <li><span>Тёплая купель на всё время пребывания</span><span>5&nbsp;500&nbsp;₽</span></li>
          <li><span>Холодная купель на всё время пребывания</span><span>4&nbsp;500&nbsp;₽</span></li>
          <li><span>Свежие веники (пихта, дуб, берёза)</span><span>550&nbsp;₽ / шт</span></li>
          <li><span>Дополнительный гость (свыше {cap} человек)</span><span>{extra_guest:,}&nbsp;₽ / за всё время</span></li>
        \"\"\"
        included_services = \"\"\"
          <li><span>Комплименты: мёд, джем, сушки, вода с лимоном и розмарином, травяной чай</span><span>0&nbsp;₽</span></li>
          <li><span>Банный текстиль: полотенца, шапочки, тапочки</span><span>0&nbsp;₽</span></li>
          <li><span>Мангальная зона, решётки и шампуры</span><span>0&nbsp;₽</span></li>
          <li><span>Охраняемая парковка на Базаихе</span><span>0&nbsp;₽</span></li>
        \"\"\"
    else:
        ptable_rows = f\"\"\"
          <tr><td>Сруб «{name}»<span class="sub">Русская парная на дровах, комната отдыха, мангал</span></td><td>{price_wd:,}&nbsp;₽</td><td>{price_we:,}&nbsp;₽</td><td>{cap} гостей</td><td>2 часа</td></tr>
          <tr><td>Большой комплекс с чаном<span class="sub">Просторная парная, горячая уличная купель, сосны</span></td><td>{price_wd + 500:,}&nbsp;₽</td><td>{price_we + 500:,}&nbsp;₽</td><td>{cap} гостей</td><td>3 часа</td></tr>
          <tr><td>Пакет «Таёжный вечер»<span class="sub">5 часов отдыха, мангал, чай, веник в подарок</span></td><td>{price_wd * 4:,}&nbsp;₽</td><td>{price_we * 4:,}&nbsp;₽</td><td>до {cap} гостей</td><td>5 часов</td></tr>
        \"\"\"
        extra_services = f\"\"\"
          <li><span>{chan_note}</span><span>{chan_price:,}&nbsp;₽ / топка</span></li>
          <li><span>Свежий пихтовый или дубовый веник</span><span>от 400&nbsp;₽ / шт</span></li>
          <li><span>Банный ритуал и таёжные запарки</span><span>2&nbsp;000&nbsp;₽</span></li>
          <li><span>Дополнительный гость (с {cap+1}-го человека)</span><span>{extra_guest:,}&nbsp;₽ / за всё время</span></li>
        \"\"\"
        included_services = \"\"\"
          <li><span>Зона барбекю, решётки, шампуры и посуда</span><span>0&nbsp;₽</span></li>
          <li><span>Таёжный чай с сибирским мёдом</span><span>0&nbsp;₽</span></li>
          <li><span>Охраняемая парковка на территории</span><span>0&nbsp;₽</span></li>
          <li><span>Питьевая артезианская вода</span><span>0&nbsp;₽</span></li>
        \"\"\"

    meta_title = f\"Банный комплекс «{name}» — баня на дровах и купели в Красноярске ({address})\"
    meta_desc = f\"Банный комплекс «{name}» в Красноярске: русская парная на дровах, {chan_note.lower()}, зона барбекю. От {price_wd:,} ₽/час. {cap} гостей включено в цену! Рейтинг ★ 5.0.\"
    canonical_url = f\"https://ti-kan.github.io/banya-base/b/{slug}/\" if not is_root else \"https://ti-kan.github.io/banya-base/\"

    html = f\"\"\"<!doctype html>
<html lang=\"ru\" class=\"js\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">
<script>document.documentElement.classList.add('js');</script>
<title>{meta_title}</title>
<meta name=\"description\" content=\"{meta_desc}\">
<link rel=\"canonical\" href=\"{canonical_url}\">
<meta property=\"og:type\" content=\"website\">
<meta property=\"og:url\" content=\"{canonical_url}\">
<meta property=\"og:title\" content=\"{meta_title}\">
<meta property=\"og:description\" content=\"{meta_desc}\">
<meta property=\"og:image\" content=\"https://ti-kan.github.io/banya-base/img/hero-1200.jpg\">
<meta property=\"og:image:width\" content=\"1200\">
<meta property=\"og:image:height\" content=\"630\">
<meta property=\"og:locale\" content=\"ru_RU\">
<meta property=\"og:site_name\" content=\"Банный комплекс «{name}»\">
<meta name=\"twitter:card\" content=\"summary_large_image\">
<meta name=\"twitter:title\" content=\"{meta_title}\">
<meta name=\"twitter:description\" content=\"{meta_desc}\">
<meta name=\"twitter:image\" content=\"https://ti-kan.github.io/banya-base/img/hero-1200.jpg\">
<meta name=\"theme-color\" content=\"#ffffff\">
<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230b0c0e'/%3E%3Cpath d='M8 23h16M10 23V14l6-5 6 5v9' stroke='%23cc3d0b' stroke-width='2.6' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E\">
<link rel=\"preload\" href=\"{asset_prefix}fonts/oswald.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>
<link rel=\"preload\" href=\"{asset_prefix}fonts/onest.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>
<link rel=\"preload\" as=\"image\" type=\"image/avif\" imagesrcset=\"{asset_prefix}img/hero-480.avif 480w, {asset_prefix}img/hero-720.avif 720w, {asset_prefix}img/hero-1200.avif 1200w\" imagesizes=\"(min-width: 1024px) 700px, calc(100vw - 32px)\" fetchpriority=\"high\">"""

new_ptable_block = """    ptable_rows = f\"\"\"
      <tr><td>{small_name}<span class="sub">{small_desc}</span></td><td>{small_wd:,}&nbsp;₽</td><td>{small_we:,}&nbsp;₽</td><td>{small_cap} гостей</td><td>{small_min}</td></tr>
      <tr><td>{big_name}<span class="sub">{big_desc}</span></td><td>{big_wd:,}&nbsp;₽</td><td>{big_we:,}&nbsp;₽</td><td>до {big_max} гостей</td><td>{big_water}</td></tr>
      <tr><td>{house_name}<span class="sub">{house_desc}</span></td><td>{house_wd:,}&nbsp;₽</td><td>{house_we:,}&nbsp;₽</td><td>до {big_max} гостей</td><td>{house_dur}</td></tr>
    \"\"\"

    extra_services = f\"\"\"
      <li><span>{chan_note}</span><span>{chan_price_str}</span></li>
      <li><span>{brooms_note}</span><span>от 450&nbsp;₽ / шт</span></li>
      <li><span>{master_note}</span><span>2&nbsp;000&nbsp;₽</span></li>
      <li><span>Дополнительный гость</span><span>{extra_guest_str}</span></li>
    \"\"\"

    included_services = "\\n".join([f'      <li><span>{item}</span><span>0&nbsp;₽</span></li>' for item in included_list])

    # Photo paths (relative to page)
    hero_avif_srcset = f"{asset_prefix}img/venues/{slug}/hero-480.avif 480w, {asset_prefix}img/venues/{slug}/hero-720.avif 720w, {asset_prefix}img/venues/{slug}/hero-1200.avif 1200w"
    hero_jpg_srcset = f"{asset_prefix}img/venues/{slug}/hero-480.jpg 480w, {asset_prefix}img/venues/{slug}/hero-720.jpg 720w, {asset_prefix}img/venues/{slug}/hero-1200.jpg 1200w"
    hero_src = f"{asset_prefix}img/venues/{slug}/hero-720.jpg"

    hall1_1_src = f"{asset_prefix}img/venues/{slug}/hall1_1-720.jpg"
    hall1_1_srcset = f"{asset_prefix}img/venues/{slug}/hall1_1-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall1_1-720.jpg 720w"
    hall1_2_src = f"{asset_prefix}img/venues/{slug}/hall1_2-720.jpg"
    hall1_2_srcset = f"{asset_prefix}img/venues/{slug}/hall1_2-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall1_2-720.jpg 720w"
    hall1_3_src = f"{asset_prefix}img/venues/{slug}/hall1_3-720.jpg"
    hall1_3_srcset = f"{asset_prefix}img/venues/{slug}/hall1_3-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall1_3-720.jpg 720w"

    hall2_1_src = f"{asset_prefix}img/venues/{slug}/hall2_1-720.jpg"
    hall2_1_srcset = f"{asset_prefix}img/venues/{slug}/hall2_1-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall2_1-720.jpg 720w"
    hall2_2_src = f"{asset_prefix}img/venues/{slug}/hall2_2-720.jpg"
    hall2_2_srcset = f"{asset_prefix}img/venues/{slug}/hall2_2-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall2_2-720.jpg 720w"
    hall2_3_src = f"{asset_prefix}img/venues/{slug}/hall2_3-720.jpg"
    hall2_3_srcset = f"{asset_prefix}img/venues/{slug}/hall2_3-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall2_3-720.jpg 720w"

    hall3_1_src = f"{asset_prefix}img/venues/{slug}/hall3_1-720.jpg"
    hall3_1_srcset = f"{asset_prefix}img/venues/{slug}/hall3_1-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall3_1-720.jpg 720w"
    hall3_2_src = f"{asset_prefix}img/venues/{slug}/hall3_2-720.jpg"
    hall3_2_srcset = f"{asset_prefix}img/venues/{slug}/hall3_2-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall3_2-720.jpg 720w"
    hall3_3_src = f"{asset_prefix}img/venues/{slug}/hall3_3-720.jpg"
    hall3_3_srcset = f"{asset_prefix}img/venues/{slug}/hall3_3-480.jpg 480w, {asset_prefix}img/venues/{slug}/hall3_3-720.jpg 720w"

    rituals_avif_srcset = f"{asset_prefix}img/venues/{slug}/rituals-480.avif 480w, {asset_prefix}img/venues/{slug}/rituals-800.avif 800w"
    rituals_jpg_srcset = f"{asset_prefix}img/venues/{slug}/rituals-480.jpg 480w, {asset_prefix}img/venues/{slug}/rituals-800.jpg 800w"
    rituals_src = f"{asset_prefix}img/venues/{slug}/rituals-800.jpg"

    meta_title = f\"Банный комплекс «{name}» — баня на дровах и купели в Красноярске ({address})\"
    meta_desc = f\"Банный комплекс «{name}» в Красноярске: {small_name}, {big_name}, {chan_note.lower()}, зона барбекю. От {small_wd:,} ₽/час. {small_cap} гостей включено в цену! Рейтинг ★ 5.0.\"
    canonical_url = f\"https://ti-kan.github.io/banya-base/b/{slug}/\" if not is_root else \"https://ti-kan.github.io/banya-base/\"
    og_image = f\"https://ti-kan.github.io/banya-base/img/venues/{slug}/hero-720.jpg\"

    html = f\"\"\"<!doctype html>
<html lang=\"ru\" class=\"js\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">
<script>document.documentElement.classList.add('js');</script>
<title>{meta_title}</title>
<meta name=\"description\" content=\"{meta_desc}\">
<link rel=\"canonical\" href=\"{canonical_url}\">
<meta property=\"og:type\" content=\"website\">
<meta property=\"og:url\" content=\"{canonical_url}\">
<meta property=\"og:title\" content=\"{meta_title}\">
<meta property=\"og:description\" content=\"{meta_desc}\">
<meta property=\"og:image\" content=\"{og_image}\">
<meta property=\"og:image:width\" content=\"1200\">
<meta property=\"og:image:height\" content=\"630\">
<meta property=\"og:locale\" content=\"ru_RU\">
<meta property=\"og:site_name\" content=\"Банный комплекс «{name}»\">
<meta name=\"twitter:card\" content=\"summary_large_image\">
<meta name=\"twitter:title\" content=\"{meta_title}\">
<meta name=\"twitter:description\" content=\"{meta_desc}\">
<meta name=\"twitter:image\" content=\"{og_image}\">
<meta name=\"theme-color\" content=\"#ffffff\">
<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230b0c0e'/%3E%3Cpath d='M8 23h16M10 23V14l6-5 6 5v9' stroke='%23cc3d0b' stroke-width='2.6' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E\">
<link rel=\"preload\" href=\"{asset_prefix}fonts/oswald.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>
<link rel=\"preload\" href=\"{asset_prefix}fonts/onest.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>
<link rel=\"preload\" as=\"image\" type=\"image/avif\" imagesrcset=\"{hero_avif_srcset}\" imagesizes=\"(min-width: 1024px) 700px, calc(100vw - 32px)\" fetchpriority=\"high\">"""

assert old_ptable_block in text, "old_ptable_block not found in build_landing.py!"
text = text.replace(old_ptable_block, new_ptable_block, 1)

# 3. Replace Hero picture
old_hero_pic = """        <picture>
          <source type="image/avif" srcset="{asset_prefix}img/hero-480.avif 480w, {asset_prefix}img/hero-720.avif 720w, {asset_prefix}img/hero-1200.avif 1200w" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)">
          <img src="{asset_prefix}img/hero-720.jpg" srcset="{asset_prefix}img/hero-480.jpg 480w, {asset_prefix}img/hero-720.jpg 720w, {asset_prefix}img/hero-1200.jpg 1200w" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)" width="720" height="518" alt="Банный комплекс {name}: сруб на дровах, горячая купель и зона барбекю" loading="eager" decoding="async" fetchpriority="high">
        </picture>"""

new_hero_pic = """        <picture>
          <source type="image/avif" srcset="{hero_avif_srcset}" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)">
          <img src="{hero_src}" srcset="{hero_jpg_srcset}" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)" width="720" height="518" alt="Банный комплекс {name}: сруб на дровах, горячая купель и зона барбекю" loading="eager" decoding="async" fetchpriority="high">
        </picture>"""

assert old_hero_pic in text, "old_hero_pic not found in build_landing.py!"
text = text.replace(old_hero_pic, new_hero_pic, 1)

# 4. Replace Bath Cards
old_cards = """      <article class="bath reveal" id="bath-small">
        <div class="strip">
          <figure><img src="{asset_prefix}img/malaya-720.jpg" srcset="{asset_prefix}img/malaya-480.jpg 480w, {asset_prefix}img/malaya-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Парная на дровах {name}"><figcaption>Парная</figcaption></figure>
          <figure><img src="{asset_prefix}img/otdyh-720.jpg" srcset="{asset_prefix}img/otdyh-480.jpg 480w, {asset_prefix}img/otdyh-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Комната отдыха"><figcaption>Отдых</figcaption></figure>
          <figure><img src="{asset_prefix}img/terrasa-720.jpg" srcset="{asset_prefix}img/terrasa-480.jpg 480w, {asset_prefix}img/terrasa-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Терраса с мангалом"><figcaption>Терраса</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>Сруб «{name}»</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{price_wd:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Выходные</dt><dd><b>{price_we:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Вместимость</dt><dd>{cap} гостей в цене</dd></div>
            <div><dt>Минимум</dt><dd>от 2 часов</dd></div>
          </dl>
          <p class="incl">Парная на дровах, комната отдыха, душ, чайник, посуда, зона барбекю.</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="small">Забронировать сруб</button>
        </div>
      </article>

      <article class="bath reveal" id="bath-big">
        <div class="strip">
          <figure><img src="{asset_prefix}img/chan-720.jpg" srcset="{asset_prefix}img/chan-480.jpg 480w, {asset_prefix}img/chan-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Горячий чан под открытым небом"><figcaption>Горячий чан</figcaption></figure>
          <figure><img src="{asset_prefix}img/parnaya-b-720.jpg" srcset="{asset_prefix}img/parnaya-b-480.jpg 480w, {asset_prefix}img/parnaya-b-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Большая парная"><figcaption>Парная</figcaption></figure>
          <figure><img src="{asset_prefix}img/srub-720.jpg" srcset="{asset_prefix}img/srub-480.jpg 480w, {asset_prefix}img/srub-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Сруб из кедра"><figcaption>Сруб</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>Большой сруб с чаном</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{price_wd + 500:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Выходные</dt><dd><b>{price_we + 500:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Вместимость</dt><dd>{cap} гостей в цене (до {cap+7})</dd></div>
            <div><dt>Купель</dt><dd>{chan_note}</dd></div>
          </dl>
          <p class="incl">Кедровая парная, просторная трапезная, горячий уличный чан на дровах, мангал.</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="big">Забронировать с чаном</button>
        </div>
      </article>

      <article class="bath reveal" id="bath-house">
        <div class="strip">
          <figure><img src="{asset_prefix}img/domik-720.jpg" srcset="{asset_prefix}img/domik-480.jpg 480w, {asset_prefix}img/domik-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Гостевой домик с баней"><figcaption>Домик</figcaption></figure>
          <figure><img src="{asset_prefix}img/otdyh-720.jpg" srcset="{asset_prefix}img/otdyh-480.jpg 480w, {asset_prefix}img/otdyh-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Спальная зона"><figcaption>Спальня</figcaption></figure>
          <figure><img src="{asset_prefix}img/terrasa-720.jpg" srcset="{asset_prefix}img/terrasa-480.jpg 480w, {asset_prefix}img/terrasa-720.jpg 720w" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Мангальная зона"><figcaption>Мангал</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>Пакет «Таёжный вечер»</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{price_wd * 4:,}&nbsp;₽</b>/пакет</dd></div>
            <div><dt>Выходные</dt><dd><b>{price_we * 4:,}&nbsp;₽</b>/пакет</dd></div>
            <div><dt>Длительность</dt><dd>5 часов отдыха</dd></div>
            <div><dt>Включено</dt><dd>Мангал, чай, веник</dd></div>
          </dl>
          <p class="incl">Полные 5 часов аренды комплекса, мангальная зона, сибирский травяной чай, банный веник в подарок.</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="house">Заказать пакет 5 часов</button>
        </div>
      </article>"""

new_cards = """      <article class="bath reveal" id="bath-small">
        <div class="strip">
          <figure><img src="{hall1_1_src}" srcset="{hall1_1_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Парная {name}"><figcaption>Парная</figcaption></figure>
          <figure><img src="{hall1_2_src}" srcset="{hall1_2_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Комната отдыха"><figcaption>Отдых</figcaption></figure>
          <figure><img src="{hall1_3_src}" srcset="{hall1_3_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Терраса с мангалом"><figcaption>Терраса</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>{small_name}</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{small_wd:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Выходные</dt><dd><b>{small_we:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Вместимость</dt><dd>{small_cap} гостей в цене</dd></div>
            <div><dt>Минимум</dt><dd>{small_min}</dd></div>
          </dl>
          <p class="incl">{small_desc}</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="small">{small_btn}</button>
        </div>
      </article>

      <article class="bath reveal" id="bath-big">
        <div class="strip">
          <figure><img src="{hall2_1_src}" srcset="{hall2_1_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Горячий чан под открытым небом"><figcaption>Купель / чан</figcaption></figure>
          <figure><img src="{hall2_2_src}" srcset="{hall2_2_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Большая парная"><figcaption>Парная</figcaption></figure>
          <figure><img src="{hall2_3_src}" srcset="{hall2_3_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Банный сруб"><figcaption>Сруб</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>{big_name}</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{big_wd:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Выходные</dt><dd><b>{big_we:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Вместимость</dt><dd>{big_cap} гостей в цене (до {big_max})</dd></div>
            <div><dt>Купель</dt><dd>{big_water}</dd></div>
          </dl>
          <p class="incl">{big_desc}</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="big">{big_btn}</button>
        </div>
      </article>

      <article class="bath reveal" id="bath-house">
        <div class="strip">
          <figure><img src="{hall3_1_src}" srcset="{hall3_1_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Гостевой домик с баней"><figcaption>Домик</figcaption></figure>
          <figure><img src="{hall3_2_src}" srcset="{hall3_2_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Спальная зона"><figcaption>Гостиная</figcaption></figure>
          <figure><img src="{hall3_3_src}" srcset="{hall3_3_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Мангальная зона"><figcaption>Мангал</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>{house_name}</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{house_wd:,}&nbsp;₽</b>/пакет</dd></div>
            <div><dt>Выходные</dt><dd><b>{house_we:,}&nbsp;₽</b>/пакет</dd></div>
            <div><dt>Длительность</dt><dd>{house_dur}</dd></div>
            <div><dt>Включено</dt><dd>{house_inc}</dd></div>
          </dl>
          <p class="incl">{house_desc}</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="house">{house_btn}</button>
        </div>
      </article>"""

assert old_cards in text, "old_cards not found in build_landing.py!"
text = text.replace(old_cards, new_cards, 1)

# 5. Replace Rituals picture
old_rituals_pic = """    <div class="master reveal" id="ritualsCard">
      <picture>
        <source type="image/avif" srcset="{asset_prefix}img/rituals-480.avif 480w, {asset_prefix}img/rituals-800.avif 800w" sizes="(min-width:1024px) 420px, (min-width:760px) 360px, calc(100vw - 32px)">
        <img src="{asset_prefix}img/rituals-800.jpg" srcset="{asset_prefix}img/rituals-480.jpg 480w, {asset_prefix}img/rituals-800.jpg 800w" sizes="(min-width:1024px) 420px, (min-width:760px) 360px, calc(100vw - 32px)" width="800" height="600" alt="Банные ритуалы, веники и сибирский чан на травах">
      </picture>"""

new_rituals_pic = """    <div class="master reveal" id="ritualsCard">
      <picture>
        <source type="image/avif" srcset="{rituals_avif_srcset}" sizes="(min-width:1024px) 420px, (min-width:760px) 360px, calc(100vw - 32px)">
        <img src="{rituals_src}" srcset="{rituals_jpg_srcset}" sizes="(min-width:1024px) 420px, (min-width:760px) 360px, calc(100vw - 32px)" width="800" height="600" alt="Банные ритуалы, веники и сибирский чан в {name}">
      </picture>"""

assert old_rituals_pic in text, "old_rituals_pic not found in build_landing.py!"
text = text.replace(old_rituals_pic, new_rituals_pic, 1)

with open(BUILD_SCRIPT, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully injected personalized data & photos engine into build_landing.py!")
