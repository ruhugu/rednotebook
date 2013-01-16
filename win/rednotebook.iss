; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{82A7E9C3-D3F3-4B85-9AC3-D0E011D19E50}
AppName=RedNotebook
AppVerName=RedNotebook 1.6.6
; AppPublisher=Jendrik Seipp
AppPublisherURL=http://rednotebook.sourceforge.net
AppSupportURL=http://rednotebook.sourceforge.net
AppUpdatesURL=http://rednotebook.sourceforge.net
DefaultDirName={pf}\RedNotebook
DefaultGroupName=RedNotebook
AllowNoIcons=yes
OutputDir=C:\Users\Jendrik\Dropbox\Public
OutputBaseFilename=rednotebook-1.6.6-beta1
SetupIconFile=rednotebook.ico
Compression=lzma2
SolidCompression=yes
;DisableWelcomePage=yes

; Show the language selector, if the default language can't be automatically found
ShowLanguageDialog=auto


; We have to include the language files. The found language will be automatically shown
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

;Name: "basque"; MessagesFile: "compiler:Languages\Basque.isl"
Name: "bp"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
;Name: "slovak"; MessagesFile: "compiler:Languages\Slovak.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"

;[Types]
;Name: "normal"; Description: "Standard installation"
;Name: "portable"; Description: "Portable installation"

;[Components]
;Name: "everything"; Description: "Program Files"; Types: normal; Flags: fixed
;Name: "portablecfgfile"; Description: "Config File"; Types: portable

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked;
;Components: everything
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked;
;Components: everything;

;Startup
name: "startupicon"; Description: "Run RedNotebook on Startup"; GroupDescription: "Additional tasks:"; MinVersion: 4,4; Flags: unchecked;

[Files]
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "dist\*"; Excludes: "*.log,*.a,*.def,*.h,*.lib,*.pc,Thumbs.db,*.aff,*.dic"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: "portable.cfg"; DestDir: "{app}\files"; DestName: "default.cfg"; Flags: ignoreversion; Components: portablecfgfile

[Icons]
Name: "{group}\RedNotebook"; Filename: "{app}\rednotebook.exe";
;Components: everything;
Name: "{group}\{cm:UninstallProgram,RedNotebook}"; Filename: "{uninstallexe}";
;Components: everything;
Name: "{commondesktop}\RedNotebook"; Filename: "{app}\rednotebook.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\RedNotebook"; Filename: "{app}\rednotebook.exe"; Tasks: quicklaunchicon

;Startup
Name: "{userstartup}\RedNotebook"; Filename: "{app}\rednotebook.exe"; Tasks: startupicon; workingdir: "{app}"


[Run]
Filename: "{app}\rednotebook.exe"; Description: "{cm:LaunchProgram,RedNotebook}"; Flags: nowait postinstall skipifsilent


