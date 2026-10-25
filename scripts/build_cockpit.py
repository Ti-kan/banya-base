#!/usr/bin/env python3
"""
Builds ~/banya-base/krasnoyarsk-50.html - Master Outreach Cockpit
for 50 Krasnoyarsk Wood-Fired Bathhouses
"""

import json
import os

OUT_PATH = "/Users/takanov/banya-base/krasnoyarsk-50.html"

HTML_CONTENT = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>50 Банных комплексов Красноярска — Outreach Cockpit & Готовые сайты для отправки</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230B0C0E'/%3E%3Cpath d='M8 23h16M10 23V14l6-5 6 5v9' stroke='%23cc3d0b' stroke-width='2.6' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E">
<style>
@font-face{font-family:"Oswald";src:url("fonts/oswald.woff2") format("woff2");font-weight:600 700;font-display:swap}
@font-face{font-family:"Onest";src:url("fonts/onest.woff2") format("woff2");font-weight:400 700;font-display:swap}
:root{
  --night:#0B0C0E;
  --night-2:#14161C;
  --night-3:#1C1F28;
  --night-line:rgba(255,255,255,0.09);
  --night-muted:#8E94A3;

  --accent:#cc3d0b;
  --accent-hover:#b3350a;
  --accent-on-dark:#ff7a4d;
  --accent-glow:rgba(204,61,11,0.3);

  --champagne:#eab308;
  --champagne-soft:rgba(234,179,8,0.12);

  --green:#10b981;
  --tg:#229ed9;
  --wa:#25d366;

  --display:"Oswald","Arial Narrow","Roboto Condensed",sans-serif;
  --sans:"Onest",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  --r:20px;
}
*{box-sizing:border-box}
body{margin:0;background:var(--night);color:#fff;font:15px/1.5 var(--sans);-webkit-font-smoothing:antialiased;padding:32px 16px 80px}
.wrap{max-width:1280px;margin:0 auto}
a{color:inherit;text-decoration:none}

.hero-box{background:linear-gradient(135deg,rgba(204,61,11,.16) 0%,rgba(234,179,8,.06) 100%),var(--night-2);border:1px solid var(--night-line);border-radius:var(--r);padding:32px;margin-bottom:32px}
h1{font:700 clamp(28px,3.8vw,44px)/1.1 var(--display);text-transform:uppercase;letter-spacing:-.01em;margin:0 0 12px;color:#fff}
.lead{font-size:16px;color:var(--night-muted);max-width:74ch;line-height:1.55;margin-bottom:24px}

.base-url-bar{background:rgba(0,0,0,.45);border:1px solid var(--night-line);border-radius:14px;padding:14px 18px;margin-bottom:24px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.base-url-bar label{font-size:13px;font-weight:700;color:var(--accent-on-dark);text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
.base-url-input{flex:1;min-width:280px;height:42px;border-radius:8px;border:1px solid var(--night-line);background:var(--night-3);color:#fff;padding:0 14px;font:600 14px var(--sans);outline:0}
.base-url-input:focus{border-color:var(--accent)}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:24px}
.stat{background:rgba(255,255,255,.03);border:1px solid var(--night-line);border-radius:14px;padding:16px}
.stat-val{font:700 28px/1 var(--display);color:var(--accent-on-dark)}
.stat-lbl{font-size:13px;color:var(--night-muted);margin-top:4px}

.controls{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:24px;align-items:center;justify-content:space-between}
.tabs{display:flex;flex-wrap:wrap;gap:8px}
.tab{min-height:44px;padding:0 16px;border-radius:999px;border:1px solid var(--night-line);background:var(--night-2);color:var(--night-muted);font:600 13px/1 var(--sans);cursor:pointer;transition:all .15s}
.tab:hover{color:#fff;border-color:var(--accent)}
.tab.on{background:var(--accent);color:#fff;border-color:var(--accent)}

.search-wrap{position:relative;flex:1;max-width:380px;min-width:260px}
.search-input{width:100%;height:44px;border-radius:999px;border:1px solid var(--night-line);background:var(--night-2);color:#fff;padding:0 18px 0 42px;font:500 14px var(--sans);outline:0}
.search-input:focus{border-color:var(--accent)}
.search-icon{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:16px;height:16px;color:#6b7280}

.grid{display:grid;grid-template-columns:1fr;gap:20px}
@media (min-width:768px){.grid{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1140px){.grid{grid-template-columns:repeat(3,1fr)}}

.card{background:var(--night-2);border:1px solid var(--night-line);border-radius:var(--r);padding:22px;display:flex;flex-direction:column;transition:all .2s;position:relative}
.card:hover{border-color:var(--accent);transform:translateY(-3px);box-shadow:0 14px 36px rgba(204,61,11,.15)}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}
.rank{font:700 15px/1 var(--display);color:var(--night-muted)}
.badge{font-size:11px;font-weight:700;padding:4px 10px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em}
.badge-great{background:rgba(16,185,129,.15);color:#10b981;border:1px solid rgba(16,185,129,.35)}
.badge-warn{background:rgba(234,179,8,.15);color:#eab308;border:1px solid rgba(234,179,8,.35)}
.badge-crit{background:rgba(204,61,11,.18);color:var(--accent-on-dark);border:1px solid rgba(204,61,11,.4)}

.name{font:700 22px/1.2 var(--display);text-transform:uppercase;color:#fff;margin-bottom:4px}
.addr{font-size:13px;color:var(--night-muted);margin-bottom:6px}
.phone{font-size:13px;font-weight:600;color:#e5e7eb;margin-bottom:12px;display:flex;align-items:center;gap:6px}

.flaw{background:rgba(204,61,11,.08);border-left:3px solid var(--accent);padding:10px 12px;border-radius:0 8px 8px 0;font-size:12px;color:#fca5a5;line-height:1.45;margin-bottom:12px}
.quote{background:rgba(255,255,255,.03);border-left:3px solid #6b7280;padding:8px 12px;border-radius:0 8px 8px 0;font-size:12px;color:#d1d5db;line-height:1.45;margin-bottom:14px;font-style:italic}

.meta-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-top:1px solid var(--night-line);border-bottom:1px solid var(--night-line);margin-bottom:14px;font-size:13px}
.rating{color:#eab308;font-weight:600}
.price{color:#fff;font-weight:700}

/* Action buttons */
.acts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:44px;padding:0 12px;border-radius:10px;font:600 13px/1 var(--sans);cursor:pointer;transition:all .15s;border:0;text-align:center}
.btn-open{background:var(--accent);color:#fff}
.btn-open:hover{background:var(--accent-hover)}
.btn-copy{background:rgba(255,255,255,.06);color:#fff;border:1px solid var(--night-line)}
.btn-copy:hover{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.25)}

/* Outreach copy buttons */
.outreach-box{background:rgba(0,0,0,.35);border:1px solid var(--night-line);border-radius:12px;padding:12px;margin-top:auto}
.outreach-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--night-muted);margin-bottom:8px}
.outreach-btns{display:flex;flex-direction:column;gap:6px}
.btn-msg{background:rgba(255,255,255,.04);color:#d1d5db;border:1px solid var(--night-line);min-height:38px;font-size:12px;justify-content:flex-start;padding:0 10px;border-radius:8px;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.btn-msg:hover{background:rgba(204,61,11,.15);border-color:var(--accent);color:#fff}

.messengers{display:flex;gap:6px;margin-top:8px}
.btn-wa{background:rgba(37,211,102,.12);color:#25d366;border:1px solid rgba(37,211,102,.3);flex:1;min-height:38px;font-size:12px}
.btn-wa:hover{background:#25d366;color:#000}
.btn-tg{background:rgba(34,158,217,.12);color:#229ed9;border:1px solid rgba(34,158,217,.3);flex:1;min-height:38px;font-size:12px}
.btn-tg:hover{background:#229ed9;color:#fff}

.toast{position:fixed;bottom:24px;right:24px;background:#fff;color:var(--night);padding:14px 22px;border-radius:999px;font:700 14px/1 var(--sans);z-index:99;box-shadow:0 12px 30px rgba(0,0,0,.5);opacity:0;transform:translateY(20px);pointer-events:none;transition:all .25s}
.toast.show{opacity:1;transform:translateY(0)}
</style>
</head>
<body>
<div class="wrap">
  
  <div class="hero-box">
    <h1>50 Банных комплексов Красноярска — Outreach Cockpit</h1>
    <p class="lead">
      Для каждой из 50 бань сгенерирован индивидуальный сайт на статическом роуте <code>/b/&lt;slug&gt;/</code>.
      Реальные цены, часы, купели из стенограмм тайного аудита, интерактивный расчёт с делением стоимости на человека и 2-рядный marquee реальных отзывов. В 1 клик открывайте переписку в WhatsApp или Telegram с готовым персональным предложением.
    </p>

    <div class="base-url-bar">
      <label for="baseUrlInput">🌐 Live Base URL сайта:</label>
      <input class="base-url-input" id="baseUrlInput" type="text" value="https://ti-kan.github.io/banya-base">
      <span style="font-size:12px;color:var(--night-muted)">Все ссылки и тексты обновляются на лету!</span>
    </div>

    <div class="stats">
      <div class="stat">
        <div class="stat-val" id="statTotal">50</div>
        <div class="stat-lbl">Отобранных бань на дровах</div>
      </div>
      <div class="stat">
        <div class="stat-val" style="color:var(--accent-on-dark)" id="statFlaws">12</div>
        <div class="stat-lbl">Грейд: Хорошо и Удовл.</div>
      </div>
      <div class="stat">
        <div class="stat-val" style="color:#eab308" id="statSlow">24</div>
        <div class="stat-lbl">Долгий ответ / без дожима</div>
      </div>
      <div class="stat">
        <div class="stat-val" style="color:#10b981">49</div>
        <div class="stat-lbl">С чаном и купелью</div>
      </div>
    </div>

    <div class="controls">
      <div class="tabs" id="filterTabs">
        <button class="tab on" type="button" data-filter="all">Все 50 бань</button>
        <button class="tab" type="button" data-filter="flaws">🔥 Грейд: Хорошо и Удовл. (12)</button>
        <button class="tab" type="button" data-filter="slow">⚡ Долгий ответ > 30 мин (24)</button>
        <button class="tab" type="button" data-filter="chan">🌲 С чаном и купелью (49)</button>
      </div>

      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" id="searchInput" type="search" placeholder="Поиск по названию или улице...">
      </div>
    </div>
  </div>

  <div class="grid" id="bathsGrid">
    <!-- Loaded dynamically from baths-krasnoyarsk.json -->
  </div>
</div>

<div class="toast" id="toast">📋 Скопировано в буфер обмена!</div>

<script>
(function(){
  var grid = document.getElementById("bathsGrid");
  var toast = document.getElementById("toast");
  var baseInput = document.getElementById("baseUrlInput");
  var allData = [];
  var activeFilter = "all";

  // Permanent 24/7 Production URL default
  var initialBase = "https://ti-kan.github.io/banya-base";
  baseInput.value = initialBase;

  function showToast(text){
    if(text) toast.textContent = text;
    toast.classList.add("show");
    setTimeout(function(){ toast.classList.remove("show"); }, 2400);
  }

  function copyText(val, msg){
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(val).then(function(){ showToast(msg || "📋 Скопировано в буфер обмена!"); });
    } else {
      var t = document.createElement("textarea"); t.value = val; document.body.appendChild(t); t.select();
      try{ document.execCommand("copy"); showToast(msg || "📋 Скопировано в буфер обмена!"); }catch(e){}
      document.body.removeChild(t);
    }
  }

  function render(list){
    var base = (baseInput.value || window.location.origin || "").replace(/\\/+$/, "");

    grid.innerHTML = list.map(function(b){
      var staticUrl = base + "/b/" + b.slug + "/";
      
      var badgeClass = b.grade === "Отлично" ? "badge-great" : (b.grade === "Хорошо" ? "badge-warn" : "badge-crit");
      var badgeLabel = b.grade + " · " + b.reply_time;

      var chanStr = b.chan > 0 ? (b.chan.toLocaleString('ru-RU') + " ₽") : "включён";
      var quoteText = b.transcript_quote ? ('«' + b.transcript_quote + '»') : "Стенограмма переписки сохранена в аудите";

      // 3 Tailored Psychological Outreach Messages
      var msgDirect = "Здравствуйте, руководство «" + b.name + "»! Мы провели тайный аудит обработки входящих обращений среди 197 бань Красноярска. В тесте вы ответили за " + b.reply_time + ", назвали от " + b.price_wd.toLocaleString('ru-RU') + " ₽/час и купель " + chanStr + ", но клиент ушёл согласовывать с компанией и не вернулся. Специально для вас мы собрали готовый конверсионный сайт: " + staticUrl + " , где гости за 20 секунд рассчитывают полный чек визита (с делением суммы поровну на каждого человека) и отправляют готовую заявку вам в Telegram или WhatsApp. Посмотрите с телефона — готовы передать его вашей бане на тест.";
      
      var msgStep1 = "Здравствуйте! На прошлой неделе мы провели тайный аудит скорости ответа и конверсии среди 197 бань и саун Красноярска. «" + b.name + "» вошла в наш итоговый рейтинг топ-50. Мы составили сравнительную таблицу: сколько броней теряется из-за долгого подсчёта сметы компанией и как онлайн-расчёт на человека решает эту проблему. Можем прислать строчку вашей бани из аудита и 2-минутный разбор?";
      
      var msgStep2 = "Записали короткий разбор: главная причина потери лидов в банях Красноярска — сложность согласования цены в компании («я спрошу у ребят и напишу»). На вашем готовом персональном сайте " + staticUrl + " встроен мгновенный расчёт на человека и 1-клик кнопка «Скинуть смету компании в Telegram». Это закрывает до 40% сомневающихся компаний прямо в мессенджере.";

      var waPhone = b.whatsapp.replace(/\\D/g, "");
      if(waPhone.length === 11 && waPhone.startsWith("8")) waPhone = "7" + waPhone.slice(1);
      var waLink = "https://wa.me/" + waPhone + "?text=" + encodeURIComponent(msgDirect);
      
      var tgHandle = b.telegram.replace(/^@/, "");
      var tgLink = tgHandle.startsWith("+") ? ("https://t.me/" + tgHandle + "?text=" + encodeURIComponent(msgDirect)) : ("https://t.me/" + tgHandle);

      return '<div class="card">' +
        '<div class="card-top">' +
          '<span class="rank">#' + b.id + ' · ' + b.slug + '</span>' +
          '<span class="badge ' + badgeClass + '">' + badgeLabel + '</span>' +
        '</div>' +
        '<div class="name">' + b.name + '</div>' +
        '<div class="addr">📍 ' + b.address + '</div>' +
        '<div class="phone">📞 ' + b.phone_display + '</div>' +
        '<div class="flaw">⚠️ <b>Косяк аудита:</b> ' + b.flaw + '</div>' +
        '<div class="quote">' + quoteText + '</div>' +
        '<div class="meta-row">' +
          '<span class="rating">★ ' + b.rating_2gis + ' (' + b.reviews_2gis + ' отз.)</span>' +
          '<span class="price">Час: ' + b.price_wd.toLocaleString('ru-RU') + ' ₽ · Чан: ' + chanStr + '</span>' +
        '</div>' +
        '<div class="acts">' +
          '<a class="btn btn-open" href="' + staticUrl + '" target="_blank">Открыть сайт ↗</a>' +
          '<button class="btn btn-copy" type="button" data-copy-url="' + staticUrl + '">Копировать URL</button>' +
        '</div>' +
        '<div class="outreach-box">' +
          '<div class="outreach-title">Психологические сообщения (в 1 клик):</div>' +
          '<div class="outreach-btns">' +
            '<button class="btn btn-msg" type="button" data-copy-msg="' + encodeURIComponent(msgDirect) + '" title="' + msgDirect + '">1. Прямой оффер: «Подготовили сайт...»</button>' +
            '<button class="btn btn-msg" type="button" data-copy-msg="' + encodeURIComponent(msgStep1) + '" title="' + msgStep1 + '">2. Шаг 1 (Интрига): «Таблица 197 бань...»</button>' +
            '<button class="btn btn-msg" type="button" data-copy-msg="' + encodeURIComponent(msgStep2) + '" title="' + msgStep2 + '">3. Шаг 2 (Разбор): «Разбор + ссылка...»</button>' +
          '</div>' +
          '<div class="messengers">' +
            '<a class="btn btn-wa" href="' + waLink + '" target="_blank" rel="noopener">WhatsApp</a>' +
            '<a class="btn btn-tg" href="' + tgLink + '" target="_blank" rel="noopener">Telegram</a>' +
          '</div>' +
        '</div>' +
      '</div>';
    }).join("");

    grid.querySelectorAll("[data-copy-url]").forEach(function(b){
      b.addEventListener("click", function(){
        copyText(b.getAttribute("data-copy-url"), "🔗 Ссылка на персональный сайт бани скопирована!");
      });
    });

    grid.querySelectorAll("[data-copy-msg]").forEach(function(b){
      b.addEventListener("click", function(){
        var text = decodeURIComponent(b.getAttribute("data-copy-msg"));
        copyText(text, "💬 Текст оффера скопирован! Готов к отправке в мессенджер");
      });
    });
  }

  function filterAndSearch(){
    var q = (document.getElementById("searchInput").value || "").toLowerCase().trim();
    var filtered = allData.filter(function(b){
      if(activeFilter === "flaws" && b.grade === "Отлично") return false;
      if(activeFilter === "slow"){
        var rt = b.reply_time.toLowerCase();
        var isSlow = rt.includes("игнор") || rt.includes("час") || rt.includes("дн");
        var m = rt.match(/\\d+/);
        if(m && parseInt(m[0]) >= 20) isSlow = true;
        if(b.flaw.toLowerCase().includes("дожим") || b.flaw.toLowerCase().includes("медлен")) isSlow = true;
        if(!isSlow) return false;
      }
      if(activeFilter === "chan" && b.chan <= 0) return false;

      if(q){
        var match = b.name.toLowerCase().includes(q) ||
                    b.address.toLowerCase().includes(q) ||
                    b.slug.toLowerCase().includes(q) ||
                    b.flaw.toLowerCase().includes(q) ||
                    (b.transcript_quote && b.transcript_quote.toLowerCase().includes(q));
        if(!match) return false;
      }
      return true;
    });
    render(filtered);
  }

  fetch("/baths-krasnoyarsk.json")
    .then(function(r){ return r.json(); })
    .then(function(d){
      allData = d;
      render(allData);
    })
    .catch(function(e){ console.error(e); });

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

  baseInput.addEventListener("input", function(){
    filterAndSearch();
  });
})();
</script>
</body>
</html>
"""

def main():
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote master outreach cockpit to {OUT_PATH}")

if __name__ == "__main__":
    main()
