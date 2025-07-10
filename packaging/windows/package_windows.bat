@echo off
REM Package build output into a zip archive
setlocal
cd /d "%~dp0\..\.."
if not exist dist\SysAdminAssistant-win (
    echo [ERROR] Build directory dist\SysAdminAssistant-win not found. Run build_windows.bat first.
    exit /b 1
)
set CLEAN=0
for %%A in (%*) do (
    REM use --clean to delete existing zip
    if "%%A"=="--clean" set CLEAN=1
)
if %CLEAN%==1 del SysAdminAssistant-win.zip 2>nul
powershell -Command "Compress-Archive -Path dist\SysAdminAssistant-win\* -DestinationPath SysAdminAssistant-win.zip -Force"
echo Created SysAdminAssistant-win.zip
endlocal
