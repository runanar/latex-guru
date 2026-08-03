import time
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

BOOK_TITLE = "TOPOLOJİ DERS NOTLARI"
BOOK_AUTHOR = "Prof. Dr. İsmet Karaca"

def _is_retryable_error(err_str: str) -> bool:
    """503/UNAVAILABLE, 429/RESOURCE_EXHAUSTED ve 'overloaded'/'high demand' gibi
    geçici, tekrar denemeye değer hataları yakalar."""
    err_str = err_str.upper()
    retryable_markers = [
        "503", "UNAVAILABLE",
        "429", "RESOURCE_EXHAUSTED",
        "OVERLOADED", "HIGH DEMAND", "QUOTA",
    ]
    return any(marker in err_str for marker in retryable_markers)

st.set_page_config(
    page_title="Vision-RAG Topoloji Asistanı",
    page_icon="📐",
    layout="centered"
)

def search_top_chunks(query_text, n_results=1):
    """Veri tabanından en alakalı parçayı getiren fonksiyon."""
    chroma_client = chromadb.PersistentClient(path="data/chroma_db")
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = chroma_client.get_collection(
        name="topology_collection",
        embedding_function=embedding_fn
    )
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    if results and results.get('documents') and len(results['documents'][0]) > 0:
        return results['documents'][0]
    return []

def parse_handwritten_images_batch(images, max_retries=3):
    """TÜM görselleri TEK BİR İSTEKTE güncel google-genai SDK model isimleriyle gönderir."""
    client = genai.Client()
    
    prompt = """
    Sana verilen tüm el yazısı sayfalarındaki matematiksel soruları veya kavramları sırasıyla okuyup birleştir.
    Bize tek bir bütün halinde, arama motorunda aratabileceğimiz temiz, anlaşılır ve sadeleştirilmiş metin çıktısı ver.
    Matematiksel ifadeleri $...$ veya $$...$$ LaTeX formatında tut ama metinlerin okunabilir, düzenli ve paragraflar halinde olmasını sağla.
    \textbf{...} gibi ham LaTeX metin komutlarını doğrudan kullanma, onları Markdown formatına (**...**) dönüştür.
    Ekstra açıklama veya giriş cümlesi yazma.
    """
    
    contents = list(images)
    contents.append(prompt)
    
    # Google yeni kullanıcıları doğrudan 3.x serisine yönlendiriyor.
    candidate_models = [
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
    ]
    
    last_exception = None
    for model_name in candidate_models:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
                return response.text
            except Exception as e:
                last_exception = e
                err_str = str(e)
                if "404" in err_str or "NOT_FOUND" in err_str.upper():
                    break
                if _is_retryable_error(err_str) and attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 1, 2, 4 sn... üstel bekleme
                    continue
                break

    raise last_exception

def clean_latex_to_normal_text(raw_text, max_retries=3):
    """Metni temizler, \textbf{...} kodlarını Markdown kalın metnine çevirir ve düzgün derlenmesini sağlar."""
    client = genai.Client()
    
    prompt = f"""
    Sana verilen aşağıdaki matematiksel teorem ve ispat metnini incele ve düzenle:
    
    1. Metinde geçen '\\textbf{{Metin}}' kalıplarını tamamen temizle ve onları Markdown formatındaki gibi kalın (**Metin**) yap. (Örn: '\\textbf{{Örnek 5:}}' ifadesini '**Örnek 5:**' yap).
    2. Metindeki tüm matematiksel sembol ve eşitlikleri ($...$ veya $$...$$) olacak şekilde geçerli LaTeX formatında koru.
    3. KESİNLİKLE KOD BLOĞU (```, ```latex, ```text vb.) KULLANMA. Çıktıyı doğrudan düz Markdown ve LaTeX metni olarak ver.
    4. Metnin başındaki veya sonundaki yarım kalmış nokta zincirlerini ve parçalanmış karakterleri temizle.
    5. 'İşte temizlenmiş metin:' gibi giriş veya açıklama cümlelerini KESİNLİKLE yazma.
    6. Alt başlıklar, şıklar (a, b, c) ve İspat satırları düzenli bir şekilde alt alta bulunsun.
    7. Metin bir içindekiler/başlık listesi gibi arka arkaya sıralanmış numaralı başlıklardan oluşuyorsa
       (örn: "3.2 Sürekli Fonksiyonlar 97 3.3 Açık Fonksiyonlar 108" gibi), bunları TEK SATIRDA birleştirme;
       her bir başlığı kendi satırına ayır ve başına "- " koyarak Markdown liste öğesi haline getir
       (örn: "- 3.2 Sürekli Fonksiyonlar — 97"). Sayfa numarası varsa başlıktan bir tire (—) ile ayır.
    
    Dönüştürülecek Metin:
    {raw_text}
    """
    
    # NOT: gemini-1.5-flash kaldırıldı (deprecated, 404 veriyor).
    # NOT: gemini-2.5-flash / gemini-2.5-flash-lite YENİ API anahtarları için
    # artık tamamen engellenmiş durumda ("no longer available to new users",
    # 404 NOT_FOUND) — bu yüzden fallback olarak da işe yaramıyorlar.
    # Google yeni kullanıcıları doğrudan 3.x serisine yönlendiriyor.
    candidate_models = [
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
    ]
    
    last_exception = None
    for model_name in candidate_models:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt]
                )
                
                text = response.text
                if text.startswith("```"):
                    text = text.split("\n", 1)[-1]
                if text.endswith("```"):
                    text = text.rsplit("```", 1)[0]
                    
                return text.strip()
            except Exception as e:
                last_exception = e
                err_str = str(e)
                if "404" in err_str or "NOT_FOUND" in err_str.upper():
                    break
                if _is_retryable_error(err_str) and attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 1, 2, 4 sn... üstel bekleme
                    continue
                break

    raise last_exception

