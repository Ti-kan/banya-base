#!/usr/bin/env python3
"""
Builds ~/banya-base/krasnoyarsk-50.html - Master Outreach Cockpit
and ~/banya-base/TUESDAY_50_KRASNOYARSK_OUTREACH.md for 50 Krasnoyarsk Wood-Fired Bathhouses.
Zero slop, zero hallucination, psychologically sound B2B templates.
"""

import json
import os
import re

DATA_PATH = "/Users/takanov/banya-base/baths-krasnoyarsk.json"
HTML_OUT_PATH = "/Users/takanov/banya-base/krasnoyarsk-50.html"
MD_OUT_PATH = "/Users/takanov/banya-base/TUESDAY_50_KRASNOYARSK_OUTREACH.md"

BATH_NAME_OVERRIDES = {
    'Баня (п. Солонцы, ул. Осенняя)': 'Баня в Солонцах',
    'Баня на дровах (ул. Побежимова)': 'Баня на дровах на Побежимова',
    'A-Frame_bathhouse': 'A-Frame Bathhouse',
    'Par house': 'Par House',
    'Баня-house': 'Баня-House',
    'Bazaiha river': 'Базаиха River',
    'Базаиха river': 'Базаиха River',
    'Family par': 'Family Par',
    'Joy in home': 'Joy In Home',
    'Green rancho': 'Green Rancho',
    'Грин холл': 'Грин Холл',
    'С Легким Паром': 'С Лёгким Паром',
    'Пар.ОК': 'Пар.ОК',
    'Hut House': 'Hut House',
    'Pillars': 'Pillars',
    'Breza': 'Breza',
    'Grelka': 'Grelka',
}

def clean_banya_name(b):
    raw_name = b.get('name', '').strip()
    if raw_name in BATH_NAME_OVERRIDES:
        return BATH_NAME_OVERRIDES[raw_name]
    name = raw_name.replace('_', ' ')
    name = re.sub(r'\[.*?\]', '', name)
    name = re.sub(r'\(.*?\)', '', name).strip()
    return name

def clean_banya_street(b):
    addr = b.get('address', '').strip()
    slug = b.get('slug', '')
    
    if slug == 'banya-solontsy':
        return 'в Солонцах, ул. Осенняя'
    
    raw = addr
    raw = re.sub(r'^Красноярский край,\s*', '', raw)
    raw = re.sub(r'^городской округ Красноярск,\s*', '', raw)
    raw = re.sub(r'^Красноярск,\s*', '', raw)
    raw = re.sub(r'^Емельяновский район,\s*', '', raw)
    raw = re.sub(r'^Емельяновский муниципальный округ,\s*', '', raw)
    raw = re.sub(r'^городское поселение Емельяново,\s*', '', raw)
    raw = re.sub(r'^городской округ Дивногорск,\s*', '', raw)
    
    if 'Дрокино' in raw:
        return 'в Дрокино, ул. Садовая, 33'
    if 'Кузнецово' in raw or 'Таежная' in raw or 'Таёжная' in raw:
        return 'в Кузнецово, Таёжная ул., 4'
    if 'Нанжуль' in raw:
        return 'в Солонцах, мкр. Нанжуль, 10А'
    if 'Калина' in raw:
        return 'в Солонцах, СНТ Калина, 97'
    if 'Солонцы' in raw and 'Сосновая' in raw:
        return 'в Солонцах, Сосновая ул., 21'
    if 'Солонцы' in raw and 'Осенняя' in raw:
        return 'в Солонцах, ул. Осенняя'
    if 'Манский' in raw:
        if 'Весёлый' in raw:
            return 'в посёлке Манский, Весёлый пер., 1а'
        return 'в посёлке Манский'
    if 'Сосновоборск' in raw or 'Сосновоборская' in raw:
        return 'в Сосновоборске, Сосновоборская ул., 36'
    if 'Минино' in raw:
        return 'в Минино, Восточная ул., 1'
    if 'Бугачево' in raw:
        return 'в Бугачево, Молодёжная ул., 9'
    if 'Сухая Балка' in raw:
        return 'в Сухой Балке, Ландмания, 1'
    if 'Емельяново' in raw and 'Придорожная' in raw:
        return 'в Емельяново, Придорожная ул., 2'
    if 'Шафран-2' in raw:
        return 'в СНТ «Шафран-2», Солнечная ул., 1'
    if 'Александрия' in raw:
        return 'в КП «Александрия», Орлиная ул., 22'
    if 'Дивный бор' in raw or 'Дивный Бор' in raw:
        return 'в Дивном Бору'
    if 'Тихий Бор' in raw:
        return 'в ДНТ «Тихий Бор», 12'
    if 'Лесная Поляна' in raw:
        return 'в СНТ «Лесная Поляна», 79'
    if 'Здоровье' in raw:
        return 'в СО «Здоровье», 2'
    if 'Алюминий' in raw:
        return 'в СНТ «Алюминий», Мичуринская ул., 183'
    if 'Демьяна Бедного' in raw:
        return 'на ул. Демьяна Бедного, 6'
    if 'Елены Стасовой' in raw:
        return 'на ул. Елены Стасовой, 54ж'
    if 'Курагинская' in raw:
        return 'на Курагинской, 241'
    if '4-я Линейная' in raw:
        return 'на 4-й Линейной, 62'
    if 'Базайская' in raw:
        num = re.search(r'(\d+[А-Яа-яA-Za-z]?)', raw)
        return f'на Базайской, {num.group(1)}' if num else 'на Базайской'
    if 'Первая улица' in raw:
        return 'на Первой улице, 405'
    if 'Хантайская' in raw:
        num = re.search(r'(\d+[А-Яа-яA-Za-z]?)', raw)
        return f'на Хантайской, {num.group(1)}' if num else 'на Хантайской'
    if 'Вольный проезд' in raw:
        return 'в Вольном проезде, 15А'
    if 'Лазурный берег' in raw:
        return 'на ул. Лазурный берег, 33'
    if 'Центральная' in raw:
        return 'на Центральной, 154'
    if 'Монтажников' in raw:
        return 'на ул. Монтажников, 57/30'
    if 'Весны' in raw:
        return 'на ул. Весны, 2а'
    if 'Сибирская' in raw:
        return 'на Сибирской, 19'
    if 'Гармония' in raw:
        return 'на ул. Гармония, 155'
    if 'Подъёмная' in raw:
        return 'на Подъёмной, 12а'
    if 'Побежимова' in raw:
        return 'на ул. Побежимова, 4'
    if '1-я Приручейная' in raw:
        return 'на 1-й Приручейной, 39а'
    if 'Западная' in raw:
        return 'на Западной, 11'
    if 'Соколовская' in raw:
        return 'на Соколовской, 21'
    if 'Металлургов' in raw:
        return 'на просп. Металлургов, 2г'
    if 'Садовая' in raw:
        return 'на ул. Садовой, 7а'
    if 'Качинская' in raw:
        return 'на Качинской, 60Б'
    if 'Ястынская' in raw:
        return 'на ул. Ястынской, 44в'
    if 'Рейдовая' in raw:
        return 'на Рейдовой, 45/4'
    if 'Ручейная' in raw:
        return 'на ул. Ручейной, 748'

    clean = raw.strip()
    if not (clean.startswith('на ') or clean.startswith('в ')):
        clean = 'на ' + clean
    clean = clean.replace(' (', ', ').replace('(', '').replace(')', '')
    return clean

