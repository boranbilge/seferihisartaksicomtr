"""Verify the generated public files; no external accounts or messaging needed."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json,re,sys,xml.etree.ElementTree as ET

BASE=Path(__file__).parent
ROOT=BASE/'dist'
sys.path.insert(0,str(BASE/'.tools'))
from PIL import Image
cfg=json.loads((BASE/'site_config.json').read_text(encoding='utf-8'))

class Document(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.tags=[];self.ids=set();self.links=[];self.h1=0;self.errors=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if tag=='h1':self.h1+=1
  if 'id' in a:
   if a['id'] in self.ids:self.errors.append('duplicate id '+a['id'])
   self.ids.add(a['id'])
  if tag=='a':self.links.append(a)

pages=list(ROOT.rglob('index.html'));assert len(pages)==9
titles=set();descriptions=set();canonical=set();checks=0
for file in pages:
 s=file.read_text(encoding='utf-8');doc=Document();doc.feed(s)
 assert not doc.errors,(file,doc.errors)
 assert doc.h1==1,(file,'H1 count')
 title=re.search(r'<title>(.*?)</title>',s).group(1)
 desc=next(a['content'] for t,a in doc.tags if t=='meta' and a.get('name')=='description')
 assert title not in titles and desc not in descriptions
 titles.add(title);descriptions.add(desc)
 can=next(a['href'] for t,a in doc.tags if t=='link' and a.get('rel')=='canonical');canonical.add(can)
 assert can.startswith(cfg['canonical_origin'])
 assert 'İletişim bilgileri hazırlanıyor' not in s
 assert cfg['address'].split(',')[0] in s and cfg['display_phone'] in s
 assert any(a.get('href')=='tel:'+cfg['telephone'] for a in doc.links)
 assert any(a.get('href','').startswith('https://wa.me/'+cfg['whatsapp']) for a in doc.links)
 assert 'send-whatsapp' in doc.ids and 'trip-form' in doc.ids
 assert s.index('call-banner')>s.index('</header>')
 data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s).group(1))
 biz=next(n for n in data['@graph'] if n['@type']=='LocalBusiness')
 assert biz['telephone']==cfg['telephone'] and biz['name']==cfg['name']
 assert biz['openingHoursSpecification']['opens']=='00:00'
 assert any(n['@type']=='TaxiService' for n in data['@graph'])
 for tag,a in doc.tags:
  target=a.get('src') if tag in ['img','script'] else a.get('href') if tag in ['a','link'] else a.get('srcset') if tag=='source' else None
  if not target:continue
  if target.startswith('/'):
   parts=urlsplit(target);local=ROOT/unquote(parts.path.lstrip('/'))
   if local.is_dir():local=local/'index.html'
   assert local.is_file(),(file,'missing local target',target)
   if parts.fragment:
    other=Document();other.feed(local.read_text(encoding='utf-8'));assert parts.fragment in other.ids,(file,target)
  elif target.startswith('#'):assert target[1:] in doc.ids,(file,'missing fragment',target)
  if a.get('target')=='_blank':assert 'noopener' in a.get('rel',''),(file,'unsafe target')
 checks+=1
sitemap=ET.parse(ROOT/'sitemap.xml')
urls={e.text for e in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert urls==canonical
assert 'Sitemap: '+cfg['canonical_origin']+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
manifest=json.loads((ROOT/'site.webmanifest').read_text(encoding='utf-8'))
assert manifest['name']==cfg['name']
for icon in manifest['icons']:assert (ROOT/icon['src'].lstrip('/')).is_file()
gif=Image.open(ROOT/'assets/taksi-cagir.gif')
assert gif.size==(960,180) and gif.n_frames>1
assert 'loop' not in gif.info,'GIF should play once'
assert (ROOT/'assets/taksi-cagir.gif').stat().st_size<250_000
assert Image.open(ROOT/'assets/social.png').size==(1200,630)
for p in (ROOT/'assets').glob('*.svg'):ET.parse(p)
css=(ROOT/'experience.css').read_text(encoding='utf-8')
assert 'prefers-reduced-motion' in css and '@media(max-width:680px)' in css
print(f'PASS: {checks} pages; unique SEO metadata; schema; phone/WhatsApp; all local links/assets/fragments; sitemap; GIF {gif.n_frames} frames; PNG/SVG; mobile/reduced-motion rules.')
