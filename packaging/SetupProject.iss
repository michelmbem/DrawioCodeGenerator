#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif
#ifndef AppArch
  #define AppArch "x64"
#endif
#ifndef SourcePath
  #define SourcePath "..\dist\DrawioCodeGenerator"
#endif

#define MyAppName "Draw.io Code Generator"
#define MyAppPublisher "Michel Mbem"
#define MyAppURL "https://github.com/michelmbem/DrawioCodeGenerator"
#define MyAppExeName "DrawioCodeGenerator.exe"

[Setup]
AppId={{740EAFC9-45E1-4D11-98BE-8DE9197F1D3A}
AppName={#MyAppName}
AppVersion={#AppVersion}
AppVerName={#MyAppName} {#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=..\dist
OutputBaseFilename=DrawioCodeGenerator-windows-{#AppArch}-setup
SetupIconFile=app-icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "{#SourcePath}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
