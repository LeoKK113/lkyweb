@echo off
cd /d "%~dp0"
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:5173/' -UseBasicParsing -TimeoutSec 3; if ($r.StatusCode -eq 200 -and $r.Content -match 'LI MIN') { exit 0 } } catch {}; exit 1"
if not errorlevel 1 (
  start "" "http://localhost:5173/"
  exit /b 0
)
set "PORTFOLIO_NODE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
if exist "%PORTFOLIO_NODE%" (
  "%PORTFOLIO_NODE%" node_modules\vite\bin\vite.js --host 0.0.0.0 --open
) else (
  node node_modules\vite\bin\vite.js --host 0.0.0.0 --open
)
pause
