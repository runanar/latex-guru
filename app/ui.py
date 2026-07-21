import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Sayfa ayarlarını yapıyoruz
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
    return results['documents'][0]

def parse_handwritten_image(image):
    """Kullanıcının yüklediği el yazısı fotoğrafını Gemini ile temiz arama metnine çevirir."""
    client = genai.Client()
    
    prompt = """
    Görseldeki matematiksel soruyu veya kavramı oku.
    Bize sadece arama motorunda aratabileceğimiz, temiz, anlaşılır ve sadeleştirilmiş bir metin çıktısı ver.
    Ekstra açıklama yazma.
    """
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=[image, prompt]
    )
    return response.text

def clean_latex_to_normal_text(raw_text):
    """İçinde \text{}, \setminus, \cup gibi kodlar olan karmaşık metni normal akıcı metne dönüştürür."""
    client = genai.Client()
    
    prompt = f"""
    Sana verilen aşağıdaki matematiksel metni incele. 
    İçinde bulunan tüm '\\text{{...}}', '\\setminus', '\\cup', '\\cap', '\\emptyset' gibi çiğ LaTeX kodlarını temizle.
    Bunları normal insanların okuyabileceği akıcı ve düzgün bir Türkçe matematik metnine dönüştür.
    Örnek: '\\text{{ boş kümeden farklı }}' yerine doğrudan 'boş kümeden farklı' yaz.
    Örnek: '\\tau = \\{{\\emptyset, X\\}}' gibi temel ifadeleri 'tau = {{boş küme, X}}' veya temiz sembollerle göster.
    
    Çıktı tamamen temiz, okunaklı, alt alta satırlar halinde ve akıcı bir Türkçe metin olmalıdır. Kod blokları veya çiğ ters eğik çizgiler (\\) içermemelidir.
    
    Dönüştürülecek Metin:
    {raw_text}
    """
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=[prompt]
    )
    return response.text

# --- ARAYÜZ TASARIMI ---
st.title("📐 Vision-RAG Topoloji Asistanı")
st.write("Aynı konuya ait bir ve birden fazla defter sayfasını yükleyin; sistem hepsini tek bir bütün olarak tarayıp en alakalı sonucu getirsin.")

st.divider()

# Çoklu dosya yükleme alanı
uploaded_files = st.file_uploader(
    "Aynı konuya ait notlarınızın fotoğraflarını yükleyin:", 
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"📋 **{len(uploaded_files)}** adet sayfa yüklendi. (Bu sayfalar tek bir konu olarak birleştirilecek)")
    
    # Görsellerin küçük önizlemeleri
    for idx, file in enumerate(uploaded_files):
        img = Image.open(file)
        st.image(img, caption=f"Sayfa - {idx+1}", width=250)
    
    st.divider()
    
    # Bütünsel Arama Butonu
    if st.button("Tüm Sayfaları Birleştir ve Kitapta Bütünsel Olarak Ara 🔍", type="primary", use_container_width=True):
        
        combined_text_list = []
        
        # 1. ADIM: Tüm sayfaları sırayla okuyoruz
        with st.spinner("🧠 Yapay zeka tüm sayfaları sırayla okuyor..."):
            for idx, file in enumerate(uploaded_files):
                try:
                    image = Image.open(file)
                    extracted_text = parse_handwritten_image(image)
                    combined_text_list.append(extracted_text.strip())
                    st.write(f"✅ Sayfa {idx+1} başarıyla okundu.")
                except Exception as e:
                    st.error(f"Sayfa {idx+1} okunurken hata oluştu: {e}")
        
        # Okunan tüm sayfaları tek bir dev metin haline getiriyoruz
        full_combined_query = " ".join(combined_text_list)
        
        st.divider()
        
        # 2. ADIM: Bütünsel arama yapıyoruz
        with st.spinner("🗄️ Tüm bağlam birleştirilerek kitapta en alakalı yer aranıyor..."):
            try:
                matched_chunks = search_top_chunks(full_combined_query, n_results=1)
                
                st.success("🎉 Tüm sayfaların bütününe en uygun olan kitap parçası bulundu!")
                st.subheader("🎯 Kitaptaki Bilgi (Temizlenmiş Metin):")
                
                # 3. ADIM: Gelen ham kodu temiz kedi/metin formatına çevirip basıyoruz
                with st.spinner("✨ Matematiksel metin düzenleniyor..."):
                    cleaned_result = clean_latex_to_normal_text(matched_chunks[0])
                
                with st.container(border=True):
                    st.write(cleaned_result)
                        
            except Exception as e:
                st.error(f"Arama yapılırken bir hata oluştu: {e}")
else:
    st.info("Lütfen birbiriyle alakalı defter sayfalarınızı yukarıdaki alana yükleyin.")