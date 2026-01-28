@echo off
echo Building Wisadel.exe...
cd /d %~dp0
pyinstaller --onefile --windowed --name Wisadel main.py
echo Done! Check dist\Wisadel.exe
pause