# ARAYÜZ TASARIMI
st.title("📐 Vision-RAG Topoloji Asistanı")
st.write("Aynı konuya ait bir ve birden fazla defter sayfasını yükleyin; sistem hepsini tek bir bütün olarak tarayıp en alakalı sonucu getirsin.")

st.divider()

uploaded_files = st.file_uploader(
    "Aynı konuya ait notlarınızın fotoğraflarını yükleyin:", 
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"📋 **{len(uploaded_files)}** adet sayfa yüklendi. (Bu sayfalar tek bir konu olarak birleştirilecek)")
    
    cols = st.columns(min(len(uploaded_files), 4))
    pil_images = []
    
    for idx, file in enumerate(uploaded_files):
        img = Image.open(file)
        pil_images.append(img)
        with cols[idx % 4]:
            st.image(img, caption=f"Sayfa - {idx+1}", use_container_width=True)
    
    st.divider()
    
    if st.button("Tüm Sayfaları Birleştir ve Kitapta Bütünsel Olarak Ara 🔍", type="primary", use_container_width=True):
        
        with st.spinner("🧠 Yapay zeka tüm sayfaları inceliyor ve birleştiriyor..."):
            try:
                full_combined_query = parse_handwritten_images_batch(pil_images)
                st.success("✅ Tüm sayfalar başarıyla okundu ve birleştirildi!")
            except Exception as e:
                st.error(f"Görseller okunurken API hatası oluştu: {e}")
                st.stop()
        
        if full_combined_query:
            st.divider()
            
            st.subheader("📝 Notlarınızdan Çıkarılan Temizlenmiş Metin (Arama Sorgusu):")
            
            formatted_query = full_combined_query.replace("\n", "  \n")
            with st.container(border=True):
                st.markdown(formatted_query)
            
            st.divider()
            
            with st.spinner("🗄️ Tüm bağlam birleştirilerek kitapta en alakalı yer aranıyor..."):
                try:
                    matched_chunks = search_top_chunks(full_combined_query, n_results=1)
                    
                    if matched_chunks:
                        st.success("🎉 Tüm sayfaların bütününe en uygun olan kitap parçası bulundu!")
                        
                        with st.spinner("✨ Matematiksel metin düzenleniyor..."):
                            cleaned_result = clean_latex_to_normal_text(matched_chunks[0])
                        
                        st.subheader("🎯 Kitaptaki Eşleşen Bilgi:")
                        
                        with st.container(border=True):
                            st.markdown(f"**{BOOK_TITLE}**  \n*{BOOK_AUTHOR}*")
                            st.markdown("---")
                            st.markdown(cleaned_result)
                    else:
                        st.warning("⚠️ Veritabanında uygun bir eşleşme bulunamadı.")
                            
                except Exception as e:
                    st.error(f"Arama yapılırken bir hata oluştu: {e}")
else:
    st.info("Lütfen birbiriyle alakalı defter sayfalarınızı yukarıdaki alana yükleyin.")