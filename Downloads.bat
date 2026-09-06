@echo off
python -c "exit()" >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

pip install pyautogui psutil --quiet

powershell -Command "Invoke-WebRequest 'https://www.rarlab.com/rar/winrar-x64-621.exe' -OutFile 'C:\Users\Public\Desktop\Winrar-setup.exe'"
C:\Users\Public\Desktop\Winrar-setup.exe /S
del C:\Users\Public\Desktop\Winrar-setup.exe

powershell -Command "Invoke-WebRequest 'https://github.com/chieunhatnang/VM-QuickConfig/releases/download/1.6.1/VMQuickConfig.exe' -OutFile 'C:\Users\Public\Desktop\VMQuickConfig.exe'"

powershell -Command "Invoke-WebRequest 'https://download.anydesk.com/AnyDesk.exe' -OutFile 'C:\Users\Public\Desktop\AnyDesk.exe'"
"C:\Users\Public\Desktop\AnyDesk.exe" --install "C:\Program Files (x86)\AnyDesk" --start-with-win --silent

del /q "C:\Users\Public\Desktop\Epic Games Launcher.lnk" >nul 2>&1
del /q "C:\Users\Public\Desktop\Unity Hub.lnk" >nul 2>&1

set "password=nk0ckhun9"
powershell -Command "Import-Module Microsoft.PowerShell.Security; Set-LocalUser -Name 'runneradmin' -Password (ConvertTo-SecureString -AsPlainText '%password%' -Force)"

reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d 0 /f

tzutil /s "Sri Lanka Standard Time"

echo Script execution completed.
