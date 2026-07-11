import streamlit as st
import chromadb
from chromadb.utils import embedding_functions

# Sayfa ayarlarını yapıyoruz (Tarayıcı sekmesinde görünecek başlık ve ikon)
st.set_page_config(
    page_title="LaTeX Topoloji Asistanı",
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

# --- ARAYÜZ TASARIMI ---

st.title("📐 LaTeX Topoloji Asistanı")
st.write("Topoloji kitabınız içindeki kavramları ve LaTeX formüllerini anlamsal olarak arayın.")

# Kullanıcıdan soruyu alacağımız arama kutusu
user_query = st.text_input("Aramak istediğiniz kavram veya formülü yazın:", placeholder="Örn: topology definition veya Sıralama Topolojisi")

# Arama Butonu
if st.button("Kitapta Ara 🔍"):
    if user_query.strip() == "":
        st.warning("Lütfen boş bir sorgu bırakmayın!")
    else:
        with st.spinner("Veri tabanında arama yapılıyor, lütfen bekleyin..."):
            try:
                # Arama fonksiyonumuzu tetikliyoruz
                matched_chunks = search_top_chunks(user_query, n_results=1)
                
                st.success("En alakalı içerik bulundu!")
                st.subheader("🎯 Eşleşen Kitap Parçası:")
                
                # Bulunan LaTeX metnini Streamlit'in özel markdown/kod bloğu içinde gösteriyoruz
                st.markdown(matched_chunks[0])
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")