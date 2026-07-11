import chromadb
from chromadb.utils import embedding_functions

def search_in_vector_db(query_text, n_results=1):
    """Kullanıcının sorusunu veri tabanında arar ve en alakalı parçayı getirir."""
    
    # 1.data/chroma_db altındaki mevcut veri tabanımıza bağlanıyoruz
    chroma_client = chromadb.PersistentClient(path="data/chroma_db")
    
    # Verileri kaydederken kullandığımız aynı embedding modelini tanımlıyoruz
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Dün gece oluşturduğumuz koleksiyonu geri çağırıyoruz
    collection = chroma_client.get_collection(
        name="topology_collection",
        embedding_function=embedding_fn
    )
    
    print(f"\n🔍 Veri tabanında aranan sorgu: '{query_text}'")
    
    # 2. Anlamsal arama (Query) işlemini tetikliyoruz
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Sonuçları ekrana basıyoruz
    print("\n En Alakalı Bulunan LaTeX Parçası:")
    print("---------------------------------------------------------")
    for doc in results['documents'][0]:
        print(doc)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    # Test etmek için kitapta geçen bir kavramı aratıyoruz
    # (Not: İleride kullanıcı buraya kendi sorusunu yazacak)
    test_query = "topology definition"
    search_in_vector_db(test_query)