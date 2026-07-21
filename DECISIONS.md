# Decisions


## 1) Veri Kaynağı: Neden El Yazısı Yerine Dijital Kitap Seçildi
**Decision:** Projede veri havuzu olarak basımı online olan bir Topoloji PDF kitabını kullanmaya karar verdim.

**Reasoning:**
- El yazısı PDF'ler ile yaptığım OCR testlerinde karmaşık matematiksel sembolleri çok bozduğunu fark ettim.
- Proje için vakit kısıtlı ve asıl önemli kısım olan RAG kısmına odaklanmak daha önemli. O yüzden 21 adet el yazısı PDF'i tek tek temizlemektense dijital kitabı kullanmak çok daha temiz ve güvenilir.

**Consequence:**
- 'data/` klasörüne eklediğim online dijital PDF kitabı sayesinde veri tabanını besleme adımları çok daha sağlıklı ve sorunsuz şekilde yürüdü.

**Status:** Confirmed


## 2) Vision-RAG Architecture & Parsing Strategy Revision
**Decision:** Başlangıçta kullandığım 'PyMuPDF' ve 'pdfplumber` gibi standart metin okuma kütüphanelerini kullanmaktan vazgeçtim. Bunun yerine sayfaları yüksek çözünürlüklü resme çevirip Gemini Vision aracılığıyla RAG mimarisine geçtim.

**Reasoning:**
- Geleneksel kütüphaneler topoloji sembollerini ve matematiksel sembolleri okuyamıyor, sembolü düz yazı gibi okuyup projede bilgi kaybı yaratıyordu (weak retrieval).
- Matematiksel sembollerin hatasız ve eksiksiz olması gerekiyordu bu yüzden bu riski ortadan kaldırmak için projeyi Vision-RAG mimarisine taşıdım. Sayfaları resim olarak Gemini'ye okutarak tüm sembollerin kusursuz ve temiz bir Latex çıktısı olarak veri tabanına yazılmasını sağladık.

**Consequence:**
- Matematiksel semboller, indisler ve teoremler yüksek doğrulukla ve standart LaTeX formatında veri tabanına işlenebildi.

**Status:** Confirmed


## 3) PDF Sayfalarını Görsele Dönüştürmek İçin Poppler Motoru Seçimi
**Decision:** 'pdf2image` kütüphanesinin arkasında çalışması için sistem motoru olarak Poppler kullanmaya karar verdim.

**Reasoning:**
- 276 sayfalık PDF kitabı tek seferde bilgisayarın hafızasına yüklemeye kalkınca sistem çok zorlanıyordu.
- Poppler motorunun 'first_page` ve 'last_page' ayarları sayesinde tüm PDF'i değil sadece hedeflediğim sayfaları hızlıca okuyabildim. Ayrıca görüntü kalitesi çok iyi olduğu için kullandığım Gemini yazıları çok net okuyabildi.

**Alternatives considered:**
- **Hafıza Sınırlaması Olmayan Düz Render Modülleri:** PDF'in tamamını hafızaya yükleyerek resmi diske yazmaya çalışan diğer yöntemler, yüksek kaynak tüketimi ve düşük işleme hızı nedeniyle elendi.

**Consequence:**
- Windows ortamında çalışabilmesi için Poppler binary klasör yolunun 'poppler_path' kod içerisinden raw string formatında manuel gösterilmesi gerekliliği doğdu.

**Status:** Confirmed


## 4) Model ve Güvenlik Altyapısı Seçimi
**Decision:** Görselleri okutmak için yeni 'google-genai' kütüphanesi üzerinden gemini-3.5-flash modelini seçtim. API anahtarını güvenlik için koda yazmayıp '.env' dosyasına gizledim.

