import base64, pathlib, re, sys
sp = pathlib.Path(__file__).resolve().parent
site = sp.parent
ALTS = {
 "logo":"Логотип «Мёдбург»: красный драккар под парусом на крафтовой бумаге",
 "kr-mindal":"Миндальный крендель с сахарной пудрой",
 "kr-mak":"Маковый крендель",
 "kr-shokolad":"Плетёный шоколадный крендель",
 "kr-oreh":"Крендель с дроблёным арахисом",
 "kr-sol":"Крендель с солью и тмином",
 "kr-kroshka":"Крендель с корицей",
 "b-goryachiy":"Стакан горячего «Бушприта» с клюквой и брусникой",
 "b-butylka":"Бутылка «Бушприта» с ягодами и можжевельником",
 "b-kombo":"Крендель и стакан «Бушприта» рядом",
 "lim-1":"Лимонады: малина с лесными ягодами и яблоко с лаймом",
 "lim-2":"Лимонады: мёд-имбирь-лимон и сочный арбуз",
 "lim-3":"Лимонады: яблоко-лайм и клубника-апельсин",
 "lim-4":"Лимонады: блю-кюрасао с апельсином и малина с лесными ягодами",
 "kupechesky-banner":"Крендель «Купеческий» — богатый состав",
 "nakleyka":"Наклейка «Мёдбург, Крепостная, 5» с драккаром",
 "ph-fasad":"Вход в «Мёдбург»: деревянная вывеска и двери с резными кренделями",
 "ph-dver":"Дверь «Мёдбурга» с вывеской и указателем городов у входа",
 "ph-interier":"Зал «Мёдбурга»: кирпичная стена, витрина с кренделями и тёплые лампы",
 "ph-krendel-zamok":"Два кренделя в руках на фоне Выборгского замка",
 "ph-bashnya":"Часовая башня Выборга",
 "ph-zamok":"Выборгский замок и башня Святого Олафа",
 "ph-panorama":"Панорама старого Выборга с высоты",
}
tpl = (sp/"comic.tpl.html").read_text(encoding="utf-8")
def repl(m):
    k = m.group(1)
    d = base64.b64encode((sp/"c"/f"{k}.jpg").read_bytes()).decode()
    return f'<img src="data:image/jpeg;base64,{d}" alt="{ALTS[k]}" loading="lazy" decoding="async">'
body, n = re.subn(r"@@([^@]+)@@", repl, tpl)
assert "@@" not in body
(sp/"medburg.html").write_text(body, encoding="utf-8")

HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="«Мёдбург» — семейная крендельная у Часовой башни в Выборге, Крепостная, 5. Крендели, фирменный горячий «Бушприт» на клюкве и бруснике, лимонады. Вт—Вс, 12:00—18:00.">
<meta name="theme-color" content="#A82C1C">
<link rel="canonical" href="https://www.medburgvyborg.ru/">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/favicon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Мёдбург">
<meta property="og:url" content="https://www.medburgvyborg.ru/">
<meta property="og:title" content="Мёдбург — крендельная у Часовой башни">
<meta property="og:description" content="Семейная крендельная в Выборге, Крепостная, 5. Крендели, «Бушприт», лимонады. Вт—Вс, 12:00—18:00.">
<meta property="og:image" content="https://www.medburgvyborg.ru/preview.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="800">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://www.medburgvyborg.ru/preview.jpg">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Bakery",
  "name": "Мёдбург",
  "alternateName": "МёдБург — крендельная у Часовой башни",
  "description": "Семейная крендельная у Часовой башни в Выборге. Крендели, фирменный горячий «Бушприт» на клюкве и бруснике, лимонады.",
  "url": "https://www.medburgvyborg.ru/",
  "image": "https://www.medburgvyborg.ru/preview.jpg",
  "logo": "https://www.medburgvyborg.ru/favicon.png",
  "foundingDate": "2024",
  "servesCuisine": "Выпечка",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Крепостная улица, 5",
    "addressLocality": "Выборг",
    "addressRegion": "Ленинградская область",
    "addressCountry": "RU"
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "12:00",
    "closes": "18:00"
  }],
  "sameAs": [
    "https://vk.com/medburg_vyborg",
    "https://yandex.ru/maps/org/20716977311/",
    "https://go.2gis.com/FaU65"
  ]
}
</script>
<style>html{-webkit-text-size-adjust:100%}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
'''
lines = body.split("\n"); head_part = []; rest = []
for i, ln in enumerate(lines):
    if ln.startswith("<title>") or ln.startswith('<link rel="preconnect"') or ln.startswith('<link rel="stylesheet"'):
        head_part.append(ln)
    else:
        rest = lines[i:]; break
site.mkdir(parents=True, exist_ok=True)
doc = HEAD + "\n".join(head_part) + "\n</head>\n<body>\n" + "\n".join(rest) + "\n</body>\n</html>\n"
(site/"index.html").write_text(doc, encoding="utf-8")
print(f"картинок: {n} · артефакт {round(len(body.encode())/1024/1024,2)} МБ · index.html {round(len(doc.encode())/1024/1024,2)} МБ")

(site/"robots.txt").write_text(
    "User-agent: *\nAllow: /\nDisallow: /src/\n\nSitemap: https://www.medburgvyborg.ru/sitemap.xml\n", encoding="utf-8")
(site/"sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url>\n'
    '    <loc>https://www.medburgvyborg.ru/</loc>\n'
    '    <lastmod>2026-09-09</lastmod>\n'
    '    <changefreq>monthly</changefreq>\n'
    '    <priority>1.0</priority>\n'
    '  </url>\n'
    '</urlset>\n', encoding="utf-8")
print("robots.txt и sitemap.xml записаны")
