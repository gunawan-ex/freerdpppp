@echo off
echo Runner aktif. Menjaga sesi tetap menyala...
:loop
ping -n 61 127.0.0.1 >nul
goto loop
