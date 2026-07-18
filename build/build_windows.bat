@echo off
:: TWSStarter — Windows build script
:: Requires: uv installed and project dependencies synced.
:: Optional: Inno Setup 6 for building the installer.
:: Output: dist\TWSStarter.exe  and  dist\TWSStarter-X.Y.Z-Setup.exe

setlocal enabledelayedexpansion

cd /d "%~dp0.."

:: ── Read version/build from the single source of truth ──────────────
for /f "tokens=1,2" %%a in ('uv run python -c "import twsstarter.version as v; print(v.VERSION, v.BUILD)"') do (
    set "APP_VERSION=%%a"
    set "APP_BUILD=%%b"
)
echo Building TWSStarter v%APP_VERSION% Build %APP_BUILD%

echo [1/4] Installing PyInstaller ...
uv add --dev pyinstaller

echo [2/4] Building executable ...
uv run pyinstaller --clean --noconfirm build\TWSStarter.spec
if not exist dist\TWSStarter.exe (
    echo  ERROR: Build failed -- dist\TWSStarter.exe not found.
    exit /b 1
)

echo [3/4] Locating Inno Setup ...
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe"      set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if not defined ISCC (
    echo  Inno Setup not found -- skipping installer.
    echo  Output: dist\TWSStarter.exe
    goto :done
)

echo [4/4] Building installer ...
"%ISCC%" /DAppVersion=%APP_VERSION% /DAppBuild=%APP_BUILD% build\installer.iss
if errorlevel 1 (
    echo  ERROR: Installer build failed.
    exit /b 1
)

echo.
echo  Output: dist\TWSStarter.exe
echo  Output: dist\TWSStarter-%APP_VERSION%.%APP_BUILD%-Setup.exe

:done
endlocal
