@echo off
setlocal

set "JSONFILE=%TEMP%\public_ip.json"
if exist "%JSONFILE%" del "%JSONFILE%" >nul 2>&1

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command " $ip = Invoke-RestMethod 'https://api.ipify.org'; @{ip=$ip} | ConvertTo-Json | Out-File '%JSONFILE%' -Encoding UTF8 "

if exist "%JSONFILE%" (
    echo Public IP JSON:
    type "%JSONFILE%"
) else (
    echo Failed to retrieve public IP.
)

endlocal
