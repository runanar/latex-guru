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
    Matematiksel ifadeleri $ ... $ veya $$ ... $$ LaTeX formatında tut ama metinlerin okunabilir, düzenli ve paragraflar halinde olmasını sağla.
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
    Sana verilen aşağıdaki matematiksel metni incele ve temizle:
    
    1. İçinde bulunan tüm '\\text{{...}}', '\\setminus', '\\cup', '\\cap', '\\emptyset' gibi çiğ LaTeX kodlarını temizle. 
    2. Sembol kodlarını okunaklı matematik sembollerine (τ, ⊆, ∅, ∩, ∪) veya akıcı Türkçe karşılıklarına çevir.
    3. Metnin başında veya sonunda yer alan '................ 96' gibi sayfa numarası olmayan yarım kalmış nokta zincirlerini ve kesik başlıkları temizle.
    4. Bunları normal insanların okuyabileceği akıcı ve düzgün bir Türkçe matematik metnine dönüştür.
    
    ÇOK ÖNEMLİ: Orijinal metindeki alt başlıkları ve maddeleri KESİNLİKLE alt alta satırlar halinde koru.
    
    Dönüştürülecek Metin:
    {raw_text}
    """
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=[prompt]
    )
    return response.text

# ARAYÜZ TASARIMI
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
        
        # Okunan tüm sayfaları birleştiriyoruz
        full_combined_query = "\n\n".join(combined_text_list)
        
        st.divider()
        
        # --- GÖSTERİM 1: TEMİZLENMİŞ SORGU METNİ (Render Edilmiş Matematiksel Metin) ---
        st.subheader("📝 Notlarınızdan Çıkarılan Temizlenmiş Metin (Arama Sorgusu):")
        
        # Satır sonlarını Markdown içindeki paragrama çevirip düzgün LaTeX renderlama yapıyoruz
        formatted_query = full_combined_query.replace("\n", "  \n")
        with st.container(border=True):
            st.markdown(formatted_query)
        
        st.divider()
        
        # 2. ADIM: Bütünsel arama yapıyoruz
        with st.spinner("🗄️ Tüm bağlam birleştirilerek kitapta en alakalı yer aranıyor..."):
            try:
                matched_chunks = search_top_chunks(full_combined_query, n_results=1)
                
                st.success("🎉 Tüm sayfaların bütününe en uygun olan kitap parçası bulundu!")
                
                # 3. ADIM: Gelen ham kodu temiz metin formatına çevirip basıyoruz
                with st.spinner("✨ Matematiksel metin düzenleniyor..."):
                    cleaned_result = clean_latex_to_normal_text(matched_chunks[0])
                
                st.subheader("🎯 Kitaptaki Eşleşen Bilgi:")
                
                formatted_output = cleaned_result.replace("\n", "  \n")
                with st.container(border=True):
                    st.markdown(formatted_output)
                        
            except Exception as e:
                st.error(f"Arama yapılırken bir hata oluştu: {e}")
else:
    st.info("Lütfen birbiriyle alakalı defter sayfalarınızı yukarıdaki alana yükleyin.")