import sys, json, urllib.parse, os
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008/"
if not URL.endswith("/"): URL += "/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/shots"
os.makedirs(OUT, exist_ok=True)

DEVICES = [
    ("android-360", 360, 740, 3, True),
    ("iphone-se-375", 375, 667, 2, True),
    ("iphone-14-390", 390, 844, 3, True),
    ("pixel-7-412", 412, 915, 2.625, True),
    ("iphone-max-430", 430, 932, 3, True),
    ("tablet-768", 768, 1024, 2, True),
    ("laptop-1024", 1024, 768, 1, False),
    ("laptop-1280", 1280, 800, 1, False),
    ("laptop-1366", 1366, 768, 1, False),
    ("desktop-1440", 1440, 900, 1, False),
    ("desktop-1920", 1920, 1080, 1, False),
]
problems = []
def bad(dev, msg):
    problems.append(f"[{dev}] {msg}")

FIRST_SCREEN_JS = """() => {
  const vh = innerHeight, r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return {top:b.top, bottom:b.bottom, h:b.height}; };
  return {vh, overflow: Math.max(document.documentElement.scrollWidth, innerWidth) - (window.__devw||innerWidth),
    dock: (document.querySelector('.dock')||{}).getBoundingClientRect ? document.querySelector('.dock').getBoundingClientRect().height : 0,
    call: r('.top .round'), h1: r('#h1'), from: r('.facts div:first-child dd'), where: r('.brand span'), img: r('.frame img'), dockcall: r('.dock a[href^=tel]'),
    num: r('.top-num'), frame: r('.frame'), rating: r('.facts div:nth-child(2) dd'),
    head: (() => { const g = s => document.querySelector(s).getBoundingClientRect(); const n = g('.topnav');
      return n.width ? {brand: g('.brand').right, navL: n.left, navR: n.right, act: g('.top-act').left} : null; })()};
}"""
TAP_JS = """() => {
  const out = [];
  document.querySelectorAll('a[href], button, .chip').forEach(e => {
    const b = e.getBoundingClientRect(), cs = getComputedStyle(e);
    if (!b.width || !b.height || cs.visibility === 'hidden' || e.closest('dialog:not([open])') || e.closest('[hidden]')) return;
    if (e.closest('.rev, footer, .revhead, .rating, .dl, .cookie')) return; // ссылки внутри текста — по правилам можно меньше
    if (b.height < 44 || b.width < 44) out.push((e.className || e.tagName) + ' ' + (e.textContent||'').trim().slice(0,30) + ' ' + Math.round(b.width) + 'x' + Math.round(b.height));
  });
  return out;
}"""
SMALLTEXT_JS = """() => {
  const out = new Set();
  document.querySelectorAll('body *').forEach(e => {
    if (!e.childNodes.length) return;
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) return; const b = e.getBoundingClientRect(); if (!b.width) return;
    if (e.closest('dialog:not([open])') || e.closest('[hidden]')) return;
    const fs = parseFloat(getComputedStyle(e).fontSize); if (fs < 12) out.add(e.tagName + '.' + e.className + ' ' + fs);
  });
  return [...out];
}"""

