; PDF Çeviri Uygulaması - Inno Setup Script
; Bu script, uygulamanın .exe ve gerekli tüm dosyalarını kurar, masaüstü ve başlat menüsüne kısayol ekler.

[Setup]
AppName=PDF Çeviri Uygulaması
AppVersion=1.0
DefaultDirName={pf}\PDFCeviri
DefaultGroupName=PDF Çeviri Uygulaması
OutputDir=.
OutputBaseFilename=Kurulum
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "static\*"; DestDir: "{app}\static"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
Name: "{group}\PDF Çeviri Uygulaması"; Filename: "{app}\app.exe"
Name: "{userdesktop}\PDF Çeviri Uygulaması"; Filename: "{app}\app.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Masaüstü simgesi oluştur"; GroupDescription: "Ekstra Görevler:"

[Run]
Filename: "{app}\app.exe"; Description: "PDF Çeviri Uygulamasını Başlat"; Flags: nowait postinstall skipifsilent 