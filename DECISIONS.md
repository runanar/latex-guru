# Decisions

Bu dosya, proje sürecinde alınan önemli teknik ve mimari kararları kaydetmek için kullanılır.

---

## 1) Çekirdek Veri Kaynağı Olarak Online Dijital Kitap Seçimi
**Decision:** Projede veri havuzu olarak basımı online bir Topoloji PDF kitabının kullanılması kararlaştırılmıştır.

**Reasoning:**
- El yazısı notlar üzerinde yapılan ilk OCR testlerinde, matematiksel sembollerin standardizasyonu bozduğu görülmüştür.
- Projenin kısıtlı 35 günlük takvimi göz önüne alındığında, zamanın el yazısı temizleme scriptlerine değil de projenin asıl kalbi olan RAG mimarisine harcanması bir önceliktir.

**Alternatives considered:**
- El yazısı 21 adet PDF'in tamamını Vision LLM pipeline'ı ile tek tek text tabanlı Latex metnine dönüştürmek hata riski nedeniyle ve projenin %100 sağlıklı ilerleyebilmesi sebebiyle elendi.

**Consequence:**
- `data/` klasörüne eklenecek olan online dijital PDF sayesinde `PyMuPDF` / `LangChain` parsing adımları %100 doğrulukla ve temiz LaTeX kodlarıyla yürütülebilecektir.

**Status:** Confirmed

---

## 2) Git Workflow ve Branch Ayrımı
**Decision:** Doğrudan `main` branch üzerinde geliştirme yapılması durdurulmuş ve tüm süreç `student/rana-nur-ceylan` branch'ine taşınmıştır.

**Reasoning:**
- `guide.md` kurallarının 7.3 maddesi uyarınca `main` branch'in temiz ve kontrollü bir alan olarak korunması gerekmektedir.

**Consequence:**
- Geliştirme disiplini tam olarak sağlanacak, hocanın yapacağı kontrollerde branch activity kurallara uygun görünecektir.

**Status:** Confirmed

---

## 3) Matematiksel Sembol Kaybı ve Parsing Stratejisi Revizyonu
**Decision:** Standart ham metin ayıklama yöntemi (`get_text("text")`), $\tau$ gibi matematiksel sembolleri ve indisleri sildiği için iptal edilmiş; karakter haritasını koruyan gelişmiş bir yapıya geçilmesine karar verilmiştir.

**Reasoning:**
- Ham metin okunduğunda topolojik semboller kaybolmakta ve bu durum RAG sisteminde "Weak Retrieval" (Zayıf Arama) riskini doğurmaktadır.
- Temiz bir arama deneyimi için sembollerin eksiksiz korunması başarı kriteridir.

**Status:** Proposed
---

## 3) Kütüphane Tabanlı Metin Ayıklama Sorunu ve Vision-RAG Mimarisine Geçiş
**Decision:** `PyMuPDF` ve `pdfplumber` kütüphanelerinin matematiksel topoloji sembollerini ($\tau$) `t` karakterine dönüştürerek bilgi kaybı yaratması sebebiyle, kütüphane tabanlı düz metin ayıklama (text parsing) yaklaşımı tamamen iptal edilmiştir. Projenin veri besleme (ingestion) aşaması, sayfaların yüksek çözünürlüklü görsellere dönüştürülüp bir Vision LLM (Gemini-1.5-Flash/Pro) aracılığıyla doğrudan temiz markdown/LaTeX formatında yapılandırılması mimarisine taşınmıştır.

**Reasoning:**
- Geleneksel PDF kütüphaneleri font haritalama hatası yapmakta ve "Weak Retrieval" riski doğurmaktadır.
- `PROJECT_CONTEXT.md` içinde belirtilen "Vision Katmanı Entegrasyonu" hedefi, projenin en başına (Ingestion aşamasına) çekilerek risk avantaja dönüştürülmüştür.

**Consequence:**
- Matematiksel semboller, indisler ve teoremler %100 doğrulukla ve standart LaTeX formatında veri tabanına işlenebilecektir.

**Status:** Confirmed

## 4) PDF Sayfalarını Görsele Dönüştürmek İçin Poppler Motoru Seçimi
**Decision:** `pdf2image` kütüphanesinin arkasında sistem motoru olarak **Poppler (Release-26.02.0-0)** ikili (binary) dosyalarının kullanılması kararlaştırılmıştır.

**Reasoning:**
- Devasa 276 sayfalık PDF dökümanının tamamını belleğe (RAM) yüklemek sistemi kilitlemekte ve takılmalara yol açmaktadır. 
- Poppler, `first_page` ve `last_page` parametreleri sayesinde tüm PDF'i taramadan sadece hedef sayfaları izole ve jet hızıyla işleme yeteneğine sahiptir. Anti-aliasing başarısı sayesinde LLM için en net pikselleri üretir.

**Alternatives considered:**
- **Hafıza Sınırlaması Olmayan Düz Render Modülleri:** PDF'in tamamını hafızaya yükleyerek resmi diske yazmaya çalışan alternatif yöntemler, yüksek kaynak tüketimi ve düşük işleme hızı nedeniyle elenmiştir.

**Consequence:**
- Windows ortamında çalışabilmesi için Poppler binary klasör yolunun (`poppler_path`) kod içerisinden `r"..."` (raw string) formatında manuel gösterilmesi gerekliliği doğmuştur. Projenin yerel bağımlılık haritasına eklenmiştir.

**Status:** Confirmed

---

## 5) LaTeX Ayıklama Süreci İçin Model ve Güvenlik Altyapısı Seçimi
**Decision:** Vision LLM katmanı için yeni `google-genai` SDK'sı üzerinden **gemini-2.5-flash** modelinin seçilmesine ve API anahtarı yönetiminin `.env` üzerinden yapılmasına karar verilmiştir.

**Reasoning:**
- Gemini-2.5-Flash, sayfa görsellerindeki içindekiler tablolarını (`\dotfill`, `\quad`) ve matematik dizgilerini eksiksiz bir şekilde geçerli LaTeX kod bloklarına dönüştürmede en yüksek doğruluğu ve hızı sunmuştur.
- API anahtarlarının koda gömülmesi ciddi bir güvenlik ihlalidir ve projenin elenme sebebidir. Güvenliğin yerel diske izole edilmesi teknik bir zorunluluktur.

**Alternatives considered:**
- **Eski google-generativeai kütüphanesi (v1beta API):** Yeni sürüm isimlendirme standartlarına uymadığı ve API tarafında `404 NOT FOUND` model eşleşme hatası fırlattığı için elenmiştir.

**Consequence:**
- Proje dış dünyaya (Google API bulutuna) bağımlı hale gelmiştir. API anahtarının güvenliği için ana dizine `.env` dosyası kurulmuş ve bu dosyanın GitHub'a sızması `.gitignore` kurallarıyla kesin olarak engellenmiştir.

**Status:** Confirmed