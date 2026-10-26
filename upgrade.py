"""Post-process dist: mobile upgrade markup, GEO/SEO tags, breadcrumbs, sitemap lastmod. Safe to run repeatedly."""
from pathlib import Path
from datetime import date
import json, re, shutil

BASE=Path(__file__).parent
CFG=json.loads((BASE/'site_config.json').read_text(encoding='utf-8'))
ORIGIN=CFG['canonical_origin'].rstrip('/')
root=BASE/'dist'
shutil.copyfile(BASE/'upgrade.css',root/'upgrade.css')

# Seferihisar town centre (approximate); replace with the Google Business Profile pin when available.
LAT,LON=CFG.get('geo',[38.1967,26.8389])
MAPS='https://www.google.com/maps/search/?api=1&query=H%C4%B1d%C4%B1rl%C4%B1k+Mahallesi+70+Sokak+No%3A5+Seferihisar+%C4%B0zmir'
# Locative forms follow Turkish vowel harmony and are not derivable mechanically from the slug.
locative={'camikebir':'Camikebir’de','hidirlik':'Hıdırlık’ta','turabiye':'Turabiye’de','colak-ibrahim-bey':'Çolak İbrahim Bey’de','tepecik':'Tepecik’te','sigacik':'Sığacık’ta','akarca':'Akarca’da','ulamis':'Ulamış’ta'}
PHONE_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 3h4l2 5-3 2a14 14 0 0 0 6 6l2-3 5 2v4c0 2-2 3-4 2C9 19 5 15 3 7 2 5 3 3 5 3Z"/></svg>'
WA_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a9 9 0 0 1-13.3 7.9L3 21l1.6-4.7A9 9 0 1 1 21 11.5Z"/><path d="M8 7c0 5 2 7 7 8l1-2-3-1-1 1-2-2 1-1-1-3Z"/></svg>'

for path in root.rglob('index.html'):
 s=path.read_text(encoding='utf-8')
 slug=path.parent.name if path.parent!=root else ''
 url=ORIGIN+(f'/bolgeler/{slug}/' if slug else '/')
 if '/upgrade.css' not in s:
  s=s.replace('<link rel="stylesheet" href="/mobile.css">','<link rel="stylesheet" href="/mobile.css"><link rel="stylesheet" href="/upgrade.css">')
 # Mobile hides intro <br>s; keep a space so sentences do not run together.
 s=re.sub(r'<p class="intro">.*?</p>',lambda m:re.sub(r'(?<! )<br>',' <br>',m[0]),s)
 if 'geo.region' not in s:
  s=s.replace('<link rel="canonical"',f'<meta name="geo.region" content="TR-35"><meta name="geo.placename" content="Seferihisar, İzmir"><meta name="geo.position" content="{LAT};{LON}"><meta name="ICBM" content="{LAT}, {LON}"><link rel="canonical"',1)
 if 'og:site_name' not in s:
  s=s.replace('<meta property="og:locale"',f'<meta property="og:site_name" content="{CFG["name"]}"><meta property="og:locale"',1)
  s=s.replace(f'<meta property="og:image" content="{ORIGIN}/assets/social.png">',f'<meta property="og:image" content="{ORIGIN}/assets/social.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{CFG["name"]} · {CFG["display_phone"]}">',1)
 def ld(m):
  data=json.loads(m[1])
  for node in data['@graph']:
   if node['@type']=='LocalBusiness':
    node['geo']={'@type':'GeoCoordinates','latitude':LAT,'longitude':LON}
    node['hasMap']=MAPS
    node['priceRange']='Taksimetre'
  return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
 s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',ld,s)
 # Hero buttons get icons, like the dock.
 s=re.sub(r'(<a class="button yellow" href="tel:[^"]+">)Taksi çağır',lambda m:m[1]+PHONE_SVG+'Taksi çağır',s,count=1)
 s=re.sub(r'(<a class="button outline"[^>]*>)WhatsApp',lambda m:m[1]+WA_SVG+'WhatsApp',s,count=1)
 s=re.sub(r'(<div class="hero-copy">)<p class="eyebrow">.*?</p>',r'\1',s,count=1)
 # Repeat the call banner directly under the header; the original stays below the hero.
 if 'top-banner' not in s:
  banner=re.search(r'<div class="call-banner">.*?</div>',s)[0]
  s=s.replace('</header>','</header>'+banner.replace('class="call-banner"','class="call-banner top-banner"'),1)
 # Below the hero, the marina photo banner replaces the GIF.
 if 'marina-banner' not in s:
  marina=f'<div class="call-banner marina-banner"><a href="tel:{CFG["telephone"]}" aria-label="Seferihisar’da taksi çağırmak için arayın: {CFG["display_phone"]}"><img src="/assets/banner-marina-800.webp" srcset="/assets/banner-marina-800.webp 800w, /assets/banner-marina.webp 1600w" sizes="(max-width:960px) 100vw, 900px" width="1600" height="667" alt="Seferihisar Taksi 7/24 · gece marina ışıkları önünde sarı taksi · {CFG["display_phone"]}" loading="lazy" decoding="async"></a></div>'
  s=re.sub(r'<div class="call-banner">.*?</div>',lambda _:marina,s,count=1)
 if slug:
  title=re.search(r'<title>(.*?) Taksi \|',s)[1]
  s=re.sub(r'<h1>.*?</h1>',f'<h1>{locative[slug]}<br><em>taksi mi lazım?</em></h1>',s,count=1)
  if 'class="crumbs"' not in s:
   s=s.replace('<main id="icerik">',f'<main id="icerik"><div class="crumbs" role="navigation" aria-label="Sayfa yolu"><ol><li><a href="/">Seferihisar Taksi</a></li><li><a href="/#bolgeler">Bölgeler</a></li><li><span aria-current="page">{title} Taksi</span></li></ol></div>',1)
  s=s.replace(f'<a href="/bolgeler/{slug}/"><span>',f'<a href="/bolgeler/{slug}/" aria-current="page"><span>')
 path.write_text(s,encoding='utf-8')

sm=root/'sitemap.xml'
today=date.today().isoformat()
sm.write_text(re.sub(r'</loc>(<lastmod>[^<]*</lastmod>)?',f'</loc><lastmod>{today}</lastmod>',sm.read_text(encoding='utf-8')),encoding='utf-8')
