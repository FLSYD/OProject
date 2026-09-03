# OProject Windows one-click setup and startup script
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendRoot = Join-Path $ProjectRoot 'backend'
$FrontendRoot = Join-Path $ProjectRoot 'frontend'
$VenvRoot = Join-Path $ProjectRoot '.venv'
$PythonExe = Join-Path $VenvRoot 'Scripts\python.exe'
$BackendRequirements = Join-Path $BackendRoot 'requirements.txt'
$DependencyStamp = Join-Path $VenvRoot '.oproject-requirements-installed'
$FrontendLock = Join-Path $FrontendRoot 'package-lock.json'
$FrontendStamp = Join-Path $FrontendRoot 'node_modules\.oproject-lock-installed'

Set-Location $ProjectRoot
Write-Host '=== OProject one-click setup and startup ===' -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python was not found. Install Python 3.10+ and enable Add Python to PATH.'
}
if (-not (Test-Path $PythonExe)) {
    Write-Host '[1/7] Creating Python virtual environment...' -ForegroundColor Yellow
    $hasPython310 = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3.10 -c "import sys; print(sys.version)" *> $null
        $hasPython310 = ($LASTEXITCODE -eq 0)
    }
    if ($hasPython310) { & py -3.10 -m venv $VenvRoot } else { & python -m venv $VenvRoot }
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw 'npm was not found. Install Node.js 18+.'
}

if (-not (Test-Path '.env')) {
    Write-Host '[2/7] Creating .env configuration...' -ForegroundColor Yellow
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example. Edit it if your database settings differ.' -ForegroundColor DarkYellow
}

$requirementsHash = (Get-FileHash $BackendRequirements -Algorithm SHA256).Hash
if (-not (Test-Path $DependencyStamp) -or ((Get-Content $DependencyStamp -Raw).Trim() -ne $requirementsHash)) {
    Write-Host '[3/7] Installing backend dependencies...' -ForegroundColor Yellow
    & $PythonExe -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw 'Backend dependency installation failed.' }
    & $PythonExe -m pip install -r $BackendRequirements
    if ($LASTEXITCODE -ne 0) { throw 'Backend dependency installation failed.' }
    Set-Content -Path $DependencyStamp -Value $requirementsHash -NoNewline
} else {
    Write-Host '[3/7] Backend dependencies are up to date.' -ForegroundColor DarkGray
}

 $frontendHash = (Get-FileHash $FrontendLock -Algorithm SHA256).Hash
if (-not (Test-Path (Join-Path $FrontendRoot 'node_modules')) -or -not (Test-Path $FrontendStamp) -or ((Get-Content $FrontendStamp -Raw).Trim() -ne $frontendHash)) {
    Write-Host '[4/7] Installing frontend dependencies...' -ForegroundColor Yellow
    Push-Location $FrontendRoot
    try { & npm ci } finally { Pop-Location }
    if ($LASTEXITCODE -ne 0) { throw 'Frontend dependency installation failed.' }
    Set-Content -Path $FrontendStamp -Value $frontendHash -NoNewline
} else {
    Write-Host '[4/7] Frontend dependencies already exist.' -ForegroundColor DarkGray
}

Write-Host '[5/7] Running database migrations and system initialization...' -ForegroundColor Yellow
Push-Location $BackendRoot
try {
    & $PythonExe manage.py migrate --noinput
    if ($LASTEXITCODE -ne 0) { throw 'Database migration failed. Check .env and MySQL.' }
    & $PythonExe manage.py init_system
    if ($LASTEXITCODE -ne 0) { throw 'System initialization failed.' }
} finally { Pop-Location }

Write-Host '[6/7] Creating one-click administrator...' -ForegroundColor Yellow
Push-Location $BackendRoot
try { & $PythonExe manage.py setup_admin } finally { Pop-Location }

Write-Host '[7/7] Starting backend and frontend...' -ForegroundColor Yellow
$BackendCommand = "& '$PythonExe' manage.py runserver 127.0.0.1:8000"
Start-Process powershell.exe -WorkingDirectory $BackendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $BackendCommand)
$FrontendCommand = 'npm run serve -- --host 127.0.0.1'
Start-Process powershell.exe -WorkingDirectory $FrontendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $FrontendCommand)

Write-Host ''
Write-Host 'Startup commands sent.' -ForegroundColor Green
Write-Host 'Frontend: http://127.0.0.1:8080/'
Write-Host 'Admin:    http://127.0.0.1:8000/admin/'
Write-Host 'Admin username: admin'
Write-Host 'Admin password: Admin@123456'
