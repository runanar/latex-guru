import os
import yaml
from pdf2image import convert_from_path
from dotenv import load_dotenv
from google import genai
from PIL import Image
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

def load_config_file(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def convert_pdf_to_images(pdf_path, output_folder="data/page_images"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    poppler_path = r"C:\Users\Pc\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    
    print(" PDF'in ilk 3 sayfası görsele dönüştürülüyor...")
    images = convert_from_path(
        pdf_path, 
        dpi=150, 
        poppler_path=poppler_path,
        first_page=1,
        last_page=3
    )
    
    saved_image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(image_path, "PNG")
        saved_image_paths.append(image_path)
        
    print(f"🎉 İlk {len(saved_image_paths)} sayfa kaydedildi.")
    return saved_image_paths

def process_images_with_gemini(image_paths):
    client = genai.Client()
    parsed_documents = []
    
    prompt = """
    Sen uzman bir matematik ve topoloji veri ayıklama asistanısın. 
    Sana verilen sayfa görselindeki tüm metinleri, formülleri ve matematiksel sembolleri (örneğin tau, indisler, alt/üst simgeler) 
    hiçbir kayıp olmadan, aynen göründüğü gibi temiz bir Markdown ve LaTeX formatında dizeceksin.
    Metin dışındaki gürültüleri veya sayfa kenarlıklarını yoksay. Sadece içerikteki matematiksel metne odaklan.
    """
    
    print("\n Gemini Vision Katmanı Aktif: Görseller yapay zeka ile okunuyor...")
    
    for path in image_paths:
        print(f"{path} işleniyor...")
        img = Image.open(path)
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=[img, prompt]
        )
        
        parsed_documents.append(response.text)
        
    return parsed_documents

def chunk_latex_text(text, chunk_size=1000, chunk_overlap=200):
    """Metni config değerlerine göre karakter bazlı ve overlap korumalı parçalar."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - chunk_overlap)
        
    return chunks

def save_to_vector_db(chunks):
    """Parçalanmış LaTeX metinlerini yerel ChromaDB veri tabanına indeksler."""
    print("\n Yerel ChromaDB bağlantısı kuruluyor...")
    
    # data/chroma_db klasörü altında kalıcı (persistent) bir veri tabanı oluşturuyoruz
    chroma_client = chromadb.PersistentClient(path="data/chroma_db")
    
    # Matematiksel metinleri vektöre çevirecek yerel embedding fonksiyonunu tanımlıyoruz
    # Default model: all-MiniLM-L6-v2 (hafif, hızlı ve etkilidir)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # 'topology_collection' adında bir koleksiyon oluşturuyoruz veya varsa açıyoruz
    collection = chroma_client.get_or_create_collection(
        name="topology_collection",
        embedding_function=embedding_fn
    )
    
    # ChromaDB'ye ekleme yaparken her parça için benzersiz ID'ler üretmeliyiz
    ids = [f"id_{i}" for i in range(len(chunks))]
    
    print("🔄 Metin parçaları vektörleştiriliyor ve veri tabanına yazılıyor...")
    collection.add(
        documents=chunks,
        ids=ids
    )
    print("Vektör veri tabanı kaydı başarıyla tamamlandı!")

if __name__ == "__main__":
    config = load_config_file()
    pdf_file_path = config["data"]["raw_pdf_path"]
    
    # 1. PDF -> Görsel
    image_paths = convert_pdf_to_images(pdf_file_path)
    
    # 2. Görsel -> Temiz LaTeX Metni
    results = process_images_with_gemini(image_paths)
    full_latex_text = "\n\n".join(results)
    
    # 3. Metni Parçalara Ayırma (Chunking)
    c_size = config["chunking"]["chunk_size"]
    c_overlap = config["chunking"]["chunk_overlap"]
    text_chunks = chunk_latex_text(full_latex_text, chunk_size=c_size, chunk_overlap=c_overlap)
    
    print("\n Metin Parçalama Tamamlandı!")
    print(f" Toplam Oluşan Parça (Chunk) Sayısı: {len(text_chunks)}")
    
    # 4. Vektör Veri Tabanına Kayıt
    save_to_vector_db(text_chunks)
    print("---------------------------------------------------------")