**Reasoning:**
- Eski kütüphane sürümü güncelliğini yitirdiği için 404 NOT FOUND hatası veriyordu, ben de Google'ın güncel yazılım Gemini Flash'e geçtim, sayfalardaki yoğun matematiksel formülleri ve tabloları yapısal bütünlüğünü koruyarak LaTeX formatına kolayca aktardı.
- API key'i koda yazıp GitHub'a atsaydım çok büyük bir güvenlik açığı olurdu. Bu yüzden '.env' dosyası açıp '.gitignore` ile orayı dış dünyaya kapattım.

**Alternatives considered:**
- **Eski google-generativeai kütüphanesi (v1beta API):** Yeni sürüm isimlendirme standartlarına uymadığı için elendi.

**Consequence:**
- Proje Google API bulutuna bağımlı hale geldi. API anahtarının güvenliği için ana dizine '.env' dosyası kuruldu ve bu dosyanın GitHub'a sızmasını engellemek için '.gitignore` dosyasını oluşturduk.
**Status:** Confirmed


## 5) Choose Vector Database
**Decision:** Projenin ana hafızası (vektör veri tabanı) olarak ChromaDB kullanmaya karar verdim.

**Reasoning:**
- Gidip ekstra bir sunucu kiralamakla veya ağır veritabanları kurmakla uğraşmak istemedim. ChromaDB çok hafif, doğrudan kendi bilgisayarımda çalışıyor ve verileri yerel `persistent' klasörüne kaydedebiliyor.
- Ayrıca Python'la ve kullandığım metin dönüştürücü modelle 'all-MiniLM-L6-v2' hiçbir sorun çıkarmadan entegre oldu.

**Status:** Confirmed


## 6) Chunking
**Decision:** Kitaptaki yazıları veri tabanına kaydederken boyutlarını sabitledim,'1000 character chunk_size' parçalara böldüm ve aralarında '200 character chunk_overlap' bıraktım.

**Reasoning:**
- Topolojide teoremler ve tanımlar gerçekten çok uzun. Eğer rastgele bölseydim, formüllerin tam ortasından ikiye kesilme riski vardı. 1000 karakter,bir formülün bütün halinde sığması için ideal olan dengeydi.
- Yine de sınırda kalan bir cümle olursa diye 200 karakterlik örtüşme payı koydum ki önceki parçayla sonraki parça birbirine bağlansın, anlam kopmasın.

**Status:** Confirmed


## 7) Çoklu Sayfa Birleştirme ve Bütünsel Retrieval Mantığı
**Decision:** Kullanıcının yüklediği defter sayfalarını ayrı ayrı aratmak yerine, hepsindeki yazıları tek bir büyük metin havuzunda birleştirip ChromaDB'de öyle aratmaya karar verdim.

**Reasoning:**
- Biz öğrenciler not tutarken genelde bir konu arka sayfaya sarkabiliyor. Sayfaları parça parça aratırsam sistem konunun bağlamını kaybediyordu.
- Hepsini birleştirip arattığımda (bütünsel arama), arama motorunun kitaptaki asıl konuyu bulma ihtimali ve doğruluğu çok ciddi oranda arttı.

**Consequence:**
- Sayfalar arası bağlam anlam korundu ve arama motorunun isabet oranı en üst seviyeye çıkarıldı.

**Status:** Confirmed


## 8) Bağımlılık Yönetiminde pyproject.toml Standardına Geçiş
**Decision:** Klasik 'requirements.txt' dosyasını sildim. Yerine güncel Python standardı olan 'pyproject.toml` yapısını kurdum ve kütüphanelere üst sürüm sınırları ekledim.

**Reasoning:**
- TOML dosyası 'requirements.txt' dosyasından daha profesyonel ve hocamızın da projemizde görmek istediği bir dosya türüydü. Ayrıca projenin gelecekte de düzgün çalışabilmesi için modern standart.
- Kütüphanelere de sürüm sınırı koydum ki, ileriki zamanlarda bir kütüphaneye büyük bir güncelleme gelirse benim kodlarımı bozmasın.

**Consequence:**
- Proje modern Python standartlarına kavuştu, sürüm güncellemelerinden kaynaklı çökme riskleri tamamen ortadan kaldırıldı.

**Status:** Confirmed