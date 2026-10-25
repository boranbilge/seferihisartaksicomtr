SEFERİHİSAR TAKSİ 7/24 — SİTE KAYNAKLARI

İşletme bilgileri: site_config.json
Tam derleme: python build.py
Kontrol: python check_site.py
JavaScript sözdizimi: node --check dist/app.js
Yerel sunucu: python -m http.server 8765 --bind 127.0.0.1 --directory dist

Derleme için Python, Pillow ve Windows Arial yazı tipleri kullanılır.
Varlık bağımlılıkları: python -m pip install --target .tools -r requirements-assets.txt
Sunucuya yüklenen dist klasörü yalnızca statik HTML, CSS, JS ve görsel dosyalardır.
Form verileri sunucuya kaydedilmez. Kullanıcı WhatsApp bağlantısına dokunduğunda
hazırlanan mesaj WhatsApp'a taşınır; gönderim kullanıcı tarafından yapılır.

SEO alan adı geçişi:
seferihisartaxi.com.tr DNS doğrulaması ve HTTPS tamamlanana kadar canonical_origin,
aktif chatgpt.site adresinde kalır. Domain etkinleştikten sonra site_config.json
içindeki canonical_origin değerini https://seferihisartaxi.com.tr yapın;
python build.py ile bütün canonical, sitemap ve yapılandırılmış veriler güncellenir.
Ardından sürümü yayınlayın. Eski adresten kalıcı yönlendirme barındırıcı destekliyorsa
ayrıca yapılandırılmalıdır; site kodunda böyle bir yönlendirme kurulduğu varsayılmaz.

Logo, açıklamalar, SEO planı ve DNS notları üst dizindeki
Seferihisar-Taksi-724-Teslim klasöründedir.

Tasarım: CSS/SVG sahne derinliği, fareyle perspektif, hafif araç animasyonu,
kaydırma açılışları, azaltılmış hareket tercihi ve sabit mobil çağrı çubuğu.
Tarayıcı görsel QA, bilgisayar kullanım aracının Windows'ta URL'yi güvenilir
okuyamaması nedeniyle tamamlanamadı. Programatik kontroller check_site.py ile yapılır.
