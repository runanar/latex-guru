# Changelog

Bu dosya, proje sürecindeki önemli değişiklikleri tarih bazlı olarak kaydetmek için kullanılır.

## 2026-06-28 — Project initialized
### Added
- Proje klasör yapısı (`data/`, `app/`, `notebooks/`) kuruldu.
- `PROJECT_CONTEXT.md` ve `TASKS.md` dökümanları online kitap senaryosuna göre hazırlandı.
- `config.yaml` dosyası oluşturuldu.
- Mimari kararların izlenebilirliği için `DECISIONS.md` dosyası başlatıldı.

### Changed
- Geliştirme hattı `main` branch'ten `student/rana-nur-ceylan` branch'ine taşındı.

**Status:** Phase 1 Completed
# Changelog

Bu dosya, proje sürecindeki önemli değişiklikleri tarih bazlı olarak kaydetmek için kullanılır.

## 2026-06-28 — Project initialized
### Added
- Proje klasör yapısı (`data/`, `app/`, `notebooks/`) kuruldu.
- `PROJECT_CONTEXT.md` ve `TASKS.md` dökümanları online kitap senaryosuna göre hazırlandı.
- `config.yaml` dosyası oluşturuldu.
- Mimari kararların izlenebilirliği için `DECISIONS.md` dosyası başlatıldı.

### Changed
- Geliştirme hattı `main` branch'ten `student/rana-nur-celan` branch'ine taşındı.

**Status:** Phase 1 Completed

## 2026-07-05 — Vector Database & Core Logic
### Added
- `app/ingestion.py` scripti yazıldı; PDF dökümanları işlenerek ChromaDB yerel veri tabanına gömüldü.
- `app/retrieval.py` tamamlandı; anlamsal arama mekanizması entegre edildi.

**Status:** Phase 2 & 3 Completed

## 2026-07-12 — UI Enhancements & Dependency Migration
### Added
- `app/ui.py` arayüzü Streamlit kullanılarak yayına alındı.
- Tekli dosya yükleme yerine, çoklu sayfa yükleme ve notları tek bir havuzda birleştiren bütünsel arama özelliği eklendi.
- Ham LaTeX karmaşasını önlemek adına arayüze anlık metin temizleme katmanı (`clean_latex_to_normal_text`) eklenedi.
- Proje kök dizinine `README.md` kılavuzu eklendi.

### Changed
- Bağımlılık yönetimi eski `requirements.txt` yerine modern `pyproject.toml` (version bounding kısıtlamalarıyla) yapısına taşındı.

**Status:** Phase 4 (MVP Ready - L4 Seviyesi)