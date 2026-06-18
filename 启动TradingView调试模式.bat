@echo off
title Launch TradingView Debug Mode

echo Closing existing TradingView...
taskkill /F /IM TradingView.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo Starting TradingView with debug port 9222...
powershell -Command "Start-Process 'C:\Program Files\WindowsApps\TradingView.Desktop_3.2.0.7916_x64__n534cwy3pjxzj\TradingView.exe' -ArgumentList '--remote-debugging-port=9222','--remote-allow-origins=*'"

echo Waiting for TradingView to load (8 seconds)...
timeout /t 8 /nobreak >nul

powershell -Command "try { $r = Invoke-WebRequest 'http://localhost:9222/json/version' -TimeoutSec 3 -UseBasicParsing; Write-Host '[OK] CDP ready - Claude can connect to TradingView!' } catch { Write-Host '[Info] TradingView still loading, close this window and Claude is ready to use.' }"
echo.
pause
