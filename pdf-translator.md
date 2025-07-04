# Katı Kurallı Akademik PDF Çeviri Uygulaması Geliştirme Promptu

Aşağıdaki kurallara **%100 bağlı kalacak**, Python ile geliştirilecek, Windows işletim sistemine özel, localde çalıştırılabilen ve tarayıcıdan erişilebilen bir PDF çeviri uygulaması oluştur:

---

## TEMEL KURALLAR & İŞLEVLER

1. **Sadece İngilizce'den Türkçe'ye çeviri yapacak.**
2. **Kullanıcıdan bir PDF dosyası alacak (yükleme formu).**
3. **Yüklenen PDF'in sayfa sayısı neyse, çıktı PDF'i de aynı sayfa sayısına sahip olacak.**
4. **Kaynak dosyada 243. sayfadaki cümle, çıktı PDF'inde de 243. sayfada yer alacak.**
5. **Çıktı dosyasının fontu, puntosu, satır sonları veya sayfa başlıkları önemli değil, sadece okunabilirlik yeterli.**
6. **PDF'deki tüm metinler, cümle cümle veya kelime kelime değil; paragraf bazında çevirilecek.**
7. **Yazıdan bağımsız ögeler (görseller, tablolar, formüller, şekiller vs.) orijinaliyle, olduğu gibi aktarılsın. Çeviri yalnızca metin üzerinde yapılsın.**
8. **Çeviri işlemi sırasında kullanıcıya kalan süreyi veya ilerlemeyi gösteren bir progress bar / loading bar arayüzde yer alacak.**
9. **Çeviri tamamlanınca çıktı PDF'i, otomatik olarak kullanıcının bilgisayarında önceden belirlenmiş veya kullanıcının seçtiği bir klasöre kaydedilecek. Kullanıcıya bu klasörün yolu arayüzde açıkça gösterilecek. "İndir" butonu olmayacak.**
10. **Ekstra hiçbir kullanıcı hesabı, login sistemi veya veritabanı olmayacak.**
11. **Tüm süreç localde, kullanıcı makinesinde çalışacak.**
12. **Uygulama, tarayıcı üzerinden açılabilen sade ve anlaşılır bir arayüze sahip olacak (HTML tabanlı veya Streamlit/Flask gibi framework kullanılabilir).**
13. **Kullanıcı, sadece bir PDF yükleyip, çıktı PDF'inin otomatik olarak belirli klasöre kaydedilmesini görecek; başka bir ayar, ek özellik veya karmaşık arayüz olmayacak.**

---

## AKADEMİK ÇEVİRİ KURALI

1. **Tüm çeviri işlemleri, metnin akademik ve bilimsel bağlamını, terim bütünlüğünü ve teknik üslubunu koruyacak şekilde yapılacak. Kullanılan çeviri API'sine veya LLM'e mümkünse "akademik çeviri" (academic translation) veya "formal/scientific style" parametresi ya da promptu iletilecek. Promptlarda "akademik makale üslubunda, terimlerin ve cümlelerin bütünlüğünü koruyarak çevir" ifadesi açıkça belirtilecek.**

---

## KLASÖR YÖNETİMİ ve KULLANICI YÖNLENDİRMESİ (Yalnızca Windows)

