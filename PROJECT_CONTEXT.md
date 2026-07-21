# Project Context

## 1. Project Title
Vision-RAG: El Yazısı Destekli Matematik ve Topoloji Kitabı Asistanı

## 2. Project Goal
Bu projenin temel amacı: Kullanıcıların el yazısıyla tuttuğu topoloji notlarının veya sorularının fotoğraflarını çekerek, dijital topoloji dökümanları içinde anlamsal arama yapabilmesini ve ilgili orijinal kitaba/LaTeX formüllerine doğrudan ulaşmasını sağlamaktır.

## 3. Business / Use Case Context
Internal Knowledge / Academic Education Assistant (Matematik ve Akademi alanı).

## 4. Problem Statement
Matematik ve topoloji alanındaki kaynaklar ağır LaTeX formülleri ve özel semboller içerir. Öğrencilerin veya bu alanda çalışan kişilerin el yazısıyla aldığı notları veya çözemedikleri soruları dijital dökümanlarda düz metin olarak aratması imkansızdır. Standart metin tarayıcılar bu sembolleri bozduğu için geleneksel RAG sistemleri bu alanda yetersiz kalmaktadır.

## 5. Target User
Matematik bölümü öğrencileri, akademisyenler ve topoloji çalışan araştırmacılar.

## 6. Target Workflow
Handwritten Image Input → Gemini Vision Processing (Text/LaTeX Extraction) → Semantic Retrieval (ChromaDB) → Context Matched Output

## 7. In Scope
- PDF dökümanının ilk 3 sayfasının görsellere dönüştürülmesi ve Gemini ile temiz LaTeX metnine çevrilmesi.
- 1000 karakter genişliğinde ve 200 karakter overlap payı olan chunking algoritması.
- Yerel ChromaDB (all-MiniLM-L6-v2) vektör veri tabanı entegrasyonu.
- Kullanıcının el yazısı fotoğrafını yükleyebileceği Streamlit arayüzü.
- El yazısı fotoğrafını anlık olarak okuyan ikinci bir Gemini Vision hattı.

## 8. Out of Scope
- Tüm kitabın (200+ sayfa) tek seferde end-to-end taranması (Maliyet ve rate-limit kısıtlaması nedeniyle ilk 3 sayfa MVP kapsamındadır).
- Fine-tuning.

## 9. Input Types
- PDF (Kaynak kitap dökümanı)
- PNG / JPG (Kullanıcının yükleyeceği el yazısı not görseli)

## 10. Expected Output
- Anlamsal olarak eşleşen döküman parçası ve orijinal LaTeX formülleri.

## 11. Technical Direction
### Planned components
- pdf2image (Document loader)
- Gemini API pipeline (Vision parsing & Handwritten text extraction)
- Character-based chunking
- all-MiniLM-L6-v2 (Embedding model)
- ChromaDB (Vector DB)
- Streamlit (Interface)

## 12. Constraints
- API bütçesi ve model istek limitleri.