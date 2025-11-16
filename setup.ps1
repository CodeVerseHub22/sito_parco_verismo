# =============================================================================
# SCRIPT SETUP AUTOMATICO - Parco Letterario Verismo (PowerShell)
# =============================================================================
# Questo script prepara l'ambiente di sviluppo su Windows.

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

function Write-Step($message) { Write-Host $message -ForegroundColor Yellow }
function Write-Ok($message) { Write-Host $message -ForegroundColor Green }
function Write-Err($message) { Write-Host $message -ForegroundColor Red }

Write-Host "Parco Letterario Verismo - Setup automatico" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------------------------------------------
# Prerequisiti
# ---------------------------------------------------------------------------
Write-Step "Verifico prerequisiti..."

function Get-PythonLauncher {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @{ Command = "py"; Args = @("-3") }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @{ Command = "python"; Args = @() }
    }
    throw "[ERRORE] Python 3 non trovato. Installalo e riprova."
}

$pythonLauncher = Get-PythonLauncher
$pythonVersion = & $pythonLauncher.Command @($pythonLauncher.Args + @("--version"))
Write-Ok "[OK] Python trovato: $pythonVersion"

try {
    $nodeVersion = node --version
    Write-Ok "[OK] Node.js trovato: $nodeVersion"
} catch {
    Write-Err "[ERRORE] Node.js non trovato. Installalo e riprova."
    exit 1
}

try {
    $npmVersion = npm --version
    Write-Ok "[OK] npm trovato: v$npmVersion"
} catch {
    Write-Err "[ERRORE] npm non trovato. Installalo e riprova."
    exit 1
}

Write-Host ""

$venvPath = ".venv"
$venvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"

# ---------------------------------------------------------------------------
# 1. Virtual environment
# ---------------------------------------------------------------------------
Write-Step "[1/5] Creo/aggiorno il virtual environment..."
if (-not (Test-Path $venvPath)) {
    & $pythonLauncher.Command @($pythonLauncher.Args + @("-m", "venv", $venvPath))
    Write-Ok "[OK] Virtual environment creato in $venvPath"
} else {
    Write-Ok "[OK] Virtual environment già presente"
}

# ---------------------------------------------------------------------------
# 2. Dipendenze Python
# ---------------------------------------------------------------------------
Write-Step "[2/5] Installo dipendenze Python..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt
Write-Ok "[OK] Dipendenze Python installate"

# ---------------------------------------------------------------------------
# 3. Dipendenze npm
# ---------------------------------------------------------------------------
Write-Step "[3/5] Installo dipendenze npm..."
if (Test-Path "package-lock.json") {
    npm ci
} else {
    npm install
}
Write-Ok "[OK] Dipendenze npm installate"

# ---------------------------------------------------------------------------
# 4. Asset frontend
# ---------------------------------------------------------------------------
Write-Step "[4/5] Copio asset frontend in locale..."
npm run setup
Write-Ok "[OK] Asset frontend copiati tramite scripts/setup-assets.js"

# ---------------------------------------------------------------------------
# 5. Database
# ---------------------------------------------------------------------------
Write-Step "[5/5] Eseguo migrazioni Django..."
& $venvPython manage.py migrate
Write-Ok "[OK] Database aggiornato"

# ---------------------------------------------------------------------------
# Riepilogo
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Ok "SETUP COMPLETATO CON SUCCESSO"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Step "Prossimi passi:"
Write-Host "  1. Attiva il virtual environment:"
Write-Host "     .\.venv\Scripts\Activate.ps1    (PowerShell)"
Write-Host "     .venv\Scripts\activate.bat      (CMD)"
Write-Host ""
Write-Host "  2. Crea un superuser (se serve):"
Write-Host "     .\.venv\Scripts\python.exe manage.py createsuperuser"
Write-Host ""
Write-Host "  3. Avvia il server di sviluppo:"
Write-Host "     .\.venv\Scripts\python.exe manage.py runserver"
Write-Host ""
Write-Host "  4. Apri http://127.0.0.1:8000/ nel browser"
Write-Host ""
Write-Host "Per l'admin: http://127.0.0.1:8000/admin/"
Write-Host ""