1. **Uygulama başlatıldığında kullanıcıya, kendi kullanıcı klasöründe (örn. `C:\Users\KULLANICI_ADI\`) "upload" ve "result" adlı iki klasör oluşturması gerektiği ekranda açıklanacak.**
2. **Her iki klasörün tam yolu arayüzde otomatik olarak gösterilecek ve yanında "kopyala" butonları olacak.**
3. **Kullanıcı, klasörleri oluşturduktan sonra "Klasörleri Oluşturdum" butonuna tıklayacak. Uygulama, bu iki klasörün var olup olmadığını kontrol edecek.**
4. **Klasörler yoksa işleme izin verilmeyecek, kullanıcıya net uyarı verilecek. Klasörler mevcutsa "Yükle" ve "Çevir" adımları aktif olacak.**
5. **"Yükle" butonuna basınca dosya seçme ekranı açılacak. Seçilen PDF dosyası, otomatik olarak "upload" klasörüne kopyalanacak.**
6. **Başarılı kopyalama sonrası kullanıcıya onay mesajı ve dosya yolu gösterilecek.**
7. **Çeviri işlemi sadece "upload" klasöründeki dosya için başlayacak ve çıktı dosyası doğrudan "result" klasörüne kaydedilecek. Sonuç klasörü ve dosya adı ekranda açıkça gösterilecek.**
8. **Kullanıcıya, tüm klasör yolları ve isimleri her adımda kopyala butonları ile sunulacak.**
9. **"Sonuç klasörünü aç" butonu olacak; sonuç dosyası bu klasörde yer alacak.**
10. **Not: Uygulama yalnızca Windows işletim sistemi için geliştirilmiştir. Tüm yollar ve işlemler Windows’a özgü olacak.**

---

## DOSYA YÖNETİMİ ve İSİMLENDİRME

1. **Yalnızca tek dosya işlenecek. Çoklu dosya desteği olmayacak.**
2. **Çeviri tamamlandığında, "upload" klasörü otomatik olarak temizlenecek (içindeki dosya silinecek).**
3. **Aynı isimde bir çıktı dosyası varsa otomatik olarak "(1)", "(2)" gibi eklemelerle isimlendirme yapılacak.**
4. **Çıktı dosyası adı: "\[orijinal\_dosya\_adı]\_TR.pdf" formatında olacak.**
5. **Varsayılan kaydetme yeri: `C:\Users\KULLANICI_ADI\result\` klasörü.**

---

## PDF OKUMA/KORUMA DURUMLARI

1. **PDF metni kopya korumalı/parolalıysa ya da okunamıyorsa, kullanıcıya konuyla ilgili bilgilendirici ve net bir mesaj gösterilecek.**
2. **PDF yükleme yalnızca “Yükle” butonundan yapılacak; kullanıcı upload klasörüne doğrudan dosya ekleyemez.**
3. **Sadece PDF dosyası seçilebilir. Yanlış dosya seçilirse uyarı gösterilecek.**

---

## ARAYÜZ VE GERİ BİLDİRİM

1. **Tüm hata, uyarı ve bilgilendirme mesajları arayüzde sabit bir mesaj kutusu alanında gösterilecek; pop-up veya geçici bildirimler kullanılmayacak.**
2. **Progress bar veya loading bar çeviri sürecinde canlı olarak ilerleme gösterecek.**

---

## ÇEVİRİ SERVİSİ: GOOGLE GEMINI 2.5 FLASH

1. **Google Gemini 2.5 Flash API kullanılacak.**
2. **API anahtarı kodda local bir config dosyasında (`config.py` veya `.env` gibi) saklanacak.**

   * **Kullanıcıdan anahtar alınmayacak; arayüzde bu konuda hiçbir alan, uyarı veya buton bulunmayacak.**
   * **Uygulama anahtarı otomatik olarak local config’den okuyacak.**
3. **Gemini 2.5 Flash'ın "thinking capabilities" özelliği akademik çeviri için prompta yansıtılacak.**
4. **Çeviri promptu:**
   `"Bu metni akademik makale üslubunda, bilimsel terimlerin ve cümlelerin bütünlüğünü koruyarak İngilizce'den Türkçe'ye çevir. Akademik terminolojiyi koru, formal üslup kullan ve thinking process ile bağlamı değerlendir."`
5. **Asenkron, thread pool veya paralel API isteği yapılmayacak.**

   * **Tüm çeviri istekleri sırayla ve tek tek yapılacak (batch sequential).**
   * **Paralel veya eş zamanlı çeviri yok.**

---

## DOSYA SINIRLARI

1. **Maksimum PDF boyutu: 50 MB**
2. **Maksimum sayfa sayısı: 300 sayfa**
3. **Bu sınırlar aşılırsa kullanıcıya net bir uyarı mesajı gösterilecek.**

---

## HATA YÖNETİMİ

1. **PDF okunamıyorsa veya hasarlıysa kullanıcıya net mesaj gösterilecek.**
2. **Gemini API hatalarında yeniden deneme mekanizması olacak (3 deneme).**
3. **İnternet bağlantısı kesilirse uygun hata mesajı gösterilecek.**
4. **Desteklenmeyen PDF formatı için alternatif çözüm önerilecek.**
5. **Gemini API günlük limit aşılırsa bilgilendirme mesajı olacak.**

---

## TEKNİK GEREKSİNİMLER ve KURULUM

1. **Python 3.8+**
2. **Kütüphaneler: streamlit, PyPDF2 veya pdfplumber, reportlab, google-generativeai**
3. **requirements.txt dosyası oluşturulacak.**
4. **Kurulum tek komutla olacak: `pip install -r requirements.txt`**
5. **Gemini API anahtarı local config dosyasında olacak (Google AI Studio’dan alınacak).**

---

## PERFORMANS OPTİMİZASYONU

1. **Büyük PDF’ler için sayfa sayfa işleme yapılacak.**
2. **Memory usage optimize edilecek.**
3. **Çeviri işlemi için async/thread pool kullanılmayacak; sırayla işlenecek.**
4. **Progress bar gerçek zamanlı gösterilecek.**
5. **Paragraph bazında chunking ile optimal istek kullanımı olacak.**

---

## PROJE YAPISI

```
pdf_translator/
├── app.py                 # Ana uygulama dosyası
├── requirements.txt       # Gerekli kütüphaneler
├── config.py or .env      # API anahtarı (local, kod içinde ayarlanacak)
├── README.md              # Kurulum ve kullanım kılavuzu
├── utils/
│   ├── pdf_processor.py   # PDF işleme fonksiyonları
│   ├── gemini_translator.py  # Gemini 2.5 Flash çeviri fonksiyonları
│   └── file_manager.py    # Dosya yönetimi
└── static/
    └── style.css          # Basit CSS (isteğe bağlı)
```

---

## ARAYÜZ KULLANICI DENEYİMİ KURALI

* **Arayüz, kullanıcı deneyimi açısından kolay, anlaşılır, verimli, hızlı ve akıcı olmalı.**
* **Tüm işlemler birkaç adımda, minimum tıklama ile tamamlanmalı.**
* **Tarayıcıda görüntüleme ve kullanım sırasında hiçbir uyumluluk veya responsive sorunu olmamalı.**
* **Mobil, tablet ve masaüstü gibi farklı tarayıcı ve çözünürlüklerde de kullanılabilir olmalı (responsive).**
* **Arayüzde gereksiz metin, karmaşa, bilgi ve renk olmamalı; sade ve minimal tasarım tercih edilmeli.**
* **Butonlar, ikonlar ve uyarılar açık, anlaşılır ve kolay erişilebilir olmalı.**
* **Uzun işlem süresi olacaksa kullanıcıyı bilgilendiren net mesajlar ve akıcı loading bar bulunmalı.**
* **Kullanıcı için ek bir eğitim veya rehbere gerek bırakmayan, “ilk kez kullanan” için bile sezgisel bir deneyim sağlanmalı.**