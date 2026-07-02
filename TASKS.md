# Tasks

Bu dosya, LATEX-GURU projemin geliştirme aşamalarını, yapılan işleri ve gelecek planlamalarını detaylı bir şekilde takip etmek için kullanılır.

## Project Status
- **Current Phase:** Phase 4 - Vector Database & Embedding Integration
- **Current Focus:** Üretilen temiz LaTeX metinlerinin akıllı parçalara ayırma stratejisiyle bölünmesi ve ChromaDB'ye basılması
- **Last Updated:** 2026-07-03

---

## Backlog
- [ ] **Phase 4.2:** Parçalanan LaTeX metinleri için text-embedding vektör dönüşümlerini entegre et
- [ ] **Phase 4.3:** ChromaDB koleksiyon yapısını oluştur ve vektörleri yerel diske indexle
- [ ] **Phase 5:** Retrieval (Arama) mekanizmasını kurarak formül bazlı eşleşme başarı oranını test et
- [ ] **Phase 6:** Kullanıcı arayüzü (CLI veya Streamlit MVP) geliştirerek sistemi test edilebilir hale getir

## In Progress
- [/] **Phase 4.1:** `config.yaml` parametrelerine uygun (`chunk_size: 1000`, `chunk_overlap: 200`) matematiksel metin parçalama (chunking) algoritmasının yazılması

## Done
- [x] **Milestone 1:** Proje vizyonunun belirlenmesi, `PROJECT_CONTEXT.md` ve `config.yaml` altyapısının kurulması
- [x] **Phase 1:** `venv` sanal ortamının kurulması ve `requirements.txt` bağımlılık listesinin dökülmesi
- [x] **Phase 2:** Windows işletim sistemi için `Poppler-26.02.0` motorunun `pdf2image` kütüphanesine başarıyla entegre edilmesi ve 276 sayfalık Topoloji kitabından ilk 3 sayfalık yüksek çözünürlüklü test görsellerinin üretilmesi
- [x] **Phase 3:** `google-genai` SDK'sı üzerinden `gemini-2.5-flash` Vision modelinin bağlanması; üretilen sayfa görsellerinin matematiksel semboller, indisler ve `\documentclass` yapısı korunarak kusursuz LaTeX Markdown formatında dışarı aktarılması