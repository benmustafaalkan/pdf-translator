# PDF Çeviri Uygulaması (End User Kurulum ve Kullanım)

## 1. Kurulum (Sadece İlk Seferde)

1. **Python 3.8 veya üzeri yüklü mü kontrol et:**
   - [Python İndir](https://www.python.org/downloads/)
   - Kurulumda "Add Python to PATH" seçeneğini işaretleyin.

2. **Kurulum Scriptini Çalıştır:**
   - `setup.bat` dosyasına çift tıkla.
   - Tüm gerekli programlar otomatik yüklenecek.

## 2. API Anahtarı Ayarlama

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresinden API anahtarını al.
2. `config.py` dosyasını Not Defteri ile aç.
3. `GEMINI_API_KEY = "your-api-key-here"` satırındaki değeri kendi anahtarınla değiştir.

## 3. Uygulamayı Başlatma

- `run_app.bat` dosyasına çift tıkla.
- Tarayıcıda uygulama otomatik açılır.

## 4. Kullanım

1. **Klasörleri Oluştur:**
   - Açılan ekranda "Klasörleri Oluştur" butonuna tıkla.
2. **PDF Yükle:**
   - "PDF Dosyası Yükle" bölümünden dosyanı seç.
3. **Çeviriyi Başlat:**
   - "Çeviriyi Başlat" butonuna tıkla.
   - İlerlemeyi ekrandaki bar ile takip et.
4. **Sonucu Gör:**
   - Çeviri bitince "Result Klasörünü Aç" butonuna tıkla.
   - Çevrilmiş PDF dosyanı bul!

---

## Sıkça Sorulan Sorular

- **Python yoksa ne yapmalıyım?**
  - [Python İndir](https://www.python.org/downloads/) ve kurulumda "Add to PATH" seçili olmalı.
- **API anahtarı nedir, nereden alırım?**
  - [Google AI Studio](https://makersuite.google.com/app/apikey) üzerinden ücretsiz alabilirsin.
- **Kurulumda hata alırsam?**
  - Komut penceresindeki uyarıları oku, eksik adım varsa tekrar dene.

---

Her şey otomatik! Sadece 3 adımda kullanıma hazır: Kur, API anahtarını gir, başlat!