def build_banya_messages(b):
    name_clean = clean_banya_name(b)
    street_short = clean_banya_street(b)
    slug = b['slug']
    pwd = b.get('price_wd', 2000)
    pwd_fmt = f"{pwd:,}".replace(",", " ")
    chan = b.get('chan', 0)
    
    if chan > 0:
        chan_fmt = f"{chan:,}".replace(",", " ")
        chan_info = f"с горячим чаном за {chan_fmt} ₽"
    else:
        chan_info = "с тёплой купелью"
        
    url = f"https://ti-kan.github.io/banya-base/b/{slug}/"
    
    # Template 1: [ 💬 Шаг 1: Короткий пробив на собственника (без ссылки) ]
    msg1 = (
        f"Здравствуйте! Подскажите, здесь можно связаться с собственником или управляющим комплекса «{name_clean}» ({street_short})?\n\n"
        f"Вопрос не по рекламе — мы с командой собрали специально под вашу баню один цифровой подарок (интерактивный сайт с калькулятором на компанию), хочу просто бесплатно передать ссылку напрямую. Скину сюда посмотреть?"
    )
    
    # Template 2: [ 🎁 Шаг 2 / Основной заход: Сайт БЕСПЛАТНО в подарок + Оффер на ИИ-сохранение и дожим лидов ]
    msg2 = (
        f"Приветствую! Меня зовут Кирилл. Мы занимаемся системами сохранения клиентов и автоматизацией бронирования для банных комплексов.\n\n"
        f"Чтобы познакомиться делом, а не словами — мы за выходные БЕСПЛАТНО собрали персонально для «{name_clean}» ({street_short}) готовый современный сайт с расчётом на компанию:\n"
        f"👉 {url}\n\n"
        f"Откройте прямо с телефона: там уже стоят ваши реальные условия (от {pwd_fmt} ₽/час {chan_info}), табло свободных окон и калькулятор, который сам делит сумму на каждого человека и даёт кнопку «Скинуть готовый расчёт друзьям в Telegram».\n\n"
        f"Сам сайт мы отдаём вам полностью бесплатно — за него ничего платить не нужно, можете хоть сегодня поставить эту ссылку в 2ГИС, Яндекс.Карты и соцсети.\n\n"
        f"А наш основной профиль — мы подключаем к мессенджерам бани автоматическую систему поиска, сохранения и дожима заявок. Когда гость спрашивает про занятую субботу или уходит «посоветоваться с друзьями по цене», система не даёт ему потеряться: автоматически сохраняет контакт в вашу базу, сама предлагает свободные окна и доводит компанию до брони.\n\n"
        f"Посмотрите сайт с телефона — всё ли точно указали по вашим ценам? Если нравится, передам вам все доступы и коротко покажу, как работает авто-сохранение всех входящих гостей!"
    )
    
    # Template 3: [ 🤖 Шаг 3: Дожим после просмотра сайта (Переход к продаже ИИ-автоматизации) ]
    msg3 = (
        f"Удалось глянуть ваш сайт с телефона? ({url})\n\n"
        f"Если нужно поправить какие-то цифры по часам или купели — напишите, мы бесплатно подправим за 5 минут, чтобы вы могли сразу закрепить ссылку в 2ГИС и Яндекс.Картах.\n\n"
        f"И заодно скажите: у вас сейчас заявки из WhatsApp, Telegram и звонков собираются автоматически в единую базу с авто-дожимом тех, кто не забронировал сразу, или администраторы ведут переписки вручную? Могу на вашем примере показать, как возвращать до 30% «ушедших подумать» компаний."
    )
    
    return {
        'name_clean': name_clean,
        'street_short': street_short,
        'pwd_formatted': pwd_fmt,
        'chan_info': chan_info,
        'url': url,
        'msg1': msg1,
        'msg2': msg2,
        'msg3': msg3
    }

