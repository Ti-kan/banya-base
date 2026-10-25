"""
Patcher for build_landing.py to inject personalized venue data & photos.
"""

BUILD_SCRIPT = "/Users/takanov/banya-base/scripts/build_landing.py"

with open(BUILD_SCRIPT, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Replace the venue facts & headings block
old_block_1 = """    if slug == "kedrovy-log":
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

new_block_1 = """    c_data = CUSTOM_DATA.get(slug, {})
    if c_data:
        name = c_data.get("name", name)
        address = c_data.get("address", address)
        phone = c_data.get("phone", phone)
        rating = c_data.get("rating", 5.0)
        halls = c_data.get("halls", [])
        chan_price_str = c_data.get("chan_price", "3 000 ₽ / топка")
        chan_note = c_data.get("chan_note", chan_note)
        brooms_note = c_data.get("brooms_note", "Свежий пихтовый или дубовый веник (от 450 ₽)")
        master_note = c_data.get("master_note", "Банный ритуал и таёжные запарки (2 000 ₽)")
        extra_guest = c_data.get("extra_guest", "300 ₽ / час (свыше нормы)")
        included_list = c_data.get("included_list", [
            "Зона барбекю, решётки, шампуры и посуда",
            "Таёжный чай с сибирским мёдом",
            "Охраняемая парковка на территории",
            "Банные простыни и шапочки"
        ])
    else:
        halls = []
        included_list = [
            "Зона барбекю, решётки, шампуры и посуда",
            "Таёжный чай с сибирским мёдом",
            "Охраняемая парковка на территории",
            "Питьевая артезианская вода"
        ]

    hall1 = halls[0] if len(halls) > 0 else {}
    hall2 = halls[1] if len(halls) > 1 else {}
    hall3 = halls[2] if len(halls) > 2 else {}

    hall1_title = hall1.get("title", f"Сруб «{name}»")
    hall1_pwd = hall1.get("price_wd", price_wd)
    hall1_pwe = hall1.get("price_we", price_we)
    hall1_cap = hall1.get("cap", cap)
    hall1_min = hall1.get("min_hours", "от 2 часов")
    hall1_desc = hall1.get("desc", "Парная на дровах, комната отдыха, душ, чайник, посуда, зона барбекю.")
    hall1_btn = hall1.get("btn_text", "Забронировать сруб")

    hall2_title = hall2.get("title", f"Большой комплекс с чаном")
    hall2_pwd = hall2.get("price_wd", price_wd + 500)
    hall2_pwe = hall2.get("price_we", price_we + 500)
    hall2_cap = hall2.get("cap", cap)
    hall2_cap_max = hall2.get("cap_max", cap + 7)
    hall2_water = hall2.get("water_note", chan_note)
    hall2_desc = hall2.get("desc", "Кедровая парная, просторная трапезная, горячий уличный чан на дровах, мангал.")
    hall2_btn = hall2.get("btn_text", "Забронировать с чаном")

    hall3_title = hall3.get("title", f"Пакет «Таёжный вечер»")
    hall3_pwd = hall3.get("price_wd", price_wd * 4)
    hall3_pwe = hall3.get("price_we", price_we * 4)
    hall3_dur = hall3.get("duration", "5 часов отдыха")
    hall3_inc = hall3.get("included", "Мангал, чай, веник")
    hall3_desc = hall3.get("desc", "Полные 5 часов аренды комплекса, мангальная зона, сибирский травяной чай, банный веник в подарок.")
    hall3_btn = hall3.get("btn_text", "Заказать пакет 5 часов")

    ptable_rows = f\"\"\"
      <tr><td>{hall1_title}<span class="sub">{hall1_desc}</span></td><td>{hall1_pwd:,}&nbsp;₽</td><td>{hall1_pwe:,}&nbsp;₽</td><td>{hall1_cap} гостей</td><td>{hall1_min}</td></tr>
      <tr><td>{hall2_title}<span class="sub">{hall2_desc}</span></td><td>{hall2_pwd:,}&nbsp;₽</td><td>{hall2_pwe:,}&nbsp;₽</td><td>до {hall2_cap_max} гостей</td><td>{hall2_water}</td></tr>
      <tr><td>{hall3_title}<span class="sub">{hall3_desc}</span></td><td>{hall3_pwd:,}&nbsp;₽</td><td>{hall3_pwe:,}&nbsp;₽</td><td>до {hall2_cap_max} гостей</td><td>{hall3_dur}</td></tr>
    \"\"\"

    extra_services = f\"\"\"
      <li><span>{chan_note}</span><span>{c_data.get('chan_price', '3 000 ₽ / топка')}</span></li>
      <li><span>Свежий пихтовый или дубовый веник</span><span>от 450&nbsp;₽ / шт</span></li>
      <li><span>Банный ритуал и таёжные запарки</span><span>2&nbsp;000&nbsp;₽</span></li>
      <li><span>Дополнительный гость</span><span>{extra_guest}</span></li>
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
    meta_desc = f\"Банный комплекс «{name}» в Красноярске: {hall1_title}, {hall2_title}, {chan_note.lower()}, зона барбекю. От {hall1_pwd:,} ₽/час. Рейтинг ★ 5.0.\"
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

assert old_block_1 in code, "old_block_1 not found in build_landing.py!"
code = code.replace(old_block_1, new_block_1, 1)

# 2. Replace Hero picture
old_hero_pic = """        <picture>
          <source type="image/avif" srcset="{asset_prefix}img/hero-480.avif 480w, {asset_prefix}img/hero-720.avif 720w, {asset_prefix}img/hero-1200.avif 1200w" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)">
          <img src="{asset_prefix}img/hero-720.jpg" srcset="{asset_prefix}img/hero-480.jpg 480w, {asset_prefix}img/hero-720.jpg 720w, {asset_prefix}img/hero-1200.jpg 1200w" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)" width="720" height="518" alt="Банный комплекс {name}: сруб на дровах, горячая купель и зона барбекю" loading="eager" decoding="async" fetchpriority="high">
        </picture>"""

new_hero_pic = """        <picture>
          <source type="image/avif" srcset="{hero_avif_srcset}" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)">
          <img src="{hero_src}" srcset="{hero_jpg_srcset}" sizes="(min-width: 1024px) 700px, calc(100vw - 32px)" width="720" height="518" alt="Банный комплекс {name}: сруб на дровах, горячая купель и зона барбекю" loading="eager" decoding="async" fetchpriority="high">
        </picture>"""

assert old_hero_pic in code, "old_hero_pic not found in build_landing.py!"
code = code.replace(old_hero_pic, new_hero_pic, 1)

# 3. Replace Bath Cards
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
          <h3>{hall1_title}</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{hall1_pwd:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Выходные</dt><dd><b>{hall1_pwe:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Вместимость</dt><dd>{hall1_cap} гостей в цене</dd></div>
            <div><dt>Минимум</dt><dd>{hall1_min}</dd></div>
          </dl>
          <p class="incl">{hall1_desc}</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="small">{hall1_btn}</button>
        </div>
      </article>

      <article class="bath reveal" id="bath-big">
        <div class="strip">
          <figure><img src="{hall2_1_src}" srcset="{hall2_1_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Горячий чан под открытым небом"><figcaption>Купель / чан</figcaption></figure>
          <figure><img src="{hall2_2_src}" srcset="{hall2_2_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Большая парная"><figcaption>Парная</figcaption></figure>
          <figure><img src="{hall2_3_src}" srcset="{hall2_3_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Банный сруб"><figcaption>Сруб</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>{hall2_title}</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{hall2_pwd:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Выходные</dt><dd><b>{hall2_pwe:,}&nbsp;₽</b>/час</dd></div>
            <div><dt>Вместимость</dt><dd>{hall2_cap} гостей в цене (до {hall2_cap_max})</dd></div>
            <div><dt>Купель</dt><dd>{hall2_water}</dd></div>
          </dl>
          <p class="incl">{hall2_desc}</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="big">{hall2_btn}</button>
        </div>
      </article>

      <article class="bath reveal" id="bath-house">
        <div class="strip">
          <figure><img src="{hall3_1_src}" srcset="{hall3_1_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Гостевой домик с баней"><figcaption>Домик</figcaption></figure>
          <figure><img src="{hall3_2_src}" srcset="{hall3_2_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Спальная зона"><figcaption>Гостиная</figcaption></figure>
          <figure><img src="{hall3_3_src}" srcset="{hall3_3_srcset}" sizes="(min-width: 900px) 30vw, 84vw" width="720" height="540" alt="Мангальная зона"><figcaption>Мангал</figcaption></figure>
        </div>
        <div class="bath-b">
          <h3>{hall3_title}</h3>
          <dl class="bfacts">
            <div><dt>Будни</dt><dd><b>{hall3_pwd:,}&nbsp;₽</b>/пакет</dd></div>
            <div><dt>Выходные</dt><dd><b>{hall3_pwe:,}&nbsp;₽</b>/пакет</dd></div>
            <div><dt>Длительность</dt><dd>{hall3_dur}</dd></div>
            <div><dt>Включено</dt><dd>{hall3_inc}</dd></div>
          </dl>
          <p class="incl">{hall3_desc}</p>
          <button class="btn btn-accent btn-wide" type="button" data-book="house">{hall3_btn}</button>
        </div>
      </article>"""

assert old_cards in code, "old_cards not found in build_landing.py!"
code = code.replace(old_cards, new_cards, 1)

# 4. Replace Rituals picture
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

assert old_rituals_pic in code, "old_rituals_pic not found in build_landing.py!"
code = code.replace(old_rituals_pic, new_rituals_pic, 1)

with open(BUILD_SCRIPT, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully patched build_landing.py with 100% personalized data and photos!")
