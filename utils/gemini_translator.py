import google.generativeai as genai
import time
from typing import List, Tuple
from config import GEMINI_API_KEY

class GeminiTranslator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.max_retries = 3
        self.retry_delay = 2
    
    def translate_paragraph(self, text: str, retry_count: int = 0) -> Tuple[bool, str, str]:
        """Tek bir paragrafı çevirir."""
        if not text.strip():
            return True, "", "Boş metin atlandı."
        
        prompt = f"""Bu metni akademik makale üslubunda, bilimsel terimlerin ve cümlelerin bütünlüğünü koruyarak İngilizce'den Türkçe'ye çevir. Akademik terminolojiyi koru, formal üslup kullan ve thinking process ile bağlamı değerlendir.

Metin:
{text}

Çeviri:"""
        
        try:
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            if translated_text:
                return True, translated_text, "Çeviri başarılı."
            else:
                return False, "", "Çeviri boş döndü."
                
        except Exception as e:
            if retry_count < self.max_retries:
                time.sleep(self.retry_delay)
                return self.translate_paragraph(text, retry_count + 1)
            else:
                return False, "", f"Çeviri hatası (3 deneme sonrası): {str(e)}"
    
    def translate_page(self, page_text: str) -> Tuple[bool, str, str]:
        """Bir sayfanın tüm paragraflarını çevirir."""
        try:
            # Metni paragraflara böl
            paragraphs = self._split_into_paragraphs(page_text)
            translated_paragraphs = []
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    success, translated, message = self.translate_paragraph(paragraph)
                    if success:
                        translated_paragraphs.append(translated)
                    else:
                        # Çeviri başarısız olursa orijinal metni kullan
                        translated_paragraphs.append(paragraph)
                        print(f"Uyarı: {message}")
                else:
                    translated_paragraphs.append("")
            
            # Çevrilmiş paragrafları birleştir
            translated_text = "\n\n".join(translated_paragraphs)
            return True, translated_text, "Sayfa çevirisi tamamlandı."
            
        except Exception as e:
            return False, "", f"Sayfa çevirisi hatası: {str(e)}"
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Metni paragraflara böler."""
        paragraphs = []
        current_paragraph = ""
        
        for line in text.split('\n'):
            line = line.strip()
            if line:
                if current_paragraph:
                    current_paragraph += " " + line
                else:
                    current_paragraph = line
            else:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = ""
        
        # Son paragrafı ekle
        if current_paragraph:
            paragraphs.append(current_paragraph)
        
        return paragraphs
    
    def translate_pages(self, pages_text: List[Tuple[int, str]], progress_callback=None) -> Tuple[bool, List[Tuple[int, str]], str]:
        """Tüm sayfaları sırayla çevirir."""
        try:
            translated_pages = []
            total_pages = len(pages_text)
            
            for i, (page_num, page_text) in enumerate(pages_text):
                # Progress callback
                if progress_callback:
                    progress = (i / total_pages) * 100
                    progress_callback(progress, f"Sayfa {page_num} çevriliyor...")
                
                success, translated_text, message = self.translate_page(page_text)
                
                if success:
                    translated_pages.append((page_num, translated_text))
                else:
                    # Çeviri başarısız olursa orijinal metni kullan
                    translated_pages.append((page_num, page_text))
                    print(f"Sayfa {page_num} çevirisi başarısız: {message}")
                
                # API rate limiting için kısa bekleme
                time.sleep(0.5)
            
            # Son progress callback
            if progress_callback:
                progress_callback(100, "Çeviri tamamlandı!")
            
            return True, translated_pages, "Tüm sayfalar çevrildi."
            
        except Exception as e:
            return False, [], f"Toplu çeviri hatası: {str(e)}" 