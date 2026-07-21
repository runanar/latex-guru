# Ödev Takip Günlüğü (Tasks)

Bu dosyada bitirme projem için hangi aşamada olduğumu, neleri bitirdiğimi ve sırada ne olduğunu takip ediyorum.

## Projenin Şu Anki Durumu
- **Şu anki Aşama:** Phase 6 — Projeyi Toparlama ve Teslim Aşaması
- **Şu an odaklandığım şey:** Hocanın istediği döküman kontrollerini yapmak, TOML dosyasını düzenlemek ve GitHub'a son halini atmak.
- **Son Güncelleme:** 18.07.2026

---

## Sırada Ne Var? (Backlog)
- [ ] **Gelecek Plan (Phase 7):** Kitabın kalan sayfalarını da yavaş yavaş sisteme yükleyip ChromaDB veri tabanını büyütmek
- [ ] **Gelecek Plan (Phase 8):** Streamlit arayüzünde birkaç kişi aynı anda arama yapınca donmasın diye session state ayarlarına ekleme ve çıkarma yapmak

## Şu An Yapılanlar (In Progress)
- [/] Projemin çalışabilirliğini test etmek için farklı fotoğraflarla farklı bölümlerden deneme yapıyorum

## Tamamlananlar (Done)

### 📐 Phase 1 — Proje Fikri ve İlk Adımlar
- [x] GitHub'da `latex-guru' reposunu açtım.
- [x] 'PROJECT_CONTEXT.md` dosyasını doldurdum.
- [x] Git üzerinde 'student/rana-nur-ceylan` adlı branch açtım.
- [x] `venv' sanal ortamını kurdum.
- [x] `DECISIONS.md' dosyasını başlattım.

### 🗂️ Phase 2 — Kitap Dosyaları ve PDF İşlemleri
- [x] Windows'ta PDF'leri resme çevirirken sıkıntı çıkaran 'Poppler' motorunu 'pdf2image` kütüphanesine tanıtmayı başardım.
- [x] Topoloji kitabından test amaçlı 3 sayfalık görseller çıkarttım.
- [x] 'config.yaml` dosyasını oluşturdum.

### 🧠 Phase 3 — Yapay Zeka Entegrasyonu (Görsel Okuma)
- [x] 'google-genai' kütüphanesini projeye ekledim ve 'gemini-3.5-flash` modelini bağladım.
- [x] Gemini'ye verdiğim görselleri, içindeki matematiksel sembolleri kaybetmeden temiz LaTeX formatında okuttum
- [x] API anahtarının güvenliği için '.env' dosyası açtım ve '.gitignore` ile GitHub'a gitmesini engelledim.

### 🗄️ Phase 4 — Vektör Veri Tabanı ve Metin Parçalama
- [x] Kitaptan okunan uzun metinler ve formüller ortadan ikiye bölünmesin diye 'chunk_size: 1000` ve 'chunk_overlap: 200' ayarlarıyla chunking yaptım.
- [x] Bu parçaları yapay zekanın anlayacağı vektörlere dönüştürmek için 'all-MiniLM-L6-v2` embedding modelini entegre ettim.
- [x] Vektörleri bilgisayarımda yerel olarak saklamak için ChromaDB veri tabanını kurdum ve dökümanları içine yükleyen 'app/ingestion.py` dosyasını tamamladım.

### 🔍 Phase 5 — Arama Motorunun Yazılması
- [x] Yazdığım el yazısı metni alıp ChromaDB'de en yakın benzerini arayan ve getiren 'app/retrieval.py` fonksiyonlarını yazdım.
- [x] El yazısı fotoğraflarla projemi test ettim ve başarılı oldu.

### 💻 Phase 6 — Kullanıcı Arayüzü ve Son Teslim Hazırlıkları
- [x] Streamlit kütüphanesini kullanarak projeye tarayıcı üzerinden açılan 'app/ui.py` dosyasını oluşturdum.
- [x] En başta tek bir fotoğraf ile arama yapma özelliği vardı fakat fikrimi değiştirdim ve birden çok fotoğrafı birleştirip bütün haliyle veri kaynağında arama özelliğini yerleştirdim.
- [x] Arama sonucunda ekrana karmaşık LaTeX kodları geliyordu. Bunları temizleyip metni herkesin okuyabileceği şekilde Türkçe metne dönüştüren 'clean_latex_to_normal_text` fonksiyonunu yazdım.
- [x] Eksiğim olduğunu fark edip 'requirements.txt' dosyasını sildim ve onun yerine 'pyproject.toml` dosyasını oluşturdum.
- [x] 'README.md' dosyasını yazdım, 'CHANGELOG.md' ve 'DECISIONS.md` dökümanlarını son yaptığım değişikliklere göre güncelledim.