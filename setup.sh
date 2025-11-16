#!/usr/bin/env bash
# =============================================================================
# SCRIPT SETUP AUTOMATICO - Parco Letterario Verismo (Linux/Mac)
# =============================================================================
# Questo script prepara l'ambiente di sviluppo in modo ripetibile.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PROJECT_NAME="Parco Letterario Verismo"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PY="$VENV_DIR/bin/python"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

step() {
    printf "${YELLOW}%s${NC}\n" "$1"
}

success() {
    printf "${GREEN}%s${NC}\n" "$1"
}

error() {
    printf "${RED}%s${NC}\n" "$1"
    exit 1
}

echo "$PROJECT_NAME - Setup automatico"
echo "=================================="
echo ""

# ---------------------------------------------------------------------------
# Verifica prerequisiti
# ---------------------------------------------------------------------------
step "Verifico prerequisiti..."

detect_python() {
    if command -v python3 >/dev/null 2>&1; then
        echo "python3"
    elif command -v python >/dev/null 2>&1; then
        echo "python"
    else
        error "[ERRORE] Python 3 non trovato. Installalo e riprova."
    fi
}

PYTHON_CMD="$(detect_python)"
success "[OK] Python trovato: $($PYTHON_CMD --version 2>&1)"

command -v node >/dev/null 2>&1 || error "[ERRORE] Node.js non trovato. Installalo e riprova."
success "[OK] Node.js trovato: $(node --version)"

command -v npm >/dev/null 2>&1 || error "[ERRORE] npm non trovato. Installalo e riprova."
success "[OK] npm trovato: $(npm --version)"

echo ""

# ---------------------------------------------------------------------------
# 1. Virtual environment Python
# ---------------------------------------------------------------------------
step "[1/5] Creo/aggiorno il virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv "$VENV_DIR"
    success "[OK] Virtual environment creato in $VENV_DIR"
else
    success "[OK] Virtual environment già presente"
fi

# ---------------------------------------------------------------------------
# 2. Dipendenze Python
# ---------------------------------------------------------------------------
step "[2/5] Installo dipendenze Python..."
"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r requirements.txt
success "[OK] Dipendenze Python installate"

# ---------------------------------------------------------------------------
# 3. Dipendenze npm
# ---------------------------------------------------------------------------
step "[3/5] Installo dipendenze npm..."
if [ -f "package-lock.json" ]; then
    npm ci
else
    npm install
fi
success "[OK] Dipendenze npm installate"

# ---------------------------------------------------------------------------
# 4. Asset frontend
# ---------------------------------------------------------------------------
step "[4/5] Copio asset frontend in locale..."
npm run setup
success "[OK] Asset frontend copiati tramite scripts/setup-assets.js"

# ---------------------------------------------------------------------------
# 5. Database
# ---------------------------------------------------------------------------
step "[5/5] Eseguo migrazioni Django..."
"$VENV_PY" manage.py migrate
success "[OK] Database aggiornato"

# ---------------------------------------------------------------------------
# Riepilogo
# ---------------------------------------------------------------------------
echo ""
echo "=================================="
success "SETUP COMPLETATO CON SUCCESSO"
echo "=================================="
echo ""
step "Prossimi passi:"
echo "  1. Attiva il virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Crea un superuser (se necessario):"
echo "     python manage.py createsuperuser"
echo ""
echo "  3. Avvia il server di sviluppo:"
echo "     python manage.py runserver"
echo ""
echo "  4. Apri http://127.0.0.1:8000/ nel browser"
echo ""
echo "Per l'admin: http://127.0.0.1:8000/admin/"
echo ""
