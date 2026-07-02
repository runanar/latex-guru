import os
import yaml
from pdf2image import convert_from_path
from dotenv import load_dotenv
from google import genai
from PIL import Image

# .env dosyasındaki GEMINI_API_KEY değişkenini sisteme yüklüyoruz
load_dotenv()

def load_config_file(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def convert_pdf_to_images(pdf_path, output_folder="data/page_images"):
    """PDF'in sadece ilk 3 sayfasını çok hızlı bir şekilde görsele dönüştürür."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    poppler_path = r"C:\Users\Pc\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    
    print("📸 PDF'in ilk 3 sayfası görsele dönüştürülüyor...")
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
    """Görselleri Gemini Vision modeline gönderip temiz LaTeX metnine dönüştürür."""
    # Google GenAI istemcisini başlatıyoruz (Otomatik olarak GEMINI_API_KEY'i okur)
    client = genai.Client()
    
    parsed_documents = []
    
    # Matematiksel sembolleri kaçırmaması için modele vereceğimiz kesin emir (System Prompt):
    prompt = """
    Sen uzman bir matematik ve topoloji veri ayıklama asistanısın. 
    Sana verilen sayfa görselindeki tüm metinleri, formülleri ve matematiksel sembolleri (örneğin tau, indisler, alt/üst simgeler) hiçbir kayıp olmadan, aynen göründüğü gibi temiz bir Markdown ve LaTeX formatında dizeceksin.
    metin dışındaki gürültüleri veya sayfa kenarlıklarını yoksay. Sadece içerikteki matematiksel metne odaklan.
    """
    
    print("\n Gemini Vision Katmanı Aktif: Görseller yapay zeka ile okunuyor...")
    
    for path in image_paths:
        print(f"🔄 {path} işleniyor...")
        # Görseli PIL kütüphanesiyle açıyoruz
        img = Image.open(path)
        
        # Gemini 1.5 Flash modelini çağırıyoruz
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, prompt]
        )
        
        parsed_documents.append(response.text)
        
    return parsed_documents

if __name__ == "__main__":
    config = load_config_file()
    pdf_file_path = config["data"]["raw_pdf_path"]
    
    # 1. PDF -> Görsel
    image_paths = convert_pdf_to_images(pdf_file_path)
    
    # 2. Görsel -> Temiz LaTeX Metni
    results = process_images_with_gemini(image_paths)
    
    # Ekranda test etmek için 2. sayfanın (içerik veya sembol barındıran sayfa) çıktısına bakalım
    if len(results) > 1:
        print("\n - Gemini'den Gelen Kusursuz Matematiksel Çıktı -")
        print(results[1][:600]) # İlk 600 karakteri görelim
        print("---------------------------------------------------------")