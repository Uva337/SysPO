@echo off
REM Build optimized Windows executable using PyInstaller
setlocal
set CLEAN=0
for %%A in (%*) do (
    REM pass --clean to remove previous builds
    if "%%A"=="--clean" set CLEAN=1
)
cd /d "%~dp0\..\.."
if %CLEAN%==1 (
    rmdir /S /Q dist 2>nul
    rmdir /S /Q build\windows 2>nul
)
where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PyInstaller is not installed. Run "pip install pyinstaller".
    exit /b 1
)
python icon.py
if exist icon.ico copy /Y icon.ico packaging\windows\icon.ico >nul
pip install -r requirements.txt || exit /b 1
pyinstaller packaging\windows\SysAdmin.spec --distpath dist\SysAdminAssistant-win --workpath build\windows --clean
if errorlevel 1 exit /b 1
echo Build finished. Files available in dist\SysAdminAssistant-win
endlocal
