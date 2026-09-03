# OProject Windows 一键配置与启动脚本
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendRoot = Join-Path $ProjectRoot 'backend'
$FrontendRoot = Join-Path $ProjectRoot 'frontend'
$VenvRoot = Join-Path $ProjectRoot '.venv'
$PythonExe = Join-Path $VenvRoot 'Scripts\python.exe'

Set-Location $ProjectRoot
Write-Host '=== OProject setup and startup ===' -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python was not found. Install Python 3.10+ and enable Add Python to PATH.'
}
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw 'npm was not found. Install Node.js 18+.'
}

if (-not (Test-Path $PythonExe)) {
    Write-Host '[1/6] Creating Python virtual environment...' -ForegroundColor Yellow
    $hasPython310 = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3.10 -c "import sys; print(sys.version)" *> $null
        $hasPython310 = ($LASTEXITCODE -eq 0)
    }
    if ($hasPython310) {
        & py -3.10 -m venv $VenvRoot
    } else {
        & python -m venv $VenvRoot
    }
}

if (-not (Test-Path '.env')) {
    Write-Host '[2/6] Creating .env configuration...' -ForegroundColor Yellow
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example. Edit it if your database password differs.' -ForegroundColor DarkYellow
}

Write-Host '[3/6] Installing backend dependencies...' -ForegroundColor Yellow
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -r (Join-Path $BackendRoot 'requirements.txt')

Write-Host '[4/6] Installing frontend dependencies...' -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $FrontendRoot 'node_modules'))) {
    Push-Location $FrontendRoot
    try { & npm ci } finally { Pop-Location }
}

Write-Host '[5/6] Running database migrations and initialization...' -ForegroundColor Yellow
Push-Location $BackendRoot
try {
    & $PythonExe manage.py migrate --noinput
    & $PythonExe manage.py init_system
} finally { Pop-Location }

Write-Host '[6/6] Starting backend and frontend...' -ForegroundColor Yellow
$BackendCommand = "& '$PythonExe' manage.py runserver 127.0.0.1:8000"
Start-Process powershell.exe -WorkingDirectory $BackendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $BackendCommand)

$FrontendCommand = 'npm run serve -- --host 127.0.0.1'
Start-Process powershell.exe -WorkingDirectory $FrontendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $FrontendCommand)

Write-Host ''
Write-Host 'Startup complete:' -ForegroundColor Green
Write-Host 'Frontend: http://127.0.0.1:8080/'
Write-Host 'Admin:    http://127.0.0.1:8000/admin/'
Write-Host 'To create an administrator, run: python manage.py createsuperuser'
Read-Host 'Press Enter to close this setup window'
