import os
import yaml
from pdf2image import convert_from_path
# Not: API anahtarını sistemine ekledikten sonra Gemini entegrasyonu buraya bağlanacak.

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def convert_pdf_to_images(pdf_path, output_folder="data/page_images"):
    """PDF sayfalarını yüksek kaliteli PNG görsellerine dönüştürür."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    print("📸 PDF sayfaları yüksek çözünürlüklü görsellere dönüştürülüyor...")
    images = convert_from_path(pdf_path, dpi=200)
    
    saved_image_paths = []
    # Test amaçlı şimdilik sadece ilk 3 sayfayı dönüştürüp sistemi yormayalım
    for i in range(min(3, len(images))):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        images[i].save(image_path, "PNG")
        saved_image_paths.append(image_path)
        
    print(f"🎉 İlk {len(saved_image_paths)} sayfa '{output_folder}' klasörüne kaydedildi.")
    return saved_image_paths

if __name__ == "__main__":
    config = load_config()
    pdf_file_path = config["data"]["raw_pdf_path"]
    
    # 1. PDF'i Görsele Çevir
    image_paths = convert_pdf_to_images(pdf_file_path)
    
    print("\n🚀 Mimari Değişiklik Başarılı: Bir sonraki adımda bu görselleri Vision LLM ile temiz LaTeX formatına dönüştüreceğiz!")

# Windows için İndirilenler klasöründeki Poppler bin yolu:
    poppler_path = r"C:\Users\Pc\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    