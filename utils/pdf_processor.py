import PyPDF2
import os
from typing import List, Tuple, Optional
from config import MAX_FILE_SIZE, MAX_PAGES

class PDFProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def validate_pdf(self, file_path: str) -> Tuple[bool, str]:
        """PDF dosyasını doğrular ve kontrol eder."""
        try:
            # Dosya boyutu kontrolü
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                return False, f"Dosya boyutu çok büyük. Maksimum {MAX_FILE_SIZE // (1024*1024)} MB olmalı."
            
            # PDF formatı kontrolü
            if not file_path.lower().endswith('.pdf'):
                return False, "Sadece PDF dosyaları desteklenir."
            
            # PDF okunabilirlik kontrolü
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Sayfa sayısı kontrolü
                if len(pdf_reader.pages) > MAX_PAGES:
                    return False, f"Sayfa sayısı çok fazla. Maksimum {MAX_PAGES} sayfa olmalı."
                
                # PDF koruma kontrolü
                if pdf_reader.is_encrypted:
                    return False, "PDF dosyası şifrelenmiş. Lütfen şifresiz bir PDF kullanın."
                
                return True, "PDF dosyası geçerli."
                
        except Exception as e:
            return False, f"PDF dosyası okunamıyor: {str(e)}"
    
    def extract_text_from_pdf(self, file_path: str) -> Tuple[bool, List[Tuple[int, str]], str]:
        """PDF'den metin çıkarır ve sayfa numaralarıyla birlikte döner."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pages_text = []
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():  # Boş sayfaları atla
                        pages_text.append((page_num, text))
                
                return True, pages_text, "Metin başarıyla çıkarıldı."
                
        except Exception as e:
            return False, [], f"Metin çıkarılamadı: {str(e)}"
    
    def split_text_into_paragraphs(self, text: str) -> List[str]:
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
    
    def create_pdf_from_text(self, pages_text: List[Tuple[int, str]], output_path: str) -> Tuple[bool, str]:
        """Çevrilmiş metinlerden yeni PDF oluşturur."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Türkçe font desteği için özel stil
            turkish_style = ParagraphStyle(
                'Turkish',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=12,
                leading=14,
                alignment=0,  # Sol hizalama
                spaceAfter=6
            )
            
            for page_num, text in pages_text:
                # Sayfa başlığı
                page_header = Paragraph(f"Sayfa {page_num}", styles['Heading2'])
                story.append(page_header)
                story.append(Spacer(1, 12))
                
                # Sayfa metni
                paragraphs = self.split_text_into_paragraphs(text)
                for paragraph in paragraphs:
                    if paragraph.strip():
                        p = Paragraph(paragraph, turkish_style)
                        story.append(p)
                        story.append(Spacer(1, 6))
                
                story.append(Spacer(1, 20))
            
            doc.build(story)
            return True, "PDF başarıyla oluşturuldu."
            
        except Exception as e:
            return False, f"PDF oluşturulamadı: {str(e)}" 