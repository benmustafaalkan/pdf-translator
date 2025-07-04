@echo off
chcp 65001 > nul

REM Python yüklü mü kontrol et
python --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python yüklü değil. Lütfen https://www.python.org/downloads/ adresinden Python 3.8 veya üzeri bir sürüm yükleyin.
    pause
    exit /b 1
)

REM pip güncelle
python -m pip install --upgrade pip

REM Gerekli paketleri yükle
pip install -r requirements.txt

echo Kurulum tamamlandı!
pause 