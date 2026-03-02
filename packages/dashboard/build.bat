@echo off
echo Building Dashboard.exe...
cd /d %~dp0
pyinstaller --noconfirm --clean Dashboard.spec
echo Done! Check dist\Dashboard.exe
pause