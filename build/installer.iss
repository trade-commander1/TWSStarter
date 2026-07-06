; TWSStarter — Inno Setup Script
; Builds a Windows installer from the PyInstaller output.
; Requires Inno Setup 6+ (https://jrsoftware.org/isinfo.php)
; Run after build_windows.bat
;
; Version / Build are normally passed in by build_windows.bat:
;   ISCC /DAppVersion=1.1 /DAppBuild=0 installer.iss
; The defaults below are fallbacks and must be kept in sync with
; src/twsstarter/version.py.

#ifndef AppVersion
  #define AppVersion "1.2"
#endif
#ifndef AppBuild
  #define AppBuild "0"
#endif

#define AppName      "TWSStarter"
#define AppFullVer   AppVersion + "." + AppBuild
#define AppPublisher "trade-commander.de"
#define AppURL       "https://trade-commander.de"
#define AppExeName   "TWSStarter.exe"
#define DistDir      "..\dist"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppFullVer}
AppVerName={#AppName} v{#AppVersion} Build {#AppBuild}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=installer_output
OutputBaseFilename=TWSStarter-{#AppFullVer}-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#AppExeName}
SetupIconFile=TWSStarter.ico
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german";  MessagesFile: "compiler:Languages\German.isl"
Name: "french";  MessagesFile: "compiler:Languages\French.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "polish";  MessagesFile: "compiler:Languages\Polish.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#DistDir}\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}";            Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}";      Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
