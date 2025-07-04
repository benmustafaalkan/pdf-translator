import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API anahtarı (None olabilir)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Dosya sınırları
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_PAGES = 800

# Klasör yolları (Windows için)
UPLOAD_FOLDER = "upload"
RESULT_FOLDER = "result" 