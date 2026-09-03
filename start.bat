@echo off
chcp 65001 >nul
PowerShell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1"
if errorlevel 1 (
    echo Setup failed. Read the message above and fix the configuration.
    pause
)