HTML_TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>50 Банных комплексов Красноярска — Outreach Cockpit & Вторник-Рассылка</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230B0C0E'/%3E%3Cpath d='M8 23h16M10 23V14l6-5 6 5v9' stroke='%23cc3d0b' stroke-width='2.6' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E">
<style>
@font-face{font-family:"Oswald";src:url("fonts/oswald.woff2") format("woff2");font-weight:600 700;font-display:swap}
@font-face{font-family:"Onest";src:url("fonts/onest.woff2") format("woff2");font-weight:400 500 600 700;font-display:swap}
:root{
  --night:#0B0C0E;
  --night-2:#14161C;
  --night-3:#1C1F28;
  --night-line:rgba(255,255,255,0.09);
  --night-muted:#8E94A3;

  --accent:#cc3d0b;
  --accent-hover:#b3350a;
  --accent-on-dark:#ff7a4d;
  --accent-glow:rgba(204,61,11,0.28);

  --champagne:#eab308;
  --champagne-soft:rgba(234,179,8,0.12);

  --green:#10b981;
  --green-soft:rgba(16,185,129,0.14);
  --tg:#229ed9;
  --wa:#25d366;

  --display:"Oswald","Arial Narrow","Roboto Condensed",sans-serif;
  --sans:"Onest",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  --r:18px;
}
*{box-sizing:border-box}
body{margin:0;background:var(--night);color:#FAF9F6;font:15px/1.5 var(--sans);-webkit-font-smoothing:antialiased;padding:28px 16px 80px}
.wrap{max-width:1320px;margin:0 auto}
a{color:inherit;text-decoration:none}

.hero-box{background:linear-gradient(135deg,rgba(204,61,11,.16) 0%,rgba(234,179,8,.05) 100%),var(--night-2);border:1px solid var(--night-line);border-radius:var(--r);padding:28px 32px;margin-bottom:28px}
h1{font:700 clamp(26px,3.5vw,40px)/1.15 var(--display);text-transform:uppercase;letter-spacing:-.01em;margin:0 0 10px;color:#fff}
.lead{font-size:15px;color:var(--night-muted);max-width:80ch;line-height:1.55;margin-bottom:20px}

/* Live Outreach Counters */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:22px}
.stat{background:rgba(255,255,255,.03);border:1px solid var(--night-line);border-radius:14px;padding:14px 16px;transition:border-color .2s}
.stat:hover{border-color:rgba(255,255,255,.2)}
.stat-val{font:700 28px/1 var(--display);color:#fff}
.stat-val.accent{color:var(--accent-on-dark)}
.stat-val.green{color:var(--green)}
.stat-val.champagne{color:var(--champagne)}
.stat-lbl{font-size:12px;color:var(--night-muted);margin-top:6px;text-transform:uppercase;letter-spacing:.04em;font-weight:600}

/* Base URL Configuration */
.base-url-bar{background:rgba(0,0,0,.5);border:1px solid var(--night-line);border-radius:12px;padding:12px 16px;margin-bottom:22px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.base-url-bar label{font-size:12px;font-weight:700;color:var(--accent-on-dark);text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
.base-url-input{flex:1;min-width:280px;height:38px;border-radius:8px;border:1px solid var(--night-line);background:var(--night-3);color:#fff;padding:0 12px;font:600 13px var(--sans);outline:0}
.base-url-input:focus{border-color:var(--accent)}

/* Filter tabs & Search */
.controls{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:24px;align-items:center;justify-content:space-between}
.filter-tabs{display:flex;flex-wrap:wrap;gap:8px}
.tab{min-height:38px;padding:0 15px;border-radius:999px;border:1px solid var(--night-line);background:var(--night-2);color:var(--night-muted);font:600 13px/1 var(--sans);cursor:pointer;transition:all .15s}
.tab:hover{color:#fff;border-color:var(--accent)}
.tab.on{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 4px 16px var(--accent-glow)}

.search-wrap{position:relative;flex:1;max-width:360px;min-width:240px}
.search-input{width:100%;height:38px;border-radius:999px;border:1px solid var(--night-line);background:var(--night-2);color:#fff;padding:0 16px 0 38px;font:500 13px var(--sans);outline:0}
.search-input:focus{border-color:var(--accent)}
.search-icon{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:15px;height:15px;color:#6b7280;pointer-events:none}

/* Grid of Cards */
.grid{display:grid;grid-template-columns:1fr;gap:20px}
@media (min-width:768px){.grid{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1200px){.grid{grid-template-columns:repeat(3,1fr)}}

.card{background:var(--night-2);border:1px solid var(--night-line);border-radius:var(--r);padding:20px;display:flex;flex-direction:column;transition:all .2s;position:relative}
.card:hover{border-color:rgba(204,61,11,.4);box-shadow:0 12px 32px rgba(0,0,0,.4)}
.card.status-step1{border-color:rgba(234,179,8,.4)}
.card.status-site{border-color:rgba(204,61,11,.6)}
.card.status-replied{border-color:rgba(16,185,129,.7);box-shadow:0 8px 24px rgba(16,185,129,.12)}

.card-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.rank{font:700 13px/1 var(--display);color:var(--night-muted);letter-spacing:.02em}
.badge{font-size:11px;font-weight:700;padding:4px 9px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em}
.badge-great{background:rgba(16,185,129,.14);color:#10b981;border:1px solid rgba(16,185,129,.35)}
.badge-warn{background:rgba(234,179,8,.14);color:#eab308;border:1px solid rgba(234,179,8,.35)}
.badge-crit{background:rgba(204,61,11,.16);color:var(--accent-on-dark);border:1px solid rgba(204,61,11,.4)}

.name{font:700 20px/1.2 var(--display);text-transform:uppercase;color:#fff;margin-bottom:4px}
.addr{font-size:13px;color:#d1d5db;margin-bottom:6px;line-height:1.4}
.phone{font-size:13px;font-weight:600;color:var(--accent-on-dark);margin-bottom:12px;display:inline-flex;align-items:center;gap:6px}

.meta-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-top:1px solid var(--night-line);border-bottom:1px solid var(--night-line);margin-bottom:12px;font-size:12px}
.rating{color:#eab308;font-weight:600}
.price{color:#fff;font-weight:700}

/* Actions Row: Site Link & Copy URL */
.site-actions{display:grid;grid-template-columns:1fr auto;gap:8px;margin-bottom:14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:38px;padding:0 12px;border-radius:8px;font:600 12px/1 var(--sans);cursor:pointer;transition:all .15s;border:0;text-align:center}
.btn-open{background:rgba(255,255,255,.07);color:#FAF9F6;border:1px solid rgba(255,255,255,.14)}
.btn-open:hover{background:rgba(255,255,255,.14);color:#fff}
.btn-copy-url{background:rgba(255,255,255,.04);color:var(--night-muted);border:1px solid var(--night-line);padding:0 10px}
.btn-copy-url:hover{color:#fff;border-color:rgba(255,255,255,.25)}

/* Outreach Box & Editable Textarea */
.outreach-box{background:rgba(0,0,0,.35);border:1px solid var(--night-line);border-radius:12px;padding:12px;margin-top:auto}
.tpl-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-bottom:10px}
.tpl-tab{background:var(--night-3);color:var(--night-muted);border:1px solid var(--night-line);border-radius:6px;padding:6px 4px;font:600 11px/1.2 var(--sans);cursor:pointer;text-align:center;transition:all .15s}
.tpl-tab:hover{color:#fff;border-color:var(--accent)}
.tpl-tab.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 2px 8px var(--accent-glow)}

.msg-textarea{width:100%;height:130px;background:var(--night-3);border:1px solid var(--night-line);border-radius:8px;color:#f3f4f6;font:12px/1.45 var(--sans);padding:8px 10px;resize:vertical;outline:0;box-sizing:border-box;margin-bottom:10px;transition:border-color .15s}
.msg-textarea:focus{border-color:var(--accent)}

.send-actions{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:12px}
.btn-copy-msg{background:rgba(255,255,255,.08);color:#FAF9F6;border:1px solid rgba(255,255,255,.15);font-size:11px;padding:0 6px}
.btn-copy-msg:hover{background:rgba(255,255,255,.16);color:#fff}
.btn-wa{background:rgba(37,211,102,.14);color:#25d366;border:1px solid rgba(37,211,102,.35);font-size:11px;padding:0 6px}
.btn-wa:hover{background:#25d366;color:#000}
.btn-tg{background:rgba(34,158,217,.14);color:#229ed9;border:1px solid rgba(34,158,217,.35);font-size:11px;padding:0 6px}
.btn-tg:hover{background:#229ed9;color:#fff}

/* Persistent CRM Checkboxes */
.crm-row{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding-top:10px;border-top:1px solid var(--night-line)}
.crm-label{display:flex;align-items:center;gap:6px;cursor:pointer;font-size:11px;color:var(--night-muted);font-weight:600;user-select:none}
.crm-label input{accent-color:var(--accent);cursor:pointer;width:14px;height:14px;margin:0}
.crm-label:hover{color:#fff}

.toast{position:fixed;bottom:24px;right:24px;background:#fff;color:var(--night);padding:12px 20px;border-radius:999px;font:700 13px/1 var(--sans);z-index:99;box-shadow:0 12px 30px rgba(0,0,0,.5);opacity:0;transform:translateY(20px);pointer-events:none;transition:all .25s}
.toast.show{opacity:1;transform:translateY(0)}
</style>
</head>
<body>
<div class="wrap">
  
  <div class="hero-box">
    <h1>50 Банных комплексов Красноярска — Outreach Cockpit</h1>
    <p class="lead">
      Персонализированная рассылка на вторник: проверенные B2B-шаблоны без спам-блокировок.
      В карточке каждой бани доступен предпросмотр любого из 3 вариантов, редактируемый текст перед отправкой и сохранение статуса в <code>localStorage</code>.
    </p>

    <!-- Outreach Progress Stats -->
    <div class="stats">
      <div class="stat">
        <div class="stat-val" id="statTotal">50</div>
        <div class="stat-lbl">Всего комплексов</div>
      </div>
      <div class="stat">
        <div class="stat-val champagne" id="statStep1">0 / 50</div>
        <div class="stat-lbl">Шаг 1: Контакт</div>
      </div>
      <div class="stat">
        <div class="stat-val accent" id="statSite">0 / 50</div>
        <div class="stat-lbl">Шаг 2: Отправлен сайт</div>
      </div>
      <div class="stat">
        <div class="stat-val green" id="statReplied">0 / 50</div>
        <div class="stat-lbl">Ответили на диалог</div>
      </div>
    </div>

    <div class="base-url-bar">
      <label for="baseUrlInput">🌐 Live Base URL:</label>
      <input class="base-url-input" id="baseUrlInput" type="text" value="https://ti-kan.github.io/banya-base">
      <span style="font-size:11px;color:var(--night-muted)">Ссылки в сообщениях синхронизируются автоматически</span>
    </div>

    <div class="controls">
      <div class="filter-tabs" id="filterTabs">
        <button class="tab on" type="button" data-filter="all">Все 50</button>
        <button class="tab" type="button" data-filter="unprocessed">⏳ Не начато</button>
        <button class="tab" type="button" data-filter="step1">💬 Шаг 1 отправлен</button>
        <button class="tab" type="button" data-filter="site">🚀 Сайт отправлен</button>
        <button class="tab" type="button" data-filter="replied">✅ Ответили</button>
      </div>

      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" id="searchInput" type="search" placeholder="Поиск по бане, улице, телефону...">
      </div>
    </div>
  </div>

  <div class="grid" id="bathsGrid">
    <!-- Rendered dynamically -->
  </div>
</div>

<div class="toast" id="toast">📋 Скопировано в буфер обмена!</div>

<script>
window.BATHS_DATA = __DATA_PLACEHOLDER__;

(function(){
  var grid = document.getElementById("bathsGrid");
  var toast = document.getElementById("toast");
  var baseInput = document.getElementById("baseUrlInput");
  var allData = window.BATHS_DATA || [];
  var activeFilter = "all";

  function showToast(text){
    if(text) toast.textContent = text;
    toast.classList.add("show");
    setTimeout(function(){ toast.classList.remove("show"); }, 2200);
  }

  function copyToClipboard(val, msg){
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(val).then(function(){ showToast(msg || "📋 Скопировано!"); });
    } else {
      var t = document.createElement("textarea"); t.value = val; document.body.appendChild(t); t.select();
      try{ document.execCommand("copy"); showToast(msg || "📋 Скопировано!"); }catch(e){}
      document.body.removeChild(t);
    }
  }

  function getCrm(slug){
    try {
      var raw = localStorage.getItem("banya_crm_" + slug);
      return raw ? JSON.parse(raw) : { step1: false, site: false, replied: false };
    } catch(e) {
      return { step1: false, site: false, replied: false };
    }
  }

  function saveCrm(slug, data){
    try {
      localStorage.setItem("banya_crm_" + slug, JSON.stringify(data));
    } catch(e){}
    updateStats();
  }

  function updateStats(){
    var step1Count = 0;
    var siteCount = 0;
    var repliedCount = 0;

    allData.forEach(function(b){
      var crm = getCrm(b.slug);
      if(crm.step1) step1Count++;
      if(crm.site) siteCount++;
      if(crm.replied) repliedCount++;
    });

    document.getElementById("statTotal").textContent = allData.length;
    document.getElementById("statStep1").textContent = step1Count + " / " + allData.length;
    document.getElementById("statSite").textContent = siteCount + " / " + allData.length;
    document.getElementById("statReplied").textContent = repliedCount + " / " + allData.length;
  }

  function render(list){
    var base = (baseInput.value || "https://ti-kan.github.io/banya-base").trim().replace(/\\/+$/, "");

    grid.innerHTML = list.map(function(b){
      var staticUrl = base + "/b/" + b.slug + "/";
      var badgeClass = b.grade === "Отлично" ? "badge-great" : (b.grade === "Хорошо" ? "badge-warn" : "badge-crit");
      var badgeLabel = b.grade + " · " + b.reply_time;
      var chanStr = b.chan > 0 ? (b.chan.toLocaleString('ru-RU') + " ₽") : "купель";

      var crm = getCrm(b.slug);
      var cardStatusClass = crm.replied ? "status-replied" : (crm.site ? "status-site" : (crm.step1 ? "status-step1" : ""));

      // Clean messenger targets
      var waPhone = (b.whatsapp || "").replace(/\\D/g, "");
      if(waPhone.length === 11 && waPhone.startsWith("8")) waPhone = "7" + waPhone.slice(1);
      
      var tgHandle = (b.telegram || "").replace(/^@/, "");

      return '<div class="card ' + cardStatusClass + '" id="card-' + b.slug + '" data-slug="' + b.slug + '">' +
        '<div class="card-top">' +
          '<span class="rank">#' + b.id + ' · ' + b.slug + '</span>' +
          '<span class="badge ' + badgeClass + '">' + badgeLabel + '</span>' +
        '</div>' +
        '<div class="name">' + b.name_clean + '</div>' +
        '<div class="addr">📍 ' + b.street_short + '</div>' +
        '<a class="phone" href="tel:' + b.phone_digits + '">📞 ' + b.phone_display + '</a>' +
        '<div class="meta-row">' +
          '<span class="rating">★ ' + b.rating_2gis + ' (' + b.reviews_2gis + ' отз.)</span>' +
          '<span class="price">Час: ' + b.pwd_formatted + ' ₽ · ' + chanStr + '</span>' +
        '</div>' +
        '<div class="site-actions">' +
          '<a class="btn btn-open" href="' + staticUrl + '" target="_blank">↗ Открыть сайт</a>' +
          '<button class="btn btn-copy-url" type="button" data-url="' + staticUrl + '">🔗 Ссылка</button>' +
        '</div>' +
        '<div class="outreach-box">' +
          '<div class="tpl-tabs" data-slug="' + b.slug + '">' +
            '<button class="tpl-tab active" type="button" data-tpl="1">💬 Шаг 1: Пробив</button>' +
            '<button class="tpl-tab" type="button" data-tpl="2">🎁 Шаг 2: Подарок + ИИ</button>' +
            '<button class="tpl-tab" type="button" data-tpl="3">🤖 Шаг 3: Дожим ИИ</button>' +
          '</div>' +
          '<textarea class="msg-textarea" id="txt-' + b.slug + '" rows="7">' + b.msg1 + '</textarea>' +
          '<div class="send-actions">' +
            '<button class="btn btn-copy-msg" type="button" data-copy-for="' + b.slug + '">📋 Копировать</button>' +
            '<button class="btn btn-wa" type="button" data-wa-for="' + b.slug + '" data-wa-phone="' + waPhone + '">💬 WhatsApp</button>' +
            '<button class="btn btn-tg" type="button" data-tg-for="' + b.slug + '" data-tg-target="' + tgHandle + '">✈️ Telegram</button>' +
          '</div>' +
          '<div class="crm-row">' +
            '<label class="crm-label"><input type="checkbox" data-crm-type="step1" data-slug="' + b.slug + '" ' + (crm.step1 ? "checked" : "") + '> Шаг 1</label>' +
            '<label class="crm-label"><input type="checkbox" data-crm-type="site" data-slug="' + b.slug + '" ' + (crm.site ? "checked" : "") + '> Сайт</label>' +
            '<label class="crm-label"><input type="checkbox" data-crm-type="replied" data-slug="' + b.slug + '" ' + (crm.replied ? "checked" : "") + '> Ответили</label>' +
          '</div>' +
        '</div>' +
      '</div>';
    }).join("");

    attachCardHandlers();
    updateStats();
  }

  function attachCardHandlers(){
    // Copy URL
    grid.querySelectorAll("[data-url]").forEach(function(btn){
      btn.addEventListener("click", function(){
        copyToClipboard(btn.getAttribute("data-url"), "🔗 Ссылка на сайт скопирована!");
      });
    });

    // Template Switcher Tabs
    grid.querySelectorAll(".tpl-tab").forEach(function(tab){
      tab.addEventListener("click", function(){
        var tplNum = tab.getAttribute("data-tpl");
        var slug = tab.parentElement.getAttribute("data-slug");
        var item = allData.find(function(x){ return x.slug === slug; });
        if(!item) return;

        tab.parentElement.querySelectorAll(".tpl-tab").forEach(function(t){ t.classList.remove("active"); });
        tab.classList.add("active");

        var txtArea = document.getElementById("txt-" + slug);
        if(!txtArea) return;

        var base = (baseInput.value || "https://ti-kan.github.io/banya-base").trim().replace(/\\/+$/, "");
        var currentUrl = base + "/b/" + slug + "/";

        var text = "";
        if(tplNum === "1") text = item.msg1;
        else if(tplNum === "2") text = item.msg2.replace(/https:\/\/ti-kan\.github\.io\/banya-base\/b\/[^\/]+\//, currentUrl);
        else if(tplNum === "3") text = item.msg3.replace(/https:\/\/ti-kan\.github\.io\/banya-base\/b\/[^\/]+\//, currentUrl);

        txtArea.value = text;
      });
    });

    // Copy Textarea Content
    grid.querySelectorAll("[data-copy-for]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var slug = btn.getAttribute("data-copy-for");
        var txtArea = document.getElementById("txt-" + slug);
        if(txtArea){
          copyToClipboard(txtArea.value, "💬 Текст сообщения скопирован!");
        }
      });
    });

    // Open WhatsApp
    grid.querySelectorAll("[data-wa-for]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var slug = btn.getAttribute("data-wa-for");
        var phone = btn.getAttribute("data-wa-phone");
        var txtArea = document.getElementById("txt-" + slug);
        var text = txtArea ? txtArea.value : "";
        var link = "https://wa.me/" + phone + "?text=" + encodeURIComponent(text);
        window.open(link, "_blank");
      });
    });

    // Open Telegram
    grid.querySelectorAll("[data-tg-for]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var slug = btn.getAttribute("data-tg-for");
        var target = btn.getAttribute("data-tg-target");
        var txtArea = document.getElementById("txt-" + slug);
        var text = txtArea ? txtArea.value : "";
        var link = "";
        if(target.match(/^\\+?\\d+$/)){
          var num = target.replace(/^\\+/, "");
          link = "https://t.me/+" + num + "?text=" + encodeURIComponent(text);
        } else {
          link = "https://t.me/" + target + "?text=" + encodeURIComponent(text);
        }
        window.open(link, "_blank");
      });
    });

    // CRM Checkboxes
    grid.querySelectorAll(".crm-label input").forEach(function(chk){
      chk.addEventListener("change", function(){
        var slug = chk.getAttribute("data-slug");
        var type = chk.getAttribute("data-crm-type");
        var crm = getCrm(slug);
        crm[type] = chk.checked;
        saveCrm(slug, crm);

        var card = document.getElementById("card-" + slug);
        if(card){
          card.classList.remove("status-step1", "status-site", "status-replied");
          if(crm.replied) card.classList.add("status-replied");
          else if(crm.site) card.classList.add("status-site");
          else if(crm.step1) card.classList.add("status-step1");
        }
      });
    });
  }

  function filterAndSearch(){
    var q = (document.getElementById("searchInput").value || "").toLowerCase().trim();
    var filtered = allData.filter(function(b){
      var crm = getCrm(b.slug);

      if(activeFilter === "unprocessed" && (crm.step1 || crm.site || crm.replied)) return false;
      if(activeFilter === "step1" && !crm.step1) return false;
      if(activeFilter === "site" && !crm.site) return false;
      if(activeFilter === "replied" && !crm.replied) return false;

      if(q){
        var match = b.name_clean.toLowerCase().includes(q) ||
                    b.street_short.toLowerCase().includes(q) ||
                    b.slug.toLowerCase().includes(q) ||
                    (b.phone_display && b.phone_display.includes(q));
        if(!match) return false;
      }
      return true;
    });
    render(filtered);
  }

  // Initial render
  render(allData);

  document.querySelectorAll("#filterTabs .tab").forEach(function(t){
    t.addEventListener("click", function(){
      document.querySelectorAll("#filterTabs .tab").forEach(function(x){ x.classList.remove("on"); });
      t.classList.add("on");
      activeFilter = t.getAttribute("data-filter");
      filterAndSearch();
    });
  });

  var sInput = document.getElementById("searchInput");
  if(sInput) sInput.addEventListener("input", filterAndSearch);

  if(baseInput){
    baseInput.addEventListener("input", function(){
      filterAndSearch();
    });
  }
})();
</script>
</body>
</html>
"""

def generate_markdown_cheat_sheet(baths):
    lines = [
        "# ВТОРНИК: 50 БАННЫХ КОМПЛЕКСОВ КРАСНОЯРСКА — OUTREACH CHEAT-SHEET",
        "",
        "> **Инструкция по рассылке во вторник:**",
        "> 1. **Шаг 1 (Утро / Холодный контакт)**: отправляем короткий вход **без ссылок**, чтобы не ловить спам-блок от WhatsApp/Telegram.",
        "> 2. **Шаг 2 (После ответа / Владение)**: как только ответили или подтвердили контакт — отправляем ссылку на персональный сайт с калькулятором на компанию.",
        "> 3. **Вариант 3 (Короткий)**: для быстрых карточек в 2ГИС, Яндекс.Картах или соцсетях.",
        "",
        "## СВОДНАЯ ТАБЛИЦА (50 КОМПЛЕКСОВ)",
        "",
        "| № | Название | Адрес | Телефон | WhatsApp | Готовый сайт |",
        "|---|---|---|---|---|---|"
    ]
    
    for b in baths:
        wa_phone = re.sub(r'\D', '', b.get('whatsapp', ''))
        if len(wa_phone) == 11 and wa_phone.startswith('8'):
            wa_phone = '7' + wa_phone[1:]
        wa_link = f"https://wa.me/{wa_phone}" if wa_phone else "—"
        url = f"https://ti-kan.github.io/banya-base/b/{b['slug']}/"
        lines.append(f"| {b['id']} | **{b['name_clean']}** | {b['street_short']} | `{b.get('phone_display', '')}` | [Написать]({wa_link}) | [{b['slug']}]({url}) |")
        
    lines.append("\n---\n")
    lines.append("## ПЕРСОНАЛЬНЫЕ СООБЩЕНИЯ ДЛЯ КАЖДОЙ БАНИ\n")
    
    for b in baths:
        lines.append(f"### #{b['id']} · {b['name_clean']} ({b['slug']})")
        lines.append(f"- **Локация:** {b['street_short']}")
        lines.append(f"- **Телефон:** `{b.get('phone_display', '')}`")
        lines.append(f"- **Сайт:** [{b['url']}]({b['url']})")
        
        wa_phone = re.sub(r'\D', '', b.get('whatsapp', ''))
        if len(wa_phone) == 11 and wa_phone.startswith('8'):
            wa_phone = '7' + wa_phone[1:]
        if wa_phone:
            lines.append(f"- **WhatsApp:** https://wa.me/{wa_phone}")
        if b.get('telegram'):
            tg = b['telegram'].replace('@', '')
            lines.append(f"- **Telegram:** https://t.me/{tg}")
            
        lines.append("\n**[ 💬 Шаг 1: Короткий пробив на собственника (без ссылки) ]:**")
        lines.append("```text")
        lines.append(b['msg1'])
        lines.append("```")
        
        lines.append("\n**[ 🎁 Шаг 2 / Основной заход: Сайт БЕСПЛАТНО в подарок + Оффер на ИИ-сохранение и дожим лидов ]:**")
        lines.append("```text")
        lines.append(b['msg2'])
        lines.append("```")
        
        lines.append("\n**[ 🤖 Шаг 3: Дожим после просмотра сайта (Переход к продаже ИИ-автоматизации) ]:**")
        lines.append("```text")
        lines.append(b['msg3'])
        lines.append("```")
        lines.append("\n---\n")
        
    return "\n".join(lines)

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        baths = json.load(f)
        
    print(f"Loaded {len(baths)} baths from {DATA_PATH}")
    
    for b in baths:
        info = build_banya_messages(b)
        b.update(info)
        
    # Write enriched baths-krasnoyarsk.json
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(baths, f, ensure_ascii=False, indent=2)
    print(f"Saved enriched data back to {DATA_PATH}")
    
    # Generate HTML Cockpit
    html_content = HTML_TEMPLATE.replace("__DATA_PLACEHOLDER__", json.dumps(baths, ensure_ascii=False))
    with open(HTML_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved master cockpit to {HTML_OUT_PATH}")
    
    # Generate Markdown Cheat Sheet
    md_content = generate_markdown_cheat_sheet(baths)
    with open(MD_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved master cheat sheet to {MD_OUT_PATH}")

if __name__ == "__main__":
    main()
