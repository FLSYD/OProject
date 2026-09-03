# OProject Windows 一键配置与启动脚本
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendRoot = Join-Path $ProjectRoot 'backend'
$FrontendRoot = Join-Path $ProjectRoot 'frontend'
$VenvRoot = Join-Path $ProjectRoot '.venv'
$PythonExe = Join-Path $VenvRoot 'Scripts\python.exe'

Set-Location $ProjectRoot
Write-Host '=== OProject 一键配置与启动 ===' -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw '未找到 Python。请先安装 Python 3.10+，并勾选 Add Python to PATH。'
}
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw '未找到 npm。请先安装 Node.js 18+。'
}

if (-not (Test-Path $PythonExe)) {
    Write-Host '[1/6] 创建 Python 虚拟环境...' -ForegroundColor Yellow
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
    Write-Host '[2/6] 创建 .env 配置文件...' -ForegroundColor Yellow
    Copy-Item '.env.example' '.env'
    Write-Host '已从 .env.example 创建 .env；如数据库密码不同，请先编辑 .env。' -ForegroundColor DarkYellow
}

Write-Host '[3/6] 安装后端依赖...' -ForegroundColor Yellow
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -r (Join-Path $BackendRoot 'requirements.txt')

Write-Host '[4/6] 安装前端依赖...' -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $FrontendRoot 'node_modules'))) {
    Push-Location $FrontendRoot
    try { & npm ci } finally { Pop-Location }
}

Write-Host '[5/6] 执行数据库迁移和系统初始化...' -ForegroundColor Yellow
Push-Location $BackendRoot
try {
    & $PythonExe manage.py migrate --noinput
    & $PythonExe manage.py init_system
} finally { Pop-Location }

Write-Host '[6/6] 启动后端和前端...' -ForegroundColor Yellow
$BackendCommand = "& '$PythonExe' manage.py runserver 127.0.0.1:8000"
Start-Process powershell.exe -WorkingDirectory $BackendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $BackendCommand)

$FrontendCommand = 'npm run serve -- --host 127.0.0.1'
Start-Process powershell.exe -WorkingDirectory $FrontendRoot -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $FrontendCommand)

Write-Host ''
Write-Host '启动完成：' -ForegroundColor Green
Write-Host '前端：http://127.0.0.1:8080/'
Write-Host '后台：http://127.0.0.1:8000/admin/'
Write-Host '如需创建管理员，请在 backend 窗口执行：python manage.py createsuperuser'
Read-Host '按 Enter 关闭此配置窗口'
