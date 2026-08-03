# 🎓 LaTeX-Guru: Vision-RAG ile Matematiksel Not Arama Sistemi

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/ChromaDB-Persistent-green.svg)](https://www.trychroma.com/)
[![LLM](https://img.shields.io/badge/Gemini-3.5--Flash-orange.svg)](https://deepmind.google/technologies/gemini/)

LaTeX-Guru, öğrencilerin derslerde tuttuğu el yazısı matematiksel notları ve görselleri analiz ederek, dijital/basılı **Topoloji** kaynak kitabında anlamsal (semantic) arama yapan iki aşamalı bir **Vision-RAG (Retrieval-Augmented Generation)** uygulamasıdır.

## 🚀 Öne Çıkan Özellikler

* **Vision OCR (Gemini 3.5 Flash):** El yazısı notlardaki karmaşık matematiksel sembolleri ve yapıları yüksek doğrulukla metne dönüştürür.
* **Çoklu Sayfa Desteği (Multi-Page Query Fusion):** Birden fazla ders notu sayfasını aynı anda kabul ederek bağlam bütünlüğünü korur.
* **Anlamsal Vektör Arama (ChromaDB + SentenceTransformers):** Kelime eşleşmesi yerine `all-MiniLM-L6-v2` embedding modeli ile anlamsal yakınlık (Cosine Similarity) üzerinden arama yapar.
* **LaTeX Metin Düzenleme (Post-Processing):** Vektör veri tabanından dönen karmaşık LaTeX kodlarını kullanıcı dostu, akıcı bir Türkçe matematiksel paragrafa dönüştürür.
* **Modern Arayüz (Streamlit):** Kullanıcı dostu ve hızlı etkileşim sunan web arayüzü.

---

## 📸 Örnek Girdi / Çıktı (Input / Output)

| Aşama | İçerik / Görünüm |
|---|---|
| **Girdi (Input)** | El yazısı Topoloji ders notu fotoğrafı (`.png` / `.jpg`) |
| **Vision OCR Çıktısı** | `f: (X, \tau) \rightarrow (Y, \tau')` matematiksel ifade dizisi |
| **Vektör Eşleşmesi** | ChromaDB üzerinden $O(\log N)$ HNSW algoritması ile Cosine Similarity araması |
| **Çıktı (Output)** | Topoloji kaynak kitabından ilgili bölüm: *3.2 Sürekli Fonksiyonlar (Sayfa 97)* ve Türkçe matematiksel açıklaması |

---

## 🧰 Kullanılan Teknolojiler ve Araçlar

* **Programlama Dili:** Python 3.10+
* **Arayüz (UI):** Streamlit
* **Multimodal LLM / OCR:** Google Gemini 3.5 Flash (`google-genai` SDK)
* **Embedding Modeli:** `SentenceTransformers - all-MiniLM-L6-v2` (384 Boyutlu Vektör Uzayı)
* **Vektör Veritabanı:** ChromaDB (`PersistentClient`)
* **PDF / Görsel İşleme:** Poppler, `pdf2image`, Pillow
* **Çevre Değişkenleri:** `python-dotenv`

---

## 🛠️ Kurulum ve Çalıştırma Adımları

Projeyi sıfır bir bilgisayara kurup çalıştırmak için aşağıdaki adımları **sırasıyla ve ayrı ayrı** uygulayın:

### Adım 1: Depoyu Klonlayın
```bash
git clone [https://github.com/runanar/latex-guru.git](https://github.com/runanar/latex-guru.git)
cd latex-guru

Adım 2: Bağımlılıkları Yükleyin
Proje, modern Python standartlarına (pyproject.toml) uygun olarak yapılandırılmıştır:

pip install -e .

Adım 3: Çevre Değişkenlerini (API Key) Ayarlayın
Proje kök dizininde .env adında bir dosya oluşturun ve Google Gemini API anahtarınızı ekleyin :

GEMINI_API_KEY="buraya_gemini_api_keyinizi_yazin"

🔑 Gemini API Anahtarı Nasıl Alınır?

Google AI Studio (aistudio.google.com) adresine bir Google hesabı ile giriş yapın.

Sol üst menüden "Get API key" butonuna tıklayın.

"Create API key" seçeneği ile ücretsiz API anahtarınızı oluşturup kopyalayın ve yukarıdaki .env dosyasına yapıştırın. (Ücretsiz kota sunduğu için kart/ücret gerektirmez).

Adım 4: Uygulamayı Başlatın
Streamlit web arayüzünü çalıştırın:

streamlit run app/ui.py

📂 Proje Dizin Yapısı

.
├── app/
│   └── ui.py           # Streamlit web arayüzü ve canlı akış yönetimi
├── data/               # ChromaDB vektör veri tabanı ve PDF kaynakları
├── ingestion.py        # PDF dönüştürme (Poppler), chunking ve veri yükleme
├── retrieval.py        # ChromaDB vektör arama motoru ve embedding pipeline
├── DECISIONS.md        # Mimari kararlar ve geliştirme günlüğü
├── pyproject.toml      # Proje bağımlılıkları ve paket yönetimi
├── .env.example        # Örnek çevre değişkenleri şablonu
└── README.md           # Proje dokümantasyonu


Demo video link:
https://www.loom.com/share/48ca5cc6f960477cb513c6ca9cb834c0