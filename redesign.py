"""Build: python redesign.py (includes legacy generator and brand assets)."""
from pathlib import Path
from urllib.parse import quote
import runpy, json, re

BASE=Path(__file__).parent
CFG=json.loads((BASE/'site_config.json').read_text(encoding='utf-8'))
ORIGIN=CFG['canonical_origin'].rstrip('/')
NAME=CFG['name']
PHONE=CFG['telephone']
DISPLAY=CFG['display_phone']
WA='https://wa.me/'+CFG['whatsapp']
HELLO=WA+'?text='+quote('Merhaba, Seferihisar’da taksi talep etmek istiyorum.')
root=BASE/'dist'
runpy.run_path(str(BASE/'build_base.py'))
runpy.run_path(str(BASE/'make_assets.py'))
areas=[('camikebir','Camikebir'),('hidirlik','Hıdırlık'),('turabiye','Turabiye'),('colak-ibrahim-bey','Çolak İbrahim Bey'),('tepecik','Tepecik'),('sigacik','Sığacık'),('akarca','Akarca'),('ulamis','Ulamış')]
localcopy={
 'camikebir':('Merkezde bir sonraki durak.','Camikebir’deki yolculuğunuz için sokak adınızı ve bina numaranızı paylaşın. Merkezdeki alışveriş, ziyaret veya günlük işlerinize giderken alınacağınız noktayı telefonda netleştirebilirsiniz.','Merkez içindeki buluşmalarda sokak adıyla birlikte yakındaki belirgin bir noktayı iletmek, adresin anlaşılmasını kolaylaştırır.'),
 'hidirlik':('Bizim mahalleden, sizin rotanıza.','İşletme adresimiz Hıdırlık Mahallesi, 70 Sokak No:5, Seferihisar / İzmir. Hıdırlık’tan merkeze ya da başka bir adrese gitmek için bizi arayabilir, WhatsApp üzerinden konumunuzu paylaşabilirsiniz.','Adresimize gelmek isterseniz yol tarifi bağlantısını kullanın. Araç uygunluğunu gelmeden önce telefonla sorabilirsiniz.'),
 'turabiye':('Günlük hayatın yol arkadaşı.','Turabiye Mahallesi’nden yolculuğunuz için hareket noktanızı, gideceğiniz adresi ve yolcu sayısını paylaşın. Merkeze gidişinizi ya da dönüşünüzü görüşerek planlayın.','Apartman girişi veya sokak üzerindeki uygun bir buluşma noktasını belirtin; dönüş yolculuğunuz varsa saati ayrıca paylaşın.'),
 'colak-ibrahim-bey':('Mahallenizden yeni bir güne.','Çolak İbrahim Bey Mahallesi’nde taksi talebiniz için açık adresinizi telefonla veya WhatsApp ile iletin. Merkez, sahil ya da farklı bir varış noktası için güzergâhı birlikte netleştirin.','Mahalle adıyla birlikte sokak ve kapı numarasını yazın. Bagaj veya araç kapasitesiyle ilgili ihtiyacınızı görüşme sırasında belirtin.'),
 'tepecik':('Rotanız neresi olursa.','Tepecik’ten Seferihisar merkeze veya çevre mahallelere ulaşım talebinizi bize iletebilirsiniz. Yolculuk öncesinde alınış adresini, saati ve varış noktasını görüşün.','Ara sokaklarda kolay bulunabilecek bir buluşma noktası paylaşın. İleri tarihli yolculuklar için tarih ve saat bilgisini birlikte gönderin.'),
 'sigacik':('Sahile uzanan bir yolculuk.','Sığacık’a giderken veya Sığacık’tan dönerken buluşma yerinizi ve varış adresinizi paylaşın. Sahil çevresindeki planınız için araç uygunluğunu telefonla öğrenin.','Kalabalık zamanlarda erişilebilir bir buluşma noktası seçin. Dönüş planınızı önceden iletmeniz, talebin görüşülmesini kolaylaştırır.'),
 'akarca':('Denize doğru, eve doğru.','Akarca sahilinden Seferihisar merkeze ya da merkezden Akarca’ya yolculuk için bizi arayın. Alınacağınız adresi veya konum bağlantınızı WhatsApp üzerinden paylaşabilirsiniz.','Sahil boyunca benzer adresler olabileceği için konum ve yakınınızdaki bir işletme veya sokak adını birlikte gönderebilirsiniz.'),
 'ulamis':('Yolun başında buluşalım.','Ulamış’tan Seferihisar’a veya farklı bir adrese yapacağınız yolculuk için hareket saatinizi ve buluşma noktanızı iletin. Araç ve saat uygunluğu görüşme sırasında netleşir.','Mahalle içindeki adresinizi açık şekilde yazın. Yolcu ve bagaj sayısını, özellikle havalimanı yolculuklarında, önceden paylaşın.')}

for path in root.rglob('index.html'):
 s=path.read_text(encoding='utf-8')
 slug=path.parent.name if path.parent!=root else ''
 area=dict(areas).get(slug)
 s=s.replace('Seferihisar Taksi',NAME)
 title=f'{area} Taksi | {NAME}' if area else f'{NAME} | {DISPLAY}'
 desc=f'{area} taksi için {DISPLAY}. {NAME}: konum paylaşımı, merkeze ve çevre mahallelere yolculuk talebi.' if area else f'Seferihisar taksi için {DISPLAY}. Seferihisar’da taksi çağırın; merkez, Hıdırlık, Sığacık ve Akarca için arayın veya WhatsApp’tan konum gönderin.'
 s=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',s)
 s=re.sub(r'(<meta name="description" content=")[^"]*',lambda m:m[1]+desc,s)
 s=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m[1]+title,s)
 s=re.sub(r'(<meta property="og:description" content=")[^"]*',lambda m:m[1]+desc,s)
 s=s.replace('https://seferihisar-taksi-merkez.rubysage32.chatgpt.site',ORIGIN)
 s=s.replace('/social.svg','/assets/social.png').replace('content="summary"','content="summary_large_image"').replace('content="#f4c844"','content="#09131c"')
 s=s.replace('href="/icon.svg"','href="/assets/logo-mark.svg"')
 s=s.replace('<link rel="stylesheet" href="/style.css">','<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/experience.css">')
 data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s).group(1))
 data['@graph']=[n for n in data['@graph'] if n['@type']!='FAQPage']
 for node in data['@graph']:
  if node['@type']=='WebPage':node['name']=title;node['description']=desc
 business={'@type':'LocalBusiness','@id':ORIGIN+'/#isletme','name':NAME,'alternateName':'Seferihisar Taxi 7/24','url':ORIGIN+'/','telephone':PHONE,'logo':ORIGIN+'/assets/logo-mark.svg','image':ORIGIN+'/assets/social.png','address':{'@type':'PostalAddress','streetAddress':'Hıdırlık Mahallesi, 70 Sokak No:5','addressLocality':'Seferihisar','addressRegion':'İzmir','addressCountry':'TR'},'openingHoursSpecification':{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],'opens':'00:00','closes':'23:59'},'areaServed':[{'@type':'Place','name':n} for _,n in areas]}
 data['@graph'] += [business,{'@type':'TaxiService','name':f'{area or "Seferihisar"} Taksi','provider':{'@id':ORIGIN+'/#isletme'},'areaServed':{'@type':'Place','name':area or 'Seferihisar, İzmir'},'availableChannel':{'@type':'ServiceChannel','servicePhone':{'@type':'ContactPoint','telephone':PHONE,'contactType':'customer service','availableLanguage':'Turkish'}}}]
 s=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda _: '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>',s)
 s=s.replace('<body>','<body><div class="scroll-progress" aria-hidden="true"></div>')
 s=re.sub(r'<span class="brandicon">.*?</span></span>', '<img class="brandmark" src="/assets/logo-mark.svg" width="46" height="46" alt="">',s)
 s=s.replace('<b>TAKSİ</b>','<b>TAKSİ <i>7/24</i></b>')
 s=s.replace('Bize ulaşın <span>↗</span>', 'Hemen ara <span>↗</span>').replace('class="button dark headercta" href="#iletisim"','class="button dark headercta" href="tel:'+PHONE+'"')
 banner=f'''<div class="call-banner"><a href="tel:{PHONE}" aria-label="Seferihisar’da taksi çağırmak için tıklayınız. {DISPLAY}"><picture><source media="(prefers-reduced-motion: reduce)" srcset="/assets/taksi-cagir.png"><img src="/assets/taksi-cagir.gif" width="960" height="180" alt="Seferihisar’da taksi çağırmak için tıklayınız · {DISPLAY}" fetchpriority="high"></picture></a></div>'''
 banner=banner.replace('/assets/taksi-cagir.png','/assets/banner-premium-still.png').replace('/assets/taksi-cagir.gif','/assets/banner-premium.gif').replace('width="960" height="180"','width="1280" height="280"')
 s=s.replace('</header>','</header>'+banner)
 hero=f'{area}.<br><em>Yola çıkalım.</em>' if area else 'Şehir sakin.<br><em>Senin yolun açık.</em>'
 s=re.sub(r'<h1>.*?</h1>',f'<h1>{hero}</h1>',s)
 s=s.replace('SEFERİHİSAR MERKEZ ODAKLI TAKSİ','SEFERİHİSAR TAKSİ 7/24')
 s=re.sub(r'<p class="intro">.*?</p>','<p class="intro">Seferihisar’da taksi, bir telefon uzağında.<br>Merkezden sahile, gün doğumundan geceye.<br>Bir sonraki yolculuğunuz burada başlıyor.</p>',s)
 s=re.sub(r'<div class="hero-actions">.*?</div>',f'<div class="hero-actions"><a class="button yellow" href="tel:{PHONE}">Taksi çağır <span>↗</span></a><a class="button outline" href="{HELLO}" target="_blank" rel="noopener noreferrer">WhatsApp’tan yaz <span>↗</span></a></div>',s)
 s=s.replace('Merkez. Mahalleler. Yeni rotalar.','YEREL ROTALAR. YENİ HİKÂYELER.')
 s=s.replace('<div class="hero-art"','<div class="hero-art"')
 s=s.replace('<div class="sun">','<div class="scene-orbit orbit-one"></div><div class="scene-orbit orbit-two"></div><span class="scene-word" aria-hidden="true">TAXI</span><div class="sun">')
 s=s.replace('Seferihisar kıyı yolunda sarı taksi illüstrasyonu','Gece sahil yolunda sarı taksiyi gösteren stilize sahne')
 s=s.replace('YAVAŞ ŞEHİR.<br><b>AKICI YOLCULUK.</b>','EGE’NİN RİTMİNDE.<br><b>SENİN ROTANDA.</b>')
 s=s.replace('Güzel yollar burada başlar.','GECE. GÜNDÜZ. HER GÜN.')
 s=re.sub(r'<svg class="taxi".*?</svg>','<img class="taxi" src="/assets/taxi.svg" width="800" height="390" alt="" aria-hidden="true">',s)
 s=s.replace('Gününüzün rotasına<br>uyum sağlayalım.','Bir şehir.<br><em>Birçok güzel rota.</em>')
 s=s.replace('HER YOLUN BİR BAŞLANGICI VAR','01 / YOLCULUKLAR')
 s=s.replace('YAKININIZDAN BAŞLIYORUZ','02 / YAKININIZDAYIZ').replace('BİR SONRAKİ DURAK','03 / SİZ NEREYE?').replace('YOLA ÇIKMADAN ÖNCE','04 / YOLA ÇIKMADAN').replace('GÖRÜŞELİM, YOLA ÇIKALIM','05 / GÖRÜŞELİM, YOLA ÇIKALIM')
 s=s.replace('Merkezdeyiz.<br>Mahallenizdeyiz.','Merkezdeyiz.<br><em>Mahallenizdeyiz.</em>').replace('Plan sizden.<br>Başlangıç buradan.','Plan sizden.<br><em>İlk adım buradan.</em>')
 s=s.replace('Yolculuk bilgilerinizi hazırlayın. Talebinizi kopyalayıp iletişim sırasında paylaşabilirsiniz.','Yolculuk bilgilerinizi girin, hazır mesajınızı WhatsApp’tan gönderin. Konumunuzu da sohbet üzerinden ekleyebilirsiniz.')
 s=s.replace('Yolculuk notunu hazırlayın ↗','WhatsApp mesajını hazırla ↗')
 s=s.replace('<button id="copy"',f'<a id="send-whatsapp" class="button yellow" href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp’ta gönder ↗</a><button id="copy"')
 s=s.replace('<strong>İletişim bilgileri hazırlanıyor</strong>',f'<a class="contact-phone" href="tel:{PHONE}">{DISPLAY} <span>↗</span></a>')
 s=s.replace('Telefon ve WhatsApp hattı eklendiğinde<br>buradan doğrudan ulaşabilirsiniz.','Telefon ve WhatsApp hattımız.<br>Gece. Gündüz. Her gün.')
 s=s.replace('<a href="#yolculuk" class="button dark">Yolculuk notu hazırlayın ↗</a>',f'<a href="{HELLO}" class="button dark" target="_blank" rel="noopener noreferrer">WhatsApp’tan ulaşın ↗</a>')
 s=s.replace('Bir sonraki yolculuk<br>burada başlıyor. <span>↗</span>','Bir telefon.<br><em>Yepyeni bir rota.</em>')
 s=s.replace('<div class="mobile-bar"><a href="#yolculuk">Yolculuk planla ↗</a><a href="#iletisim">İletişim ↗</a></div>',f'<div class="mobile-bar"><a href="tel:{PHONE}">↗ Taksi çağır</a><a href="{HELLO}" target="_blank" rel="noopener noreferrer">◉ WhatsApp</a></div>')
 s=s.replace('İletişim bölümünden hareket noktanızı, gideceğiniz adresi ve yolcu sayısını paylaşarak araç uygunluğunu öğrenebilirsiniz.',f'{DISPLAY} numarasını arayabilir veya WhatsApp’tan konum gönderebilirsiniz. Hareket noktanızı, varış adresinizi ve yolcu sayısını paylaşın. Araç uygunluğu ve alınış saati görüşmede kesinleşir.')
 s=s.replace('Seferihisar merkezden nasıl taksi talep edebilirim?','Seferihisar’da taksi nasıl çağırabilirim?')
 if area:
  tag,copy,tip=localcopy[slug]
  s=re.sub(r'<section class="section local">.*?</section>',f'<section class="section local"><div><p class="eyebrow">{area.upper()} TAKSİ</p><h2>{tag}</h2></div><div><p>{copy}</p><p>{tip}</p><a class="textlink" href="{HELLO}" target="_blank" rel="noopener noreferrer">Konumunuzu WhatsApp’tan gönderin ↗</a></div></section>',s)
 else:
  statement=f'<section class="section statement"><p class="eyebrow">SEFERİHİSAR’DA TAKSİ</p><p class="statement-text">Gideceğin yer belli.<br>Geriye sadece <em>yola çıkmak</em> kaldı.</p><div class="statement-bottom"><p>Bir arama. Bir konum.<br>Yolculuğun ilk adımı bu kadar.</p><a href="tel:{PHONE}">{DISPLAY} ↗</a></div></section>'
  s=s.replace('<section id="bolgeler"',statement+'<section id="bolgeler"')
 # Keep the local voice direct; contact details matter more than repeated slogans.
 s=s.replace('Şehir sakin.<br><em>Senin yolun açık.</em>','Seferihisar’da<br><em>taksi mi lazım?</em>')
 s=s.replace('Seferihisar’da taksi, bir telefon uzağında.<br>Merkezden sahile, gün doğumundan geceye.<br>Bir sonraki yolculuğunuz burada başlıyor.','Merkezde, mahallede ya da sahilde.<br>Bizi arayın veya WhatsApp’tan konumunuzu gönderin.<br>Nereden alınacağınızı birlikte netleştirelim.')
 s=s.replace('İZMİR’İN SAKİN ŞEHRİNDE, YOL ARKADAŞINIZ.','SEFERİHİSAR TAKSİ 7/24 · 0551 218 22 44')
 s=s.replace('YEREL ROTALAR. YENİ HİKÂYELER.','Hıdırlık Mahallesi · Seferihisar / İzmir')
 s=s.replace('Bir şehir.<br><em>Birçok güzel rota.</em>','Merkeze, sahile<br><em>ve havalimanına.</em>')
 s=s.replace('Günlük işler, sahil kaçamakları ya da bir uçuş.<br>İhtiyacınıza uygun yolculuğu birlikte planlayın.','Nereye gideceğinizi ve ne zaman yola çıkmak istediğinizi söyleyin. Araç uygunluğunu telefonla görüşelim.')
 s=s.replace('Gideceğin yer belli.<br>Geriye sadece <em>yola çıkmak</em> kaldı.','Seferihisar’da taksi için<br><em>konumunuzu göndermeniz yeterli.</em>')
 s=s.replace('Bir arama. Bir konum.<br>Yolculuğun ilk adımı bu kadar.','Alınacağınız yer, varış adresi ve yolcu sayısı.<br>Geri kalanını görüşerek netleştirelim.')
 s=s.replace('Bir telefon.<br><em>Yepyeni bir rota.</em>','Bizi arayın.<br><em>Ya da konum gönderin.</em>')
 s=s.replace('Şehrin ritmini biliyoruz.<br>Yolculuğunuzu önemsiyoruz.','Seferihisar merkez ve çevre mahalleler.<br>Telefon ve WhatsApp: 0551 218 22 44')
 path.write_text(s,encoding='utf-8')

for f in ['robots.txt','sitemap.xml']:
 p=root/f
 p.write_text(p.read_text(encoding='utf-8').replace('https://seferihisar-taksi-merkez.rubysage32.chatgpt.site',ORIGIN),encoding='utf-8')
(root/'site.webmanifest').write_text(json.dumps({'name':NAME,'short_name':'Taksi 7/24','lang':'tr','start_url':'/','scope':'/','display':'standalone','background_color':'#09131c','theme_color':'#09131c','icons':[{'src':'/assets/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'/assets/icon-512.png','sizes':'512x512','type':'image/png'}]},ensure_ascii=False),encoding='utf-8')
print('Yeni tasarım, telefon/WhatsApp, 9 özgün sayfa ve yerel SEO verileri hazır.')
