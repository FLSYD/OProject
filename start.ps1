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

function Get-AvailablePort {
    param([int]$PreferredPort)
    foreach ($port in $PreferredPort..($PreferredPort + 50)) {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $port)
        try {
            $listener.Start()
            return $port
        } catch {
            continue
        } finally {
            $listener.Stop()
        }
    }
    throw "No available port found near $PreferredPort."
}

function Assert-PortAvailable {
    param([int]$Port)
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
    try {
        $listener.Start()
    } catch {
        throw "Frontend port $Port is occupied. Stop the existing Vue/IIS service using port $Port, then run start.bat again."
    } finally {
        $listener.Stop()
    }
}

function Wait-ForUrl {
    param([string]$Url, [int]$TimeoutSeconds = 90)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 3
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { return }
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }
    throw "Service did not become ready: $Url"
}

Set-Location $ProjectRoot
Write-Host '=== OProject one-click setup and startup ===' -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python was not found. Install Python 3.10+ and enable Add Python to PATH.'
}
if (-not (Test-Path $PythonExe)) {
    Write-Host '[1/8] Creating Python virtual environment...' -ForegroundColor Yellow
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
    Write-Host '[2/8] Creating .env configuration...' -ForegroundColor Yellow
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example. Edit it if your database settings differ.' -ForegroundColor DarkYellow
}

$requirementsHash = (Get-FileHash $BackendRequirements -Algorithm SHA256).Hash
if (-not (Test-Path $DependencyStamp) -or ((Get-Content $DependencyStamp -Raw).Trim() -ne $requirementsHash)) {
    Write-Host '[3/8] Installing backend dependencies...' -ForegroundColor Yellow
    & $PythonExe -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw 'Backend dependency installation failed.' }
    & $PythonExe -m pip install -r $BackendRequirements
    if ($LASTEXITCODE -ne 0) { throw 'Backend dependency installation failed.' }
    Set-Content -Path $DependencyStamp -Value $requirementsHash -NoNewline
} else {
    Write-Host '[3/8] Backend dependencies are up to date.' -ForegroundColor DarkGray
}

$frontendHash = (Get-FileHash $FrontendLock -Algorithm SHA256).Hash
if (-not (Test-Path (Join-Path $FrontendRoot 'node_modules')) -or -not (Test-Path $FrontendStamp) -or ((Get-Content $FrontendStamp -Raw).Trim() -ne $frontendHash)) {
    Write-Host '[4/8] Installing frontend dependencies...' -ForegroundColor Yellow
    Push-Location $FrontendRoot
    try { & npm ci } finally { Pop-Location }
    if ($LASTEXITCODE -ne 0) { throw 'Frontend dependency installation failed.' }
    Set-Content -Path $FrontendStamp -Value $frontendHash -NoNewline
} else {
    Write-Host '[4/8] Frontend dependencies already exist.' -ForegroundColor DarkGray
}

Write-Host '[5/8] Running database migrations and system initialization...' -ForegroundColor Yellow
Push-Location $BackendRoot
try {
    & $PythonExe manage.py migrate --noinput
    if ($LASTEXITCODE -ne 0) { throw 'Database migration failed. Check .env and MySQL.' }
    & $PythonExe manage.py init_system
    if ($LASTEXITCODE -ne 0) { throw 'System initialization failed.' }
} finally { Pop-Location }

Write-Host '[6/8] Creating one-click administrator...' -ForegroundColor Yellow
Push-Location $BackendRoot
try { & $PythonExe manage.py setup_admin } finally { Pop-Location }
if ($LASTEXITCODE -ne 0) { throw 'Administrator setup failed.' }

Write-Host '[7/8] Checking ports and starting services...' -ForegroundColor Yellow
$BackendPort = Get-AvailablePort -PreferredPort 8000
$FrontendPort = 8080
Assert-PortAvailable -Port $FrontendPort
$BackendBaseUrl = "http://127.0.0.1:$BackendPort"
$FrontendBaseUrl = "http://127.0.0.1:$FrontendPort"
$BackendCommand = "& '$PythonExe' manage.py runserver 127.0.0.1:$BackendPort"
Start-Process powershell.exe -WorkingDirectory $BackendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $BackendCommand)
$FrontendCommand = "`$env:VUE_APP_API_TARGET='$BackendBaseUrl'; npm run serve -- --host 127.0.0.1 --port $FrontendPort"
Start-Process powershell.exe -WorkingDirectory $FrontendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $FrontendCommand)

Write-Host '[8/8] Waiting for services and verifying login...' -ForegroundColor Yellow
Wait-ForUrl -Url "$BackendBaseUrl/api/health/"
Wait-ForUrl -Url $FrontendBaseUrl -TimeoutSeconds 120
$loginBody = @{ username = 'admin'; password = 'Admin@123456' } | ConvertTo-Json
try {
    Invoke-RestMethod -Uri "$FrontendBaseUrl/api/login/" -Method Post -ContentType 'application/json' -Body $loginBody | Out-Null
} catch {
    throw "Frontend-to-backend login verification failed: $($_.Exception.Message)"
}

$FrontendLoginUrl = "$FrontendBaseUrl/#/login"
$AdminLoginUrl = "$BackendBaseUrl/admin/"
Write-Host ''
Write-Host 'All services are ready and login was verified.' -ForegroundColor Green
Write-Host ''
Write-Host 'WEB APPLICATION LOGIN' -ForegroundColor Cyan
Write-Host "URL:      $FrontendLoginUrl"
Write-Host 'Username: admin'
Write-Host 'Password: Admin@123456'
Write-Host ''
Write-Host 'DJANGO ADMIN (same account)' -ForegroundColor Cyan
Write-Host "URL:      $AdminLoginUrl"
Write-Host 'Username: admin'
Write-Host 'Password: Admin@123456'
Start-Process $FrontendLoginUrl