with sync_playwright() as p:
    br = p.chromium.launch()
    for name, w, h, dpr, mobile in DEVICES:
        ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile, locale="ru-RU")
        pg = ctx.new_page()
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        failed = []
        pg.on("requestfailed", lambda r: failed.append(r.url) if not (r.failure and "ERR_ABORTED" in str(r.failure)) else None)
        pg.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        pg.goto(URL, wait_until="networkidle")
        pg.evaluate(f"window.__devw={w}")
        fs = pg.evaluate(FIRST_SCREEN_JS)
        if fs["overflow"] > 0: bad(name, f"страница уезжает вбок на {fs['overflow']}px")
        if mobile:
            lim = fs["vh"] - (fs["dock"] if w < 900 else 0) + 1
            for k in ["call", "h1", "from", "where"]:
                if not fs[k] or fs[k]["bottom"] > lim: bad(name, f"первый экран: «{k}» не виден без прокрутки ({fs[k]}, граница {lim})")
            if not fs["img"] or fs["img"]["top"] > fs["vh"] * 0.6: bad(name, "первый экран: фото слишком низко")
            if w < 900 and (not fs["dockcall"] or fs["dockcall"]["bottom"] > fs["vh"] + 1): bad(name, "кнопка «Позвонить» внизу не видна")
        else:
            # компьютер: без прокрутки видны всё фото, что это, цена, рейтинг и телефон в шапке
            for k in ["h1", "from", "rating", "num", "frame"]:
                if not fs[k] or fs[k]["bottom"] > fs["vh"] + 1: bad(name, f"первый экран: «{k}» не виден без прокрутки ({fs[k]}, высота {fs['vh']})")
            hd = fs["head"]
            if w >= 1280 and not hd: bad(name, "меню разделов в шапке не показано")
            if hd and (hd["navL"] - hd["brand"] < 16 or hd["act"] - hd["navR"] < 16): bad(name, f"меню в шапке налезает на название или телефон: {hd}")
        taps = pg.evaluate(TAP_JS)
        if taps: bad(name, "мелкие кнопки: " + "; ".join(taps[:8]))
        small = pg.evaluate(SMALLTEXT_JS)
        if small: bad(name, "текст мельче 12px: " + "; ".join(small[:6]))
        pg.screenshot(path=f"{OUT}/{name}-first.png")
        hh = pg.evaluate("document.documentElement.scrollHeight")
        for yy in range(0, hh, 600):
            pg.evaluate(f"window.scrollTo(0,{yy})"); pg.wait_for_timeout(120)
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(900)
        pg.screenshot(path=f"{OUT}/{name}-full.png", full_page=True)
        # нижняя панель появляется после прокрутки
        if mobile and w < 900:
            pg.mouse.wheel(0, 1200); pg.wait_for_timeout(600)
            ov = pg.evaluate(f"Math.max(document.documentElement.scrollWidth, innerWidth) - {w}")
            if ov > 0: bad(name, f"после прокрутки страница уезжает вбок на {ov}px")
        if errors: bad(name, "ошибки в консоли: " + " | ".join(errors[:5]))
        if failed: bad(name, "не загрузилось: " + " | ".join(failed[:5]))
        ctx.close()

    # ---- сценарии на iPhone 14 ----
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True, locale="ru-RU")
    pg = ctx.new_page(); pg.goto(URL, wait_until="networkidle")
    def tg_text():
        href = pg.get_attribute("#toTg", "href")
        prefix = pg.evaluate("window.TG") + "?text="
        if not href.startswith(prefix): bad("сценарий", f"ссылка Telegram неверная: {href[:60]}")
        return urllib.parse.unquote(href.split("?text=", 1)[1]).replace("\xa0", " ")
    def is_open(): return pg.evaluate("document.getElementById('sheet').open")
    
    is_taiga = ("taiga" in URL.lower()) or (URL.rstrip("/").endswith("3008"))
    venue_brand = pg.evaluate("window.BRAND || 'Баня'")

    # 1. окно из свободного окна
    pg.locator(".slot").first.tap(); pg.wait_for_timeout(400)
    if not is_open(): bad("сценарий", "окно заявки не открылось по нажатию на свободное окно")
    t = tg_text()
    if "Окно:" not in t or "Подарок" not in t: bad("сценарий", "в тексте заявки из окна нет времени или подарка: " + t)
    pg.screenshot(path=f"{OUT}/sheet-slot.png")
    box = pg.locator("#sheet").bounding_box()
    if box["width"] > 390 or box["y"] + box["height"] > 845: bad("сценарий", f"окно заявки не помещается в экран: {box}")
    for sel in ["#toTg", "#toMax", "#sheet a[href^=tel]"]:
        b = pg.locator(sel).bounding_box()
        if not b or b["y"] + b["height"] > 844: bad("сценарий", f"кнопка {sel} в окне заявки не видна без прокрутки")
    pg.locator("#sheetX").tap(); pg.wait_for_timeout(300)
    if is_open(): bad("сценарий", "окно не закрылось крестиком")

    # 2. подбор: 6 гостей, пт–вс вечером, 4 часа, чан
    pg.locator("#pick").scroll_into_view_if_needed()
    plus = pg.locator('[data-step="1"]')
    minus = pg.locator('[data-step="-1"]')
    cur_g = int(pg.inner_text("#guests"))
    while cur_g < 6:
        plus.tap(); cur_g += 1
    while cur_g > 6:
        minus.tap(); cur_g -= 1
    pg.locator('label.opt:has(input[value="we-eve"])').tap()
    pg.locator('label.opt:has(input[name="hours"][value="4"])').tap()
    pg.locator('label.opt:has(input[value="chan"])').tap()
    pg.wait_for_timeout(200)
    res = pg.inner_text("#results").replace("\xa0", " ")
    if is_taiga and "20 000 ₽" not in res:
        bad("сценарий", "подбор 6 гостей, пт–вс, 4 часа, купель: ждал 20 000 ₽, увидел: " + res.replace("\n", " / ")[:200])
    elif "₽" not in res:
        bad("сценарий", "подбор: в результатах нет суммы: " + res[:160])
    pg.screenshot(path=f"{OUT}/pick-6.png")

    pg.locator('[data-pick="big"]').tap(); pg.wait_for_timeout(300)
    t = tg_text()
    if "Гостей: 6" not in t or "Часов: 4" not in t:
        bad("сценарий", f"в заявке из подбора нет гостей или часов: {t}")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    if is_open(): bad("сценарий", "окно не закрылось клавишей Esc")

    # 3. с ночёвкой
    pg.locator('label.opt:has(input[value="night"])').tap(); pg.wait_for_timeout(200)
    res = pg.inner_text("#results").replace("\xa0", " ")
    if "Таёжный вечер" not in res or "₽" not in res:
        bad("сценарий", "пакет 5 часов: ждал пакет 5 часов, увидел: " + res.replace("\n"," / ")[:240])
    hidden = pg.evaluate("document.getElementById('hoursQ').hidden")
    if not hidden: bad("сценарий", "при ночёвке вопрос про часы не спрятан")

    # 4. ночёвка на 8
    plus.tap(); plus.tap(); pg.wait_for_timeout(200)
    res = pg.inner_text("#results").replace("\xa0", " ")
    if "до 6 гостей" not in res and not is_taiga:
        pass
    elif is_taiga and "до 6 гостей" not in res:
        bad("сценарий", "ночёвка на 8: нет подсказки: " + res[:160])

    # 5. кнопки карточек, мастера, «Написать»
    for sel, need in [('[data-book="small"]', "Тайга 82" if is_taiga else venue_brand), ('[data-book="master"]', "ритуал"), ('.dock [data-book="any"]', "свободно")]:
        pg.mouse.wheel(0, 300); pg.locator(sel).first.scroll_into_view_if_needed(); pg.locator(sel).first.tap(); pg.wait_for_timeout(300)
        if not is_open(): bad("сценарий", f"{sel} не открыл окно"); continue
        if need not in tg_text(): bad("сценарий", f"{sel}: в тексте нет «{need}»")
        pg.locator("#sheetX").tap(); pg.wait_for_timeout(250)

    # 5б. окна не в прошлом
    past = pg.evaluate("""() => { const now = Date.now(); const out = [];
      document.querySelectorAll('.slot').forEach(b => { const t = b.querySelector('.s-time').textContent; const d = b.querySelector('.s-day').textContent;
        if (d.startsWith('Сегодня')) { const m = t.match(/(\\d\\d):(\\d\\d)/); const st = new Date(); st.setHours(+m[1], +m[2], 0, 0); if (st.getTime() < now + 29*60000) out.push(t); } });
      return {past: out, n: document.querySelectorAll('.slot').length}; }""")
    if past["past"]: bad("окна", f"показаны уже начавшиеся окна: {past['past']}")
    if past["n"] < 3: bad("окна", f"окон меньше трёх: {past['n']}")
    tgp = pg.get_attribute("#tgPlain", "href")
    if "?text=" not in tgp: bad("ссылки", "кнопка Telegram в контактах без готового текста")

    # 6. расчёт цен
    if is_taiga:
        cases = [
            ("small", dict(we=False, hours=2, guests=4, extras=[]), 2 * 2750),
            ("small", dict(we=True, hours=3, guests=2, extras=[]), 3 * 3250),
            ("big", dict(we=True, hours=3, guests=4, extras=[]), 3 * 3750),
            ("big", dict(we=True, hours=3, guests=4, extras=["chan"]), 3 * 3750 + 5000),
            ("big", dict(we=False, hours=2, guests=10, extras=[]), 3 * 3250 + 2 * 1000),
            ("house", dict(we=False, hours=3, guests=6, extras=[]), 11000),
            ("small", dict(we=False, hours=3, guests=4, extras=["chan"]), 3 * 2750),
        ]
        for k, o, want in cases:
            got = pg.evaluate("([k,o]) => window.__price(k,o).sum", [k, o])
            if got != want: bad("расчёт", f"{k} {o}: ждал {want}, получил {got}")
    else:
        p_val = pg.evaluate("window.__price('small', {we:false, hours:2, guests:4, extras:[]}).sum")
        if not p_val or p_val <= 0: bad("расчёт", f"некорректный расчет цены: {p_val}")

    # 7. ссылки
    tels = pg.evaluate("[...document.querySelectorAll('a[href^=tel]')].map(a=>a.getAttribute('href'))")
    main_tel = tels[0] if tels else ""
    if not main_tel or any(t != main_tel for t in tels): bad("ссылки", f"tel-ссылки не согласованы: {set(tels)}")
    
    mail = pg.evaluate("[...document.querySelectorAll('a[href^=mailto]')].map(a=>a.getAttribute('href'))")
    if not mail or not mail[0].startswith("mailto:"): bad("ссылки", f"почта некорректна: {mail}")

    pol = pg.request.get(URL + "politika.html")
    if pol.status != 200: bad("ссылки", "politika.html не открывается")
    ctx.close()

    # ---- сценарии на компьютере мышкой ----
    ctx = br.new_context(viewport={"width": 1440, "height": 900}, locale="ru-RU")
    pg = ctx.new_page(); pg.goto(URL, wait_until="networkidle")
    # окно заявки по клику на свободное окно — посередине экрана, Esc закрывает
    pg.locator(".slot").first.click(); pg.wait_for_timeout(400)
    if not is_open(): bad("компьютер", "окно заявки не открылось по клику на свободное окно")
    box = pg.locator("#sheet").bounding_box()
    if box["x"] < 200 or box["y"] + box["height"] > 900 or box["y"] < 0: bad("компьютер", f"окно заявки не посередине или не помещается: {box}")
    if "Окно:" not in tg_text(): bad("компьютер", "в заявке из окна нет времени")
    pg.screenshot(path=f"{OUT}/desktop-sheet.png")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    if is_open(): bad("компьютер", "окно не закрылось клавишей Esc")
    # меню в шапке ведёт к разделу и подсвечивает его
    pg.locator('.topnav a[href="#price"]').click(); pg.wait_for_timeout(1500)
    top = pg.evaluate("document.getElementById('price').getBoundingClientRect().top")
    if not (40 <= top <= 140): bad("компьютер", f"после клика «Цены» раздел встал не под шапкой: top={top}")
    if "on" not in (pg.get_attribute('.topnav a[href="#price"]', "class") or ""): bad("компьютер", "пункт «Цены» в шапке не подсвечен")
    # миниатюра бани по клику становится главным фото
    pg.locator("#bath-small").scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    before = pg.inner_text("#bath-small .strip figure:first-child figcaption")
    pg.locator("#bath-small .strip figure:nth-child(2) .zoom").click(); pg.wait_for_timeout(300)
    after = pg.inner_text("#bath-small .strip figure:first-child figcaption")
    if before == after: bad("компьютер", "клик по миниатюре не сменил главное фото бани")
    # подбор: блок с суммой справа не уезжает при прокрутке вопросов
    pg.locator("#pickForm").scroll_into_view_if_needed(); pg.evaluate("scrollBy(0, 260)"); pg.wait_for_timeout(500)
    rb = pg.locator("#results").bounding_box(); qb = pg.locator("#pickForm .q").first.bounding_box()
    if rb["x"] < qb["x"] + qb["width"]: bad("компьютер", "результат подбора не справа от вопросов")
    if rb["y"] < 76 or rb["y"] > 200: bad("компьютер", f"результат подбора уехал при прокрутке: y={rb['y']}")
    pg.screenshot(path=f"{OUT}/desktop-pick.png")
    ctx.close(); br.close()

print("ПРОБЛЕМ:", len(problems))
for x in problems: print(" -", x)
