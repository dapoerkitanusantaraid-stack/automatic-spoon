#!/usr/bin/env bash
set -euo pipefail

# Interactive Termux setup script for Project Server
# Usage: cd project-root && ./scripts/termux_setup.sh

if ! command -v pkg >/dev/null 2>&1; then
  echo "This script is intended to run on Termux (pkg not found). Aborting."
  exit 1
fi

echo "[1/6] Updating packages..."
pkg update && pkg upgrade -y

echo "[2/6] Installing runtime dependencies..."
pkg install -y python git clang make openssl-tool libffi libcrypt-dev wget unzip

echo "[3/6] Granting storage permission (you will be prompted)..."
termux-setup-storage || true

echo "[4/6] Creating virtualenv..."
python -m venv .venv
source .venv/bin/activate

echo "[5/6] Installing Python packages (may take several minutes)..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

echo "[6/6] Copy .env.example -> .env (edit .env before running)"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from template. Please edit .env (nano .env) and set TELEGRAM_TOKEN etc."
else
  echo ".env already exists; edit if needed: nano .env"
fi

cat <<'EOF'

Setup complete.
To run the server:

  source .venv/bin/activate
  python -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

Optional (background):
  nohup python -m uvicorn server.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

To set Telegram webhook after configuring .env and TELEGRAM token, run:
  ./scripts/set_telegram_webhook.sh

EOF
