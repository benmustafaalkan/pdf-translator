@echo off
chcp 65001 > nul

REM Python yüklü mü kontrol et
python --version > nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo Python zaten yüklü.
    goto install_requirements
)

REM Python yükleyicisini indir
set PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
set PYTHON_INSTALLER=python-installer.exe

echo Python indiriliyor...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"

REM Python'u sessizce kur (Add to PATH ile)
echo Python kuruluyor...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Kurulumdan sonra yükleyiciyi sil
del %PYTHON_INSTALLER%

:install_requirements
REM pip güncelle
python -m pip install --upgrade pip

REM Gerekli paketleri yükle
pip install -r requirements.txt

echo Kurulum tamamlandı!
pause 