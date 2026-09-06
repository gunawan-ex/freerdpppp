@echo off
echo Runner aktif. Menjaga sesi tetap menyala...
:loop
timeout /t 60 /nobreak >nul
goto loop
