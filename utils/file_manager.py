import os
import shutil
import platform
from typing import Tuple, Optional
from pathlib import Path

class FileManager:
    def __init__(self):
        self.system = platform.system()
        if self.system != "Windows":
            raise RuntimeError("Bu uygulama sadece Windows işletim sistemi için geliştirilmiştir.")
        
        # Windows kullanıcı klasörü
        self.user_home = os.path.expanduser("~")
        self.upload_folder = os.path.join(self.user_home, "upload")
        self.result_folder = os.path.join(self.user_home, "result")
    
    def get_folder_paths(self) -> Tuple[str, str]:
        """Upload ve result klasör yollarını döner."""
        return self.upload_folder, self.result_folder
    
    def create_folders(self) -> Tuple[bool, str]:
        """Gerekli klasörleri oluşturur."""
        try:
            # Upload klasörü oluştur
            if not os.path.exists(self.upload_folder):
                os.makedirs(self.upload_folder)
            
            # Result klasörü oluştur
            if not os.path.exists(self.result_folder):
                os.makedirs(self.result_folder)
            
            return True, "Klasörler başarıyla oluşturuldu."
            
        except Exception as e:
            return False, f"Klasör oluşturma hatası: {str(e)}"
    
    def check_folders_exist(self) -> Tuple[bool, str]:
        """Klasörlerin var olup olmadığını kontrol eder."""
        upload_exists = os.path.exists(self.upload_folder)
        result_exists = os.path.exists(self.result_folder)
        
        if upload_exists and result_exists:
            return True, "Klasörler mevcut."
        else:
            missing_folders = []
            if not upload_exists:
                missing_folders.append("upload")
            if not result_exists:
                missing_folders.append("result")
            
            return False, f"Eksik klasörler: {', '.join(missing_folders)}"
    
    def copy_file_to_upload(self, source_path: str) -> Tuple[bool, str, str]:
        """Dosyayı upload klasörüne kopyalar."""
        try:
            if not os.path.exists(source_path):
                return False, "", "Kaynak dosya bulunamadı."
            
            # Dosya adını al
            filename = os.path.basename(source_path)
            destination_path = os.path.join(self.upload_folder, filename)
            
            # Dosyayı kopyala
            shutil.copy2(source_path, destination_path)
            
            return True, destination_path, f"Dosya başarıyla kopyalandı: {destination_path}"
            
        except Exception as e:
            return False, "", f"Dosya kopyalama hatası: {str(e)}"
    
    def get_unique_filename(self, base_filename: str) -> str:
        """Benzersiz dosya adı oluşturur."""
        name, ext = os.path.splitext(base_filename)
        counter = 1
        new_filename = f"{name}_TR{ext}"
        
        while os.path.exists(os.path.join(self.result_folder, new_filename)):
            new_filename = f"{name}_TR({counter}){ext}"
            counter += 1
        
        return new_filename
    
    def save_result_file(self, content: bytes, original_filename: str) -> Tuple[bool, str, str]:
        """Çeviri sonucunu dosyaya kaydeder."""
        try:
            # Benzersiz dosya adı oluştur
            result_filename = self.get_unique_filename(original_filename)
            result_path = os.path.join(self.result_folder, result_filename)
            
            # Dosyayı kaydet
            with open(result_path, 'wb') as f:
                f.write(content)
            
            return True, result_path, f"Sonuç dosyası kaydedildi: {result_path}"
            
        except Exception as e:
            return False, "", f"Dosya kaydetme hatası: {str(e)}"
    
    def clear_upload_folder(self) -> Tuple[bool, str]:
        """Upload klasörünü temizler."""
        try:
            for filename in os.listdir(self.upload_folder):
                file_path = os.path.join(self.upload_folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            return True, "Upload klasörü temizlendi."
            
        except Exception as e:
            return False, f"Klasör temizleme hatası: {str(e)}"
    
    def open_result_folder(self) -> Tuple[bool, str]:
        """Result klasörünü Windows Explorer'da açar."""
        try:
            os.startfile(self.result_folder)
            return True, "Result klasörü açıldı."
            
        except Exception as e:
            return False, f"Klasör açma hatası: {str(e)}"
    
    def get_file_info(self, file_path: str) -> Tuple[bool, dict, str]:
        """Dosya bilgilerini döner."""
        try:
            if not os.path.exists(file_path):
                return False, {}, "Dosya bulunamadı."
            
            stat = os.stat(file_path)
            file_info = {
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'path': file_path,
                'modified': stat.st_mtime
            }
            
            return True, file_info, "Dosya bilgileri alındı."
            
        except Exception as e:
            return False, {}, f"Dosya bilgisi alma hatası: {str(e)}" 