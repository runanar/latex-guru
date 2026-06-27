# Project Context

Bu dosya, projenin arka planını, kapsam sınırlarını ve temel varsayımlarını açıklamak için kullanılır.

## 1. Project Title
LaTeX-Guru: Topoloji Multimodal RAG Asistanı

## 2. Project Goal
Bu projenin temel amacı; bilgisayar basımı temiz bir online Topoloji PDF kitabını sayfa bazlı indeksleyerek güçlü bir RAG pipeline'ı kurmak; kullanıcının klavyeyle yapacağı aramalarda ilgili teorem ve tam sayfa numarasını getirmek, sistem stabil çalıştıktan sonra ise kullanıcının el yazısı formül fotoğraflarını LaTeX'e çevirip kitapta aratabileceği Vision katmanını entegre etmektir.

## 3. Business / Use Case Context
Academic Domain Document Assistant / Internal Knowledge Assistant.

## 4. Problem Statement
Topoloji gibi yoğun matematiksel sembol ve teorem içeren alanlarda, dijital dökümanlar içinde spesifik formüllere veya ispatlara sayfa bazlı hızlı erişim sağlamak zordur. Ayrıca el yazısı sembollerin doğrudan taranması gürültülü veri ürettiğinden, temiz bir dijital kaynak üzerinden güvenilir bir RAG yapısı kurmak ve deneysel aşamada el yazısı girdileri bu temiz kaynağa bağlamak kritik bir ihtiyaçtır.

## 5. Target User
Matematik Bölümü öğrencileri, akademisyenler ve araştırmacılar.

## 6. Target Workflow
Kullanıcı Arama Metni/LaTeX Girdisi → Vektör Veri Tabanı Sorgusu (RAG) → İlgili Sayfa Metninin ve Kitap Sayfa Numarasının Getirilmesi → (İlerleyen Aşamada: El Yazısı Fotoğrafı → Vision LLM ile LaTeX Dönüşümü → RAG).

## 7. In Scope
Bu proje kapsamında yapılacaklar:
- Online dijital Topoloji PDF kitabının sayfa tabanlı olarak metin ve LaTeX içeriklerinin ayıklanması.
- Ayıklanan sayfaların sayfa numarası metadata'ları ile ChromaDB/FAISS üzerinde indekslenmesi.
- Kullanıcının arama yapabileceği Streamlit tabanlı bir MVP arayüzü.
- (Aşama 2) El yazısı formül fotoğraflarını dijital arama girdisine dönüştüren Vision LLM prompt stratejisi.

## 8. Out of Scope
Bu proje kapsamında yapılmayacaklar:
- Sıfırdan bir LLM veya matematik modeli eğitmek.
- El yazısı notların tamamını sıfırdan OCR scriptleri ile temizlemeye çalışmak.

## 9. Input Types
- [PDF] Sistem kütüphanesini oluşturacak bilgisayar basımı temiz online Topoloji kitabı.
- [Görsel] İlerleyen aşamada test için yüklenecek anlık el yazısı formül fotoğrafları.

## 10. Expected Output
- Arama sorgusuna karşılık gelen en doğru teorem/tanım metni.
- Bilginin yer aldığı orijinal kitabın sayfa numarası referansı.

## 11. Technical Direction
### Initial tech choices
- **Language:** Python
- **Framework:** LangChain
- **Interface:** Streamlit
- **Vector DB:** ChromaDB
- **Config Management:** YAML

## 12. Constraints
- [Time constraint] 35 günlük bitirme projesi takvimi.
- [API budget constraint] İkinci aşamada kullanılacak Vision LLM modellerinin bütçe sınırı.

## 13. Assumptions
- Kullanılacak online topoloji kitabının dijital metin katmanının temiz olduğu varsayılır.

## 14. Risks
- Matematiksel sembollerin vektör uzayında birbirine yakınsaması nedeniyle arama kalitesinin düşmesi (Weak retrieval).

## 15. Success Criteria
- Klavyeden girilen 5 farklı topolojik kavram sorgusunda, sistemin doğru sayfayı ve döküman referansını %90 doğrulukla getirebilmesi.