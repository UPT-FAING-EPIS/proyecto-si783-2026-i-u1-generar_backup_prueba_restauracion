[Setup]
AppName=SQL-SafeBridge
AppVersion=1.0
AppPublisher=TuNombre
DefaultDirName={autopf}\SQL-SafeBridge
DefaultGroupName=SQL-SafeBridge
OutputDir=.\Installer
OutputBaseFilename=SQL-SafeBridge_Setup
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\SQL-SafeBridge.exe
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "dist\SQL-SafeBridge\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\SQL-SafeBridge"; Filename: "{app}\SQL-SafeBridge.exe"
Name: "{group}\Desinstalar SQL-SafeBridge"; Filename: "{uninstallexe}"
Name: "{autodesktop}\SQL-SafeBridge"; Filename: "{app}\SQL-SafeBridge.exe"

[Run]
Filename: "{app}\SQL-SafeBridge.exe"; Description: "Iniciar SQL-SafeBridge"; Flags: nowait postinstall skipifsilent