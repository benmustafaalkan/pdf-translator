import streamlit as st
import os
import tempfile
import platform
from pathlib import Path
import time
from dotenv import set_key

# Modülleri import et
from utils.file_manager import FileManager
from utils.pdf_processor import PDFProcessor
from utils.gemini_translator import GeminiTranslator
from config import GEMINI_API_KEY

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="PDF Çeviri Uygulaması",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS stil dosyasını yükle
def load_css():
    with open('static/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# API anahtarı kontrolü ve kullanıcıdan alma
def ensure_api_key():
    if not GEMINI_API_KEY:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2>🔑 API Anahtarı Girişi</h2>', unsafe_allow_html=True)
        api_key = st.text_input("Google Gemini API anahtarınızı girin:", type="password")
        if st.button("Kaydet ve Devam Et"):
            set_key('.env', 'GEMINI_API_KEY', api_key)
            st.success("API anahtarı kaydedildi. Uygulama yeniden başlatılıyor...")
            st.experimental_rerun()
        st.stop()

# Session state başlatma
if 'file_manager' not in st.session_state:
    try:
        st.session_state.file_manager = FileManager()
    except RuntimeError as e:
        st.error("Bu uygulama sadece Windows işletim sistemi için geliştirilmiştir.")
        st.stop()

if 'pdf_processor' not in st.session_state:
    st.session_state.pdf_processor = PDFProcessor()

if 'translator' not in st.session_state:
    if GEMINI_API_KEY == 'your-api-key-here':
        st.error("Gemini API anahtarı config.py dosyasında ayarlanmamış!")
        st.stop()
    st.session_state.translator = GeminiTranslator()

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'translation_complete' not in st.session_state:
    st.session_state.translation_complete = False

# Ana uygulama
def main():
    st.markdown("""
    <div class="header">
        <h1>📄 PDF Çeviri Uygulaması</h1>
        <p>İngilizce PDF dosyalarını Türkçe'ye çevirin</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Klasör kontrolü kartı
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2>📁 Klasör Kurulumu</h2>', unsafe_allow_html=True)
        
        upload_folder, result_folder = st.session_state.file_manager.get_folder_paths()
        
        # Klasör yollarını göster
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="folder-info">
                <div class="folder-path">{upload_folder}</div>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{upload_folder}')">Kopyala</button>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Upload Klasörü** - PDF dosyalarınızı buraya yükleyin")
        
        with col2:
            st.markdown(f"""
            <div class="folder-info">
                <div class="folder-path">{result_folder}</div>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{result_folder}')">Kopyala</button>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Result Klasörü** - Çevrilmiş dosyalar buraya kaydedilir")
        
        # Klasör kontrolü
        folders_exist, folder_message = st.session_state.file_manager.check_folders_exist()
        
        if folders_exist:
            st.markdown(f'<div class="message-box message-success">{folder_message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-box message-warning">{folder_message}</div>', unsafe_allow_html=True)
            if st.button("Klasörleri Oluştur", key="create_folders"):
                success, message = st.session_state.file_manager.create_folders()
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dosya yükleme kartı
    if folders_exist:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h2>📤 PDF Dosyası Yükle</h2>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="upload-section">
                <p>Çevirmek istediğiniz PDF dosyasını seçin</p>
                <p><strong>Maksimum:</strong> 50 MB, 800 sayfa</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "PDF dosyası seçin",
                type=['pdf'],
                key="pdf_uploader"
            )
            
            if uploaded_file is not None:
                # Dosya bilgilerini göster
                file_info = {
                    'name': uploaded_file.name,
                    'size': uploaded_file.size,
                    'size_mb': round(uploaded_file.size / (1024 * 1024), 2)
                }
                
                st.markdown(f"""
                <div class="file-info">
                    <h4>📄 {file_info['name']}</h4>
                    <p><strong>Boyut:</strong> {file_info['size_mb']} MB</p>
                    <p><strong>Tip:</strong> PDF</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Dosyayı geçici olarak kaydet
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_path = tmp_file.name
                
                # PDF doğrulama
                is_valid, validation_message = st.session_state.pdf_processor.validate_pdf(temp_path)
                
                if is_valid:
                    st.session_state.uploaded_file = temp_path
                    st.markdown(f'<div class="message-box message-success">{validation_message}</div>', unsafe_allow_html=True)
                    
                    # Çeviri butonu
                    if st.button("🔄 Çeviriyi Başlat", key="translate_btn", use_container_width=True):
                        start_translation(temp_path, uploaded_file.name)
                else:
                    st.markdown(f'<div class="message-box message-error">{validation_message}</div>', unsafe_allow_html=True)
                    # Geçici dosyayı sil
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Çeviri durumu kartı
    if st.session_state.translation_complete:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h2>✅ Çeviri Tamamlandı</h2>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="message-box message-success">
                PDF dosyanız başarıyla çevrildi ve result klasörüne kaydedildi.
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📁 Result Klasörünü Aç", key="open_folder"):
                success, message = st.session_state.file_manager.open_result_folder()
                if success:
                    st.success(message)
                else:
                    st.error(message)
            
            st.markdown('</div>', unsafe_allow_html=True)

def start_translation(file_path, original_filename):
    """Çeviri işlemini başlatır."""
    try:
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 1. PDF'den metin çıkar
        status_text.text("PDF'den metin çıkarılıyor...")
        progress_bar.progress(10)
        
        success, pages_text, message = st.session_state.pdf_processor.extract_text_from_pdf(file_path)
        if not success:
            st.error(f"Metin çıkarma hatası: {message}")
            return
        
        progress_bar.progress(20)
        
        # 2. Çeviri işlemi
        status_text.text("Çeviri başlatılıyor...")
        
        def progress_callback(progress, message):
            progress_bar.progress(20 + (progress * 0.6))  # %20-%80 arası
            status_text.text(message)
        
        success, translated_pages, message = st.session_state.translator.translate_pages(
            pages_text, progress_callback
        )
        
        if not success:
            st.error(f"Çeviri hatası: {message}")
            return
        
        progress_bar.progress(80)
        status_text.text("PDF oluşturuluyor...")
        
        # 3. Çevrilmiş metinlerden PDF oluştur
        result_filename = f"{os.path.splitext(original_filename)[0]}_TR.pdf"
        result_path = os.path.join(st.session_state.file_manager.result_folder, result_filename)
        
        success, message = st.session_state.pdf_processor.create_pdf_from_text(
            translated_pages, result_path
        )
        
        if not success:
            st.error(f"PDF oluşturma hatası: {message}")
            return
        
        progress_bar.progress(90)
        status_text.text("Temizlik yapılıyor...")
        
        # 4. Upload klasörünü temizle
        st.session_state.file_manager.clear_upload_folder()
        
        # 5. Geçici dosyayı sil
        if os.path.exists(file_path):
            os.unlink(file_path)
        
        progress_bar.progress(100)
        status_text.text("✅ Çeviri tamamlandı!")
        
        # Session state'i güncelle
        st.session_state.translation_complete = True
        st.session_state.uploaded_file = None
        
        # Sayfayı yenile
        time.sleep(2)
        st.rerun()
        
    except Exception as e:
        st.error(f"Beklenmeyen hata: {str(e)}")
        # Geçici dosyayı temizle
        if os.path.exists(file_path):
            os.unlink(file_path)

if __name__ == "__main__":
    ensure_api_key()
    main() 