@echo off
REM ============================================================
REM  LindaAI - One-Click Windows Setup & Launcher
REM  Built by Daniel Wise
REM
REM  The customer just DOUBLE-CLICKS this file. It:
REM    1. Installs Node.js + Git (via winget) if missing
REM    2. Installs Claude Code if missing
REM    3. Launches LindaAI right in this folder
REM
REM  A .bat is NOT blocked by PowerShell's execution policy,
REM  so there's nothing for the customer to "allow" or fight.
REM ============================================================

setlocal enabledelayedexpansion
title LindaAI Setup
color 0B
cd /d "%~dp0"

echo.
echo   ============================================
echo      Howdy! Saddling up LindaAI for you...
echo   ============================================
echo.

REM ---------- 0. Make sure winget is available ----------
where winget >nul 2>&1
if errorlevel 1 (
  echo   [!] Windows Package Manager ^(winget^) wasn't found.
  echo       Open the Microsoft Store, search "App Installer", install/update it,
  echo       then double-click this file again.
  echo.
  if /i not "%LINDAAI_CI%"=="1" pause
  exit /b 1
)

REM ---------- 1. Node.js ----------
where node >nul 2>&1
if errorlevel 1 (
  echo   [*] Installing Node.js ^(one-time^)...
  winget install -e --id OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements
) else (
  echo   [ok] Node.js already installed.
)

REM ---------- 2. Git (Claude Code uses it) ----------
where git >nul 2>&1
if errorlevel 1 (
  echo   [*] Installing Git ^(one-time^)...
  winget install -e --id Git.Git --silent --accept-package-agreements --accept-source-agreements
) else (
  echo   [ok] Git already installed.
)

REM ---------- 3. Refresh PATH so freshly-installed tools are visible NOW ----------
REM  (winget updates the registry but not this open window's PATH.)
for /f "tokens=2,*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "MACHINE_PATH=%%b"
for /f "tokens=2,*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"
set "PATH=%MACHINE_PATH%;%USER_PATH%;%PATH%"
REM  npm installs global tools (like 'claude') here — make sure it's reachable now.
set "PATH=%APPDATA%\npm;%PATH%"

REM ---------- 4. Claude Code ----------
where claude >nul 2>&1
if errorlevel 1 (
  echo   [*] Installing Claude Code ^(one-time^)...
  call npm install -g @anthropic-ai/claude-code
) else (
  echo   [ok] Claude Code already installed.
)

REM ---------- 5. Verify claude is reachable ----------
where claude >nul 2>&1
if errorlevel 1 (
  echo.
  echo   [!] Almost there! Windows needs a moment to register the new install.
  echo       Please DOUBLE-CLICK Start-LindaAI.bat one more time to finish.
  echo.
  if /i not "%LINDAAI_CI%"=="1" pause
  exit /b 0
)

REM ---------- 6. Launch LindaAI ----------
echo.
echo   ============================================
echo      LindaAI is ready! Launching now.
echo      First time? Type  /login  to sign in.
echo   ============================================
echo.

REM  In automated tests (LINDAAI_CI=1) skip the interactive launch and just verify.
if /i "%LINDAAI_CI%"=="1" (
  echo   [CI] Verifying Claude Code is callable...
  call claude --version
  echo   [CI] Setup logic completed OK.
  endlocal & exit /b 0
)

call claude

endlocal
