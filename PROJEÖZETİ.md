# 📄 Proje Yönetici Özeti (Executive Summary)

**Proje Adı:** LaTeX-Guru  
**Mimari:** Vision-RAG (Retrieval-Augmented Generation)  
**Uygulama Alanı:** El Yazısı Matematik Notlarından Anlamsal Ders Kitabı Taraması (Topoloji)  

---

## 🎯 1. Amaç ve Problem Tanımı
Matematik ve mühendislik öğrencilerinin ders esnasında aldığı el yazısı notlar, karmaşık semboller ve kişisel yazım biçimleri içerir. Klasik Optik Karakter Tanıma (OCR) araçları (Tesseract vb.) bu sembolleri doğru okuyamaz. Ayrıca geleneksel metin arama motorları, birebir kelime eşleşmesi aradığı için "açık küme" kavramını aratan bir öğrenciye, içinde bu ifadenin kelime olarak geçmediği ama tanımını içeren bir teoremi getiremez.

**LaTeX-Guru**, el yazısı matematik notlarını anlamlandırıp kaynak kitaplarda anlamsal (semantic) arama yaparak bu problemi çözmek amacıyla geliştirilmiş iki aşamalı bir **Vision-RAG** sistemidir.

---

## 🏗️ 2. Sistem Mimarisi ve Çalışma Mantığı

Sistem iki ana hat (pipeline) üzerinden çalışmaktadır:

### A. Offline Ingestion (İçeri Alma ve Vektörleştirme)
1. **Rasterization:** Dijital Topoloji ders kitabı Poppler altyapısıyla yüksek çözünürlüklü sayfalara dönüştürülmüştür.
2. **Chunking:** Kitap metinleri, teorem ve tanım bütünlükleri korunacak şekilde anlamsal parçalara bölünmüştür.
3. **Embedding:** `SentenceTransformers (all-MiniLM-L6-v2)` modeli kullanılarak metinler 384 boyutlu vektör uzayına aktarılmış ve **ChromaDB** (`PersistentClient`) üzerinde HNSW algoritmasıyla indekslenmiştir.

### B. Online Retrieval & Generation (Canlı Sorgu Hattı)
1. **Vision OCR (Gemini 3.5 Flash):** Kullanıcı tarafından yüklenen tekli/çoklu el yazısı sayfa görselleri multimodal LLM ile analiz edilerek temiz bir LaTeX ve Türkçe arama metnine (Query Fusion) dönüştürülür.
2. **Semantic Vector Search:** Üretilen arama metni 384 boyutlu vektöre dönüştürülüp ChromaDB üzerinde **Cosine Similarity** hesabı ile en yakın teorem/tanım parçasıyla eşleştirilir.
3. **Post-Processing:** Vektör veritabanından dönen ham LaTeX kodları, ikincil bir LLM süzgecinden geçirilerek akıcı, düzgün biçimlendirilmiş ve okunabilir bir Türkçe matematiksel paragrafa dönüştürülüp Streamlit arayüzünde sunulur.

[Kullanıcı Görseli] ──> (Gemini 2.5 Flash Vision OCR) ──> [Arama Metni]
                                                               │
                                                               ▼
[Sonuç Paragrafı] <── (Gemini Post-Processing) <── [ChromaDB Arama (all-MiniLM)]

## 🧰 3. Kullanılan Teknoloji Yığını (Tech Stack)

* **Dil & Arayüz:** Python 3.10+, Streamlit
* **Multimodal LLM / OCR Engine:** Google Gemini 3.5 Flash (`google-genai` SDK)
* **Embedding Modeli:** `all-MiniLM-L6-v2` (384-dimensional dense vectors)
* **Vektör Veritabanı:** ChromaDB (HNSW Indexing, Approximate Nearest Neighbor)
* **Görsel & PDF İşleme:** Poppler, `pdf2image`, Pillow
* **Yapılandırma & Güvenlik:** `pyproject.toml`, `python-dotenv`

---

## 🏆 4. Kazanımlar ve Elde Edilen Sonuçlar

* **Yüksek Sembol Başarısı:** El yazısındaki Yunan harfleri ve küme teorisi sembolleri sıfıra yakın kayıpla dijital ortama aktarılmıştır.
* **Milisaniyelik Arama Süresi:** Vektör veritabanı sayesinde $O(\log N)$ karmaşıklığında anlık arama sonuçları üretilmiştir.
* **Modüler Yapı:** Proje, üretim ortamı standartlarına (production-ready) uygun olarak modüler dizin yapısı ve `.env` tabanlı API güvenlik mimarisiyle kurgulanmıştır.

## EKSTRALAR

## Neden Alternatifleri Varken Bu Yöntemleri Seçtik?

A. Neden `pdf2image` + Vision LLM Seçtik? (Neden `PyMuPDF` veya `pdfplumber` Kullanmadık?)

- **Geleneksel Yöntemlerin Sınırlılığı:** `PyMuPDF` gibi kütüphaneler düz metinleri okumakta iyidir ancak topoloji kitabındaki ağır matematiksel sembolleri okurken font haritalama hatası yaparlar. Sembolleri anlamsız karakterlere ya da boşluklara dönüştürerek bilgi kaybına (`Weak Retrieval`) yol açarlar.
    
- **Bizim Çözümümüz:** Sayfaları önce görsele çevirip sonra Gemini Vision ile okutarak, matematiksel sembollerin ve indislerin yapısını birebir koruyan kusursuz bir LaTeX çıktısı elde ettik.
    

B. Neden `RecursiveCharacterTextSplitter` Seçtik? (Neden Düz Karakter Sayısına Göre Bölmedik?)

- **Geleneksel Yöntemlerin Sınırlılığı:** Eğer metni düz 1000 karaktere göre pat diye bölseydik, bir teoremin veya uzun bir LaTeX formül blokunun tam ortasından kesilme riski doğardı. Formülün yarısı bir parçada, yarısı diğer parçada kalır ve anlamı tamamen kaybolurdu.
    
- **Bizim Çözümümüz:** Bu splitter sırasıyla çift satır sonu (`\n\n`), tek satır sonu (`\n`) ve boşluklara bakarak metni böler. Böylece matematiksel teoremler, tanımlar ve uzun formül blokları ortadan ikiye bölünmeden tek bir bütün halinde aynı parçanın içinde kalır.

C. Neden `SentenceTransformerEmbeddingFunction` Seçtik? (Neden Birebir Kelime Araması Yapmadık?)

- **Geleneksel Arama Yöntemlerinin Sınırlılığı:** Klasik arama motorları sadece harflerin ve kelimelerin birebir eşleşmesine bakar. Eğer defterine yazdığın formüldeki harf dizilimi veya Türkçe cümle yapısı kitaptakiyle %100 aynı değilse arama motoru hiçbir şey bulamaz.
    
- **Bizim Çözümümüz:** Bu fonksiyon sayesinde kelimelerin harflerine değil, matematiksel ve anlamsal ağırlıklarına bakıyoruz. Kullanıcı defterine konuyu biraz farklı bir dille yazmış olsa bile, sistem cümlenin "ruhunu" yakalayıp kitaptaki doğru teoremi eşleştirebiliyor.

D.`SentenceTransformerEmbeddingFunction` (`all-MiniLM-L6-v2`) vs. OpenAI Embeddings

- **Neden kullandık?** `all-MiniLM-L6-v2` modelini seçtik çünkü **yerel (local)** olarak çalışıyor. İnternete veya harici bir ücretli API'ye bağımlı olmadan matematiksel metinleri bilgisayarında vektöre çevirebiliyor. Ayrıca akademik ve açık kaynaklı projelerde bu iş için standart olarak kabul edilen, performansı kanıtlanmış bir modeldir.
    
- **Neden OpenAI ya da Cohere kullanmadık?** Onlar internet üzerinden çalışan ve her istekte ücret kesen (pay-per-token) ticari modeller. Projeyi test etmek isteyen kişi kendi bilgisayarına indirip test etmek istediğinde internet bağlantısı koparsa veya bir API anahtarı hatası çıkarsa proje çalışmazdı. Yerel model seçerek projenin her ortamda **yinelebilir (reproducible)** olmasını sağladık